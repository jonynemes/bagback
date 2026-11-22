/* ===== Piece tracking: keeps each piece's identity across frames so labels don't flicker =====
   - matches pieces frame-to-frame (same colour, nearby, after compensating camera motion)
   - each piece votes on its bag over time; only a steady answer is shown
   - badges glide and fade instead of jumping */
const Tracker={
  tracks:[], nid:1,
  reset(){ this.tracks=[]; },
  update(r){
    if(r._tracked) return; r._tracked=true;
    const W=r.W, comps=r.comps.filter(c=>!c.tiny);
    const T=this.tracks;
    // 1) camera motion: median shift of rough nearest matches
    const dxs=[],dys=[];
    for(const c of comps){ let best=null,bd=(W*0.15)**2;
      for(const t of T){ if(t.color!==c.color) continue; const d=(t.x-c.cx)**2+(t.y-c.cy)**2; if(d<bd){bd=d;best=t;} }
      if(best){dxs.push(c.cx-best.x);dys.push(c.cy-best.y);} }
    const med=a=>{if(!a.length)return 0;const s=a.slice().sort((p,q)=>p-q);return s[s.length>>1];};
    const ox=med(dxs), oy=med(dys);
    // 2) tight matching, biggest pieces first
    const used=new Set();
    for(const c of comps.slice().sort((a,b)=>b.area-a.area)){
      const R=Math.max(W*0.03, Math.sqrt(c.area)*0.7); let best=null,bd=R*R;
      for(const t of T){ if(used.has(t)||t.color!==c.color) continue; const d=(t.x+ox-c.cx)**2+(t.y+oy-c.cy)**2; if(d<bd){bd=d;best=t;} }
      const key=c.bags.join(",");
      if(best){ used.add(best);
        best.x=c.cx; best.y=c.cy; best.area=best.area*0.6+c.area*0.4; best.seen++; best.missed=0;
        for(const k in best.votes) best.votes[k]*=0.85; best.votes[key]=(best.votes[key]||0)+1; c.track=best;
      } else {
        const t={id:this.nid++,color:c.color,x:c.cx,y:c.cy,dx:c.cx,dy:c.cy,area:c.area,seen:1,missed:0,votes:{[key]:1},alpha:0};
        T.push(t); used.add(t); c.track=t;
      }
    }
    // 3) pieces not seen this frame drift with the camera, then fade out
    for(const t of T) if(!used.has(t)){ t.missed++; t.x+=ox; t.y+=oy; t.dx+=ox; t.dy+=oy; }
    this.tracks=T.filter(t=>t.missed<=6);
    // 4) steady answer per track
    for(const t of this.tracks){
      let bk=null,bv=0,tot=0; for(const k in t.votes){tot+=t.votes[k]; if(t.votes[k]>bv){bv=t.votes[k];bk=k;}}
      t.key = (t.seen>=3 && bv/tot>=0.6) ? bk : null;
      t.bags = t.key ? t.key.split(",").filter(Boolean).map(Number) : [];
    }
  },
  /* what a track shows for the chosen bag: "sure" | "maybe" | "no" | null (not steady yet) */
  stateOf(t,bag){
    if(!t||!t.key||t.missed>2) return null;
    if(!bag) return t.bags.length===1?"sure":"maybe";
    if(!t.bags.includes(bag)) return "no";
    return t.bags.length===1?"sure":"maybe";
  },
  /* per drawn frame: glide and fade */
  animate(bag,minArea){
    for(const t of this.tracks){
      const show = this.stateOf(t,bag)==="sure" && t.area>=minArea;
      t.alpha += ((show?1:0)-t.alpha)*0.18;
      t.dx += (t.x-t.dx)*0.3; t.dy += (t.y-t.dy)*0.3;
    }
  }
};

