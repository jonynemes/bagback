import json, re
raw=json.load(open('raw.json'))
# BrickLink colour id -> (name, hex)
BL={0:("Mixed","#9BA19D"),1:("White","#F4F4F4"),2:("Tan","#E4CD9E"),3:("Yellow","#F2CD37"),4:("Orange","#FE8A18"),5:("Red","#C91A09"),
6:("Green","#237841"),7:("Blue","#0055BF"),11:("Black","#1B2A34"),12:("Trans-Clear","#E6EEF2"),13:("Trans-Black","#635F52"),14:("Trans-Dark Blue","#0020A0"),
15:("Trans-Light Blue","#AEEFEC"),17:("Trans-Red","#C91A09"),19:("Trans-Yellow","#F5CD2F"),20:("Trans-Green","#84B68D"),23:("Pink","#FC97AC"),
28:("Nougat","#D09168"),34:("Lime","#BBE90B"),36:("Bright Green","#4B9F4A"),39:("Dark Turquoise","#008F9B"),42:("Medium Blue","#5A93DB"),
47:("Dark Pink","#C870A0"),48:("Sand Green","#A0BCAC"),50:("Trans-Dark Pink","#DF6695"),55:("Sand Blue","#6074A1"),59:("Dark Red","#720E0F"),
63:("Dark Blue","#0A3463"),65:("Metallic Gold","#DBAC34"),67:("Metallic Silver","#A5A9B4"),68:("Dark Orange","#A95500"),69:("Dark Tan","#958A73"),
71:("Magenta","#923978"),80:("Dark Green","#184632"),85:("Dark Bluish Gray","#6C6E68"),86:("Light Bluish Gray","#A0A5A9"),88:("Reddish Brown","#582A12"),
89:("Dark Purple","#3F3691"),90:("Light Nougat","#F6D7B3"),95:("Flat Silver","#898788"),98:("Trans-Orange","#F08F1C"),103:("Bright Light Yellow","#FFF03A"),
104:("Bright Pink","#E4ADC8"),105:("Bright Light Blue","#9FC3E9"),108:("Trans-Bright Green","#D9E4A7"),110:("Bright Light Orange","#F8BB3D"),
115:("Pearl Gold","#AA7F2E"),120:("Dark Brown","#352100"),150:("Medium Nougat","#AA7D55"),152:("Light Aqua","#ADC3C0"),153:("Dark Azure","#078BC9"),
154:("Lavender","#E1D5ED"),155:("Olive Green","#9B9A5A"),156:("Medium Azure","#36AEBF"),157:("Medium Lavender","#AC78BA"),167:("Reddish Orange","#CA4C0B"),
220:("Coral","#FF698F"),240:("Medium Brown","#755945")}
# best-effort part names with footprint in the name (used for size reasoning and the demo pile)
P={"3023":"Plate 1x2","54200":"Slope 30 1x1","85984":"Slope 30 1x2","3710":"Plate 1x4","3022":"Plate 2x2","25269":"Tile 1x1 quarter round",
"11477":"Slope curved 1x2","3020":"Plate 2x4","4073":"Round plate 1x1","3069":"Tile 1x2","3005":"Brick 1x1","3024":"Plate 1x1","98138":"Round tile 1x1",
"3004":"Brick 1x2","3021":"Plate 2x3","35480":"Plate 1x2 rounded","41740":"Plate 1x4 w/ 2 studs","15068":"Slope curved 2x2","3622":"Brick 1x3",
"4589b":"Round cone 1x1","87079":"Tile 2x4","13965":"Brick arch 1x3","3062":"Round brick 1x1","2412b":"Tile 1x2 grille","2357":"Brick corner 2x2",
"6636":"Tile 1x6","3040":"Slope 45 1x2","2431":"Tile 1x4","3623":"Plate 1x3","6541":"Technic brick 1x1","99207":"Bracket 2x2 inverted",
"85861":"Round plate 1x1 open stud","87580":"Plate 2x2 jumper","3010":"Brick 1x4","4032":"Plate round 2x2","26601":"Tile 2x2 triangular",
"99563":"Tile 1x2 ingot","14716":"Brick 1x1x3","3001":"Brick 2x4","3070":"Tile 1x1","87087":"Brick 1x1 side stud","2420":"Plate corner 2x2",
"3795":"Plate 2x6","38320":"Window pane 1x2","2780":"Technic pin 1x1","44728":"Bracket 1x2","60592":"Window 1x2","3068":"Tile 2x2",
"15573":"Plate 1x2 jumper","93606":"Slope curved 2x4","32607":"Round leaves 1x1","28192":"Slope 45 1x2 cutout","11211":"Brick 1x2 side studs",
"3032":"Plate 4x6","30136":"Brick 1x2 log","3003":"Brick 2x2","3660":"Slope inverted 2x2","32062":"Technic axle 1x2","98283":"Brick 1x2 masonry",
"99781":"Bracket 1x2","3937":"Hinge brick 1x2","6134":"Hinge top 2x2","3009":"Brick 1x6","29119":"Slope curved 1x2 right","29120":"Slope curved 1x2 left",
"11458":"Plate 1x2 pin hole","3666":"Plate 1x6","3460":"Plate 1x8","24866":"Round flower plate 1x1","2449":"Slope inverted 75 1x2",
"3700":"Technic brick 1x2","53451":"Barb 1x1","87747":"Barb 1x1","43888":"Round brick 1x1 tall","34103":"Plate 1x3 w/ 2 studs","3002":"Brick 2x3",
"93273":"Slope curved 1x4 double","36841":"Round plate 1x1 w/ bar","3941":"Brick round 2x2","41769":"Wedge plate 2x4 right","41770":"Wedge plate 2x4 left",
"23443":"Bar holder 1x1","15100":"Technic pin 1x1","15712":"Tile 1x1 clip","32013":"Technic connector 1x1","22885":"Brick 1x2 side studs",
"18654":"Round beam 1x1","26603":"Tile 2x3","30414":"Brick 1x4 side studs","4286":"Slope 33 1x3","50950":"Slope curved 1x3","4070":"Brick 1x1 headlight",
"18980":"Plate round corner 2x6","60478":"Plate 1x2 handle","4274":"Technic pin 1x1","20482":"Round tile 1x1 w/ bar","6014b":"Round wheel 1x1",
"3008":"Brick 1x8","3034":"Plate 2x8","61252":"Plate 1x1 clip","4460b":"Slope 75 1x2","49311":"Brick 1x4 tall","2540":"Plate 1x2 handle",
"3665":"Slope inverted 1x2","4162":"Tile 1x8","3673":"Technic pin 1x1","14417":"Plate 1x2 ball","14418":"Plate 1x2 ball cup","6558":"Technic pin 1x1",
"2429c01":"Hinge plate 1x4","48336":"Plate 1x2 handle end","33909":"Tile 2x2 w/ studs","2432":"Tile 1x2 handle","30413":"Panel 1x4","6081":"Slope curved 2x4",
"3176":"Plate 2x3 hole","87083":"Technic axle 1x1","11476":"Plate 1x2 clip","4477":"Plate 1x10","4871":"Slope inverted 2x4","6111":"Brick 1x10",
"3832":"Plate 2x10","3709":"Technic plate 2x4","3701":"Technic brick 1x4","3894":"Technic brick 1x6","3028":"Plate 6x12","3030":"Plate 4x10",
"3035":"Plate 4x8","3038":"Slope 45 2x3","3039":"Slope 45 2x2","3298":"Slope 33 2x3","4287":"Slope inverted 33 1x3","3747b":"Slope inverted 33 2x3",
"4740":"Dish inverted 2x2","3044c":"Slope 45 double 1x2","2730":"Technic brick 1x10","6005":"Brick arch 1x3","2454":"Brick 1x2 tall","14719":"Tile corner 2x2",
"3749":"Technic axle pin 1x1","3829c01":"Steering wheel 1x2","56890":"Tire 2x2","98282":"Mudguard 2x4","44567b":"Hinge plate 1x2","32028":"Plate 1x2 door rail",
"52036":"Vehicle base 4x12","6157":"Plate 2x2 wheel holder","44865":"Brick 1x2 pin","98281":"Wedge 4x6","57783":"Windscreen 3x4","2877":"Brick 1x2 grille",
"14769":"Tile round 2x2","14520":"Brick 2x4 arches","52501":"Slope inverted 1x6","85974":"Minifig hair 1x1","3460":"Plate 1x8","3245c":"Brick 1x2x2",
"4865b":"Panel 1x2","60470b":"Plate 1x2 clips","2431pb0733":"Tile 1x4 printed","4265c":"Technic bush 1x1","6538c":"Technic axle connector 1x1",
"77845":"Tile 1x2 rounded","44861":"Brick 1x1 axle","3034":"Plate 2x8","24299":"Wedge plate 2x2 right","24307":"Wedge plate 2x2 left",
"80545":"Tile 1x1 half round","2423":"Leaves 2x2","5489":"Round leaves 2x2","65578":"Bar holder 1x1","26287":"Brick 1x1 bracket","6254":"Minifig item 1x1",
"60475b":"Brick 1x1 clip","60596":"Door frame 1x4","2498":"Brick 2x2 corner","61678":"Slope curved 1x4","85943":"Brick round 2x2","1126":"Tile 1x1 round",
"39613":"Tile 1x1 round","4519":"Technic axle 1x1","3830":"Hinge brick 1x4","3831":"Hinge brick top 1x4","4151b":"Plate 2x2 jumper","30237b":"Brick 1x2 rounded",
"41879":"Minifig legs 1x2","973pb4420c01":"Minifig torso 1x2"}
def name(pid):
    if pid in P: return P[pid]
    if pid.startswith('3626'): return "Minifig head 1x1"
    if pid.startswith('970') or pid.startswith('971'): return "Minifig legs 1x2"
    if pid.startswith('973') or pid.startswith('976'): return "Minifig torso 1x2"
    base=re.sub(r'(pb|pr)\w+$','',pid)
    if base in P: return P[base]+" (printed)"
    return f"Part {pid}"
