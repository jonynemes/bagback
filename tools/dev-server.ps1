# Local dev server for bagback/site, no Node/Python needed.
# Serves the app on http://localhost:8080/ and mirrors Netlify's _redirects:
#   /lb/*  -> https://locabriques.fr/api/*      (needed: locabriques blocks browser CORS)
#   /bk/*  -> https://api.brickognize.com/*
# Usage (from repo root):  powershell -ExecutionPolicy Bypass -File tools\dev-server.ps1
param([string]$Root = (Join-Path $PSScriptRoot '..\bagback\site'), [int]$Port = 8080)

$Root = [IO.Path]::GetFullPath($Root)
$proxies = @{ '/lb/' = 'https://locabriques.fr/api/'; '/bk/' = 'https://api.brickognize.com/' }
$types = @{ '.html'='text/html; charset=utf-8'; '.js'='text/javascript; charset=utf-8'; '.json'='application/json';
  '.css'='text/css'; '.png'='image/png'; '.jpg'='image/jpeg'; '.svg'='image/svg+xml'; '.ico'='image/x-icon';
  '.webmanifest'='application/manifest+json' }
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

function Send-Proxy($ctx, $target) {
  $req = $ctx.Request; $res = $ctx.Response
  $up = [Net.HttpWebRequest]::Create($target)
  $up.Method = $req.HttpMethod
  $up.UserAgent = 'bagback-dev'
  $up.Accept = $(if ($req.Headers['Accept']) { $req.Headers['Accept'] } else { '*/*' })
  if ($req.HasEntityBody) {
    $up.ContentType = $req.ContentType
    $ms = New-Object IO.MemoryStream; $req.InputStream.CopyTo($ms)
    $up.ContentLength = $ms.Length
    $s = $up.GetRequestStream(); $ms.WriteTo($s); $s.Close()
  }
  try { $r = $up.GetResponse() } catch [Net.WebException] { $r = $_.Exception.Response; if (-not $r) { throw } }
  $res.StatusCode = [int]$r.StatusCode
  if ($r.ContentType) { $res.ContentType = $r.ContentType }
  $r.GetResponseStream().CopyTo($res.OutputStream); $r.Close()
}

$l = New-Object Net.HttpListener
$l.Prefixes.Add("http://localhost:$Port/")
$l.Start()
Write-Host "Serving $Root on http://localhost:$Port/  (proxy: /lb/ /bk/)"
while ($l.IsListening) {
  $ctx = $l.GetContext()
  try {
    $path = $ctx.Request.Url.AbsolutePath
    $hit = $proxies.Keys | Where-Object { $path.StartsWith($_) } | Select-Object -First 1
    if ($hit) {
      Send-Proxy $ctx ($proxies[$hit] + $path.Substring($hit.Length) + $ctx.Request.Url.Query)
    } else {
      $file = [IO.Path]::GetFullPath((Join-Path $Root ([Uri]::UnescapeDataString($path).TrimStart('/'))))
      if (-not $file.StartsWith($Root)) { $ctx.Response.StatusCode = 403 }
      else {
        if (Test-Path $file -PathType Container) { $file = Join-Path $file 'index.html' }
        if (Test-Path $file -PathType Leaf) {
          $ext = [IO.Path]::GetExtension($file).ToLower()
          $ctx.Response.ContentType = $(if ($types.ContainsKey($ext)) { $types[$ext] } else { 'application/octet-stream' })
          $b = [IO.File]::ReadAllBytes($file); $ctx.Response.OutputStream.Write($b, 0, $b.Length)
        } else { $ctx.Response.StatusCode = 404 }
      }
    }
  } catch { Write-Host "ERR $($ctx.Request.Url): $($_.Exception.Message)"; try { $ctx.Response.StatusCode = 502 } catch {} }
  try { $ctx.Response.Close() } catch {}
}