function _hexRgb(h){const n=parseInt(h.slice(1),16);return [n>>16&255,n>>8&255,n&255];}
/* overlay mask: dim everything except steady pieces of the chosen bag; soft outline + tint on those */
function buildMaskInto(r,bag,ovlC,dimC){
  const W=r.W,H=r.H,cs=r.comps, L=Int32Array.from(r.labels);
  for(let pass=0;pass<4;pass++) for(let i=0;i<L.length;i++){ const l=L[i]; if(l<0||!cs[l].tiny) continue; const x=i%W;
    for(const j of [i-1,i+1,i-W,i+W]){ if(j<0||j>=L.length||(j===i-1&&x===0)||(j===i+1&&x===W-1)) continue; const m=L[j]; if(m>=0&&!cs[m].tiny){L[i]=m;break;} } }
  ovlC.width=W; ovlC.height=H; dimC.width=W; dimC.height=H;
  const oc=ovlC.getContext("2d"), dc=dimC.getContext("2d");
  const im=oc.createImageData(W,H), d=im.data, dm=dc.createImageData(W,H), dd=dm.data;
  const col=cs.map(c=>{ if(c.tiny) return null; const s=Tracker.stateOf(c.track,bag); if(s!=="sure") return null;
    return _hexRgb(bag?bagColor(bag):bagColor(c.track.bags[0])); });
  for(let i=0,p=0;i<L.length;i++,p+=4){ const l=L[i];
    if(l<0||!col[l]){ if(bag) dd[p+3]=165; continue; }
    const x=i%W, e=x===0||x===W-1||i<W||i>=L.length-W||L[i-1]!==l||L[i+1]!==l||L[i-W]!==l||L[i+W]!==l;
    const c=col[l]; d[p]=c[0];d[p+1]=c[1];d[p+2]=c[2]; d[p+3]= e?255:(bag?50:0);
  }
  oc.putImageData(im,0,0); dc.putImageData(dm,0,0);
}
/* draw mask + glowing outlines + badges at canvas size cw x ch */
function drawTracked(ctx,r,bag,ovlC,dimC,cw,ch,opt){
  opt=opt||{};
  ctx.save(); ctx.imageSmoothingEnabled=true; ctx.imageSmoothingQuality="high";
  if(bag) ctx.drawImage(dimC,0,0,cw,ch);
  ctx.shadowColor=bag?bagColor(bag):"rgba(0,0,0,0)"; ctx.shadowBlur=bag?(opt.glow||14):0;
  ctx.drawImage(ovlC,0,0,cw,ch); ctx.restore();
  const sx=cw/r.W, sy=ch/r.H, minA=(r.scale||40)*0.5;
  Tracker.animate(bag,minA);
  const R0=opt.badge||Math.max(13,cw/42);
  ctx.save(); ctx.textAlign="center"; ctx.textBaseline="middle";
  for(const t of Tracker.tracks){
    if(t.alpha<0.03) continue;
    const x=t.dx*sx, y=t.dy*sy; if(x<R0||x>cw-R0||y<R0||y>ch-R0) continue;
    const num=bag||t.bags[0]; if(!num) continue;
    const R=R0*(0.75+0.25*t.alpha), c=bagColor(num);
    ctx.globalAlpha=t.alpha;
    ctx.shadowColor="rgba(0,0,0,.45)"; ctx.shadowBlur=R*0.6; ctx.fillStyle=c;
    ctx.beginPath(); ctx.arc(x,y,R,0,7); ctx.fill(); ctx.shadowBlur=0;
    ctx.lineWidth=Math.max(2,R*0.14); ctx.strokeStyle="#fff"; ctx.stroke();
    ctx.fillStyle="#fff"; ctx.font=`800 ${Math.round(R*1.1)}px "Plus Jakarta Sans",system-ui,sans-serif`; ctx.fillText(String(num),x,y+1);
  }
  ctx.restore();
}
function trackedCount(bag){ let n=0; for(const t of Tracker.tracks) if(t.alpha>0.5) n++; return n; }