SETS=[("60362","Car Wash",2023,"City"),("60430","Interstellar Spaceship",2024,"City"),("60500","The LEGO Van",2026,""),
("41422","Panda Jungle Tree House",2020,"Friends"),("31170","Pink Flamingo",2025,"Creator"),("40487","Sailboat Adventure",2021,""),
("76426","Hogwarts Castle Boathouse",2024,"Harry Potter"),("76398","Hogwarts Hospital Wing",2022,"Harry Potter"),
("60320","Fire Station",2022,"City"),("31151","T. rex",2024,"Creator")]
used=set(); out=[]; known=tot=0
for num,nm,yr,th in SETS:
    items=[]; pieces=0
    for b,its in raw[num]:
        bag=max(1,b)   # loose parts (bag 0) are packed with bag 1 here
        for t,pid,col,q in its:
            if 'stk' in pid: continue
            c=int(col); used.add(c); n=name(pid); tot+=q; known+= (not n.startswith('Part '))*q
            items.append({"bag":bag,"color":f"bl{c}","qty":q,"desc":n,"part":pid}); pieces+=q
    nb=len(set(i["bag"] for i in items))
    out.append({"num":num,"name":nm,"year":yr,"theme":th,"pieces":pieces,"bagsN":nb,"name_full":f"{num} {nm}","items":items})
print("named pieces", round(known/tot*100,1), "%")
pal={f"bl{c}":{"he":BL.get(c,("Other","#9BA19D"))[0],"hex":BL.get(c,("Other","#9BA19D"))[1]} for c in sorted(used)}
missing=[c for c in used if c not in BL]; print("unmapped colours",missing)
js="const BL_PALETTE="+json.dumps(pal)+";\nfor(const k in BL_PALETTE){PALETTE[k]=BL_PALETTE[k];PALETTE[k].lab=hexToLab(PALETTE[k].hex);}\n"
js+="const REAL_SETS="+json.dumps([{"num":s["num"],"name":s["name"],"year":s["year"],"theme":s["theme"],"pieces":s["pieces"],"bagsN":s["bagsN"]} for s in out])+";\n"
js+="const REAL_SET_DATA={"+",".join(f'"{s["num"]}":{{name:{json.dumps(s["name_full"])},note:"Real bag-by-bag inventory (Brick Bag Inventory).",items:{json.dumps(s["items"],separators=(",",":"))}}}' for s in out)+"};\n"
open('realsets.js','w').write(js); print(len(js))
