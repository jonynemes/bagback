import re
old=open('/home/claude/lego-sorter/index.html',encoding='utf-8').read()
t=open('template.html',encoding='utf-8').read()
def cut(a,b):
    i=old.index(a); j=old.index(b,i); return old[i:j]
core=cut('<script id="core">','</script>')+'</script>'
set31=cut('const SET_31058=','const PRESETS=')
tr=[("לבנה מקושתת","Arch brick"),("פלטת רבע עיגול","Quarter-round plate"),("פלטת כנף","Wing plate"),("גג הפוך","Inverted slope"),
("לבנה פינתית","Corner brick"),("פלטה מעוגלת","Curved plate"),("פלטה עגולה","Round plate"),("פלטה מקושתת","Curved-side plate"),
("כדור חיכוך","Friction ball"),("שקע כדור","Ball socket"),("מחזיק מנורה","Lamp holder"),("קצה זנב","Tail tip"),
("עם כדורים","w/ balls"),("עם כדור","w/ ball"),("עם בליטות צד","w/ side studs"),("עם מוט","w/ bar"),("עם שקע כדור","w/ ball socket"),
("עם שקע","w/ socket"),("עם בליטה","w/ stud"),("עם מזלג","w/ fork"),("עם חור וקורה","w/ hole & beam"),("עם חור","w/ hole"),
("עם קליפס","w/ clip"),("עם מחזיק","w/ holder"),("עם שיניים","w/ teeth"),("כדור עין","(eye)"),
("לבנה","Brick"),("פלטה","Plate"),("אריח","Tile"),("עגול","Round"),("ציר","Axle"),("מוט","Bar"),("שן","Tooth"),("קרן","Horn"),
("מחזיק","Holder"),("להב","Blade"),("מחבר","Connector"),("חלק","Part"),("גג","Slope")]
tr.sort(key=lambda x:-len(x[0]))
for a,b in tr: set31=set31.replace(a,b)
set31=re.sub(r'name:"[^"]*",note:"[^"]*"','name:"31058 Mighty Dinosaurs",note:"Real parts list (Brickset). Bag split is a placeholder, not from the instructions."',set31)
assert not re.search('[֐-׿]',set31), re.findall('[֐-׿]+',set31)[:5]
# fix word order "Brick 2x2 w/ balls" fine; dims stay
draw=cut('function parseShape(desc){','/* ================= main loop')
NEWPS='''function parseShape(desc){
  const m=/(\\d+)\\s*[x×]\\s*(\\d+)/.exec(desc||""); const a=m?+m[1]:1, b=m?+m[2]:2;
  const kind=/tile|אריח/i.test(desc)?"tile":(/^\\s*round|עגול/i.test(desc)&&a*b===1)?"round":/plate|פלטה/i.test(desc)?"plate":"brick";
  return {kind,a,b};
}
'''
draw=re.sub(r'function parseShape\(desc\)\{.*?\n\}\n',lambda m:NEWPS,draw,count=1,flags=re.S)
loop=cut('let srcW=960,srcH=640,crop=null;','const studsOf=')
lab=cut('const studsOf=','$("freeze").onclick')
import re as _re
lab=_re.sub(r'let scale = ratios.length>=3 \? [^;]*;','let scale=null;',lab)
for a,b2 in [('c.tiny = !!scale && c.area < scale*0.35;','c.tiny = !!scale && (c.area < scale*0.6 || (its.length && c.area/scale < Math.min(...its.map(i=>i.studs))*0.45));'),
             ('else if(fit.length) cand=fit;','else if(fit.length && studs>=1.4) cand=fit;'),
             ('else if(studs<minS) cand=','else if(studs<minS && studs>=1.4) cand=')]:
    assert a in lab, a
    lab=lab.replace(a,b2)
t=t.replace('/*REALSETS*/',open('/home/claude/sets/realsets.js',encoding='utf-8').read())
t=t.replace('/*TRACKER*/',open('tracker.js',encoding='utf-8').read())
t=t.replace('/*CORE*/',core).replace('/*SET31058*/',set31).replace('/*DRAW*/',draw).replace('/*LOOP*/',loop).replace('/*OVERLAY*/',lab)
t=t.replace('const S2=S; ','')
open('index.html','w',encoding='utf-8').write(t)
print(len(t), re.findall('[֐-׿]+',t)[:20])
