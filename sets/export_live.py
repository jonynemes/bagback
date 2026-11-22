import re, json
src=open('gen.py').read()
ns={}
# exec only the P dict definition
m=re.search(r'^P=\{.*?^\}', src, re.S|re.M) or re.search(r'^P=\{.*?\}\s*$', src, re.S|re.M)
start=src.index('\nP={')+1
# find end: matching brace
depth=0
for i,ch in enumerate(src[start:],start):
    if ch=='{': depth+=1
    elif ch=='}':
        depth-=1
        if depth==0: end=i+1; break
exec(src[start:end],ns)
P=ns['P']
RB={0:("Black","#05131D"),1:("Blue","#0055BF"),2:("Green","#237841"),3:("Dark Turquoise","#008F9B"),4:("Red","#C91A09"),5:("Dark Pink","#C870A0"),
6:("Brown","#583927"),7:("Light Gray","#9BA19D"),8:("Dark Gray","#6D6E5C"),9:("Light Blue","#B4D2E3"),10:("Bright Green","#4B9F4A"),11:("Light Turquoise","#55A5AF"),
12:("Salmon","#F2705E"),13:("Pink","#FC97AC"),14:("Yellow","#F2CD37"),15:("White","#FFFFFF"),17:("Light Green","#C2DAB8"),18:("Light Yellow","#FBE696"),
19:("Tan","#E4CD9E"),20:("Light Violet","#C9CAE2"),22:("Purple","#81007B"),23:("Dark Blue-Violet","#2032B0"),25:("Orange","#FE8A18"),26:("Magenta","#923978"),
27:("Lime","#BBE90B"),28:("Dark Tan","#958A73"),29:("Bright Pink","#E4ADC8"),30:("Medium Lavender","#AC78BA"),31:("Lavender","#E1D5ED"),
33:("Trans-Dark Blue","#0020A0"),34:("Trans-Green","#84B68D"),35:("Trans-Bright Green","#D9E4A7"),36:("Trans-Red","#C91A09"),40:("Trans-Black","#635F52"),
41:("Trans-Light Blue","#AEEFEC"),42:("Trans-Neon Green","#F8F184"),43:("Trans-Very Lt Blue","#C1DFF0"),45:("Trans-Dark Pink","#DF6695"),
46:("Trans-Yellow","#F5CD2F"),47:("Trans-Clear","#FCFCFC"),52:("Trans-Purple","#A5A5CB"),57:("Trans-Orange","#F08F1C"),68:("Very Light Orange","#F3CF9B"),
69:("Light Purple","#CD6298"),70:("Reddish Brown","#582A12"),71:("Light Bluish Gray","#A0A5A9"),72:("Dark Bluish Gray","#6C6E68"),73:("Medium Blue","#5A93DB"),
74:("Medium Green","#73DCA1"),77:("Light Pink","#FECCCF"),78:("Light Nougat","#F6D7B3"),80:("Metallic Silver","#A5A9B4"),82:("Metallic Gold","#DBAC34"),
84:("Medium Nougat","#AA7D55"),85:("Dark Purple","#3F3691"),86:("Light Brown","#7C503A"),89:("Royal Blue","#4C61DB"),92:("Nougat","#D09168"),
100:("Light Salmon","#FEBABD"),110:("Violet","#4354A3"),112:("Medium Bluish Violet","#6874CA"),115:("Medium Lime","#C7D23C"),118:("Aqua","#B3D7D1"),
120:("Light Lime","#D9E4A7"),125:("Light Orange","#F9BA61"),151:("Very Light Bluish Gray","#E6E3E0"),179:("Flat Silver","#898788"),182:("Trans-Orange","#F08F1C"),
191:("Bright Light Orange","#F8BB3D"),212:("Bright Light Blue","#9FC3E9"),216:("Rust","#B31004"),226:("Bright Light Yellow","#FFF03A"),232:("Sky Blue","#7DBFDD"),
272:("Dark Blue","#0A3463"),288:("Dark Green","#184632"),297:("Pearl Gold","#AA7F2E"),308:("Dark Brown","#352100"),313:("Maersk Blue","#3592C3"),
320:("Dark Red","#720E0F"),321:("Dark Azure","#078BC9"),322:("Medium Azure","#36AEBF"),323:("Light Aqua","#ADC3C0"),326:("Yellowish Green","#DFEEA5"),
330:("Olive Green","#9B9A5A"),335:("Sand Red","#D67572"),351:("Medium Dark Pink","#F785B1"),353:("Coral","#FF698F"),366:("Earth Orange","#FA9C1C"),
373:("Sand Purple","#845E84"),378:("Sand Green","#A0BCAC"),379:("Sand Blue","#6074A1"),383:("Chrome Silver","#E0E0E0"),450:("Fabuland Brown","#B67B50"),
462:("Medium Orange","#FFA70B"),484:("Dark Orange","#A95500"),503:("Very Light Gray","#E6E3DA"),1050:("Trans-Clear Glitter","#E6E6E6"),
1088:("Medium Brown","#755945"),1089:("Warm Tan","#CCA373"),1103:("Pastel Blue","#B3D7FF"),1135:("Vibrant Coral","#EF5B6B"),
1136:("Reddish Orange","#CA4C0B"),1140:("Dark Nougat","#AD6140"),1142:("Light Lilac","#D3BDE3")}
js="const RB_COLORS="+json.dumps({str(k):v for k,v in RB.items()},separators=(',',':'))+";\n"
js+="const PART_NAMES="+json.dumps(P,separators=(',',':'),ensure_ascii=False)+";\n"
open('live_data.js','w').write(js); print(len(P), len(js))
