"""Rebuild KDN's physical PDF page 50 from the user's original PDF."""

from hwpx_layout import Layout, cell
from pdf_coords import recipe_inputs

source, target = recipe_inputs(50, '세부 평가내용별 추진실적')
layout = Layout(top=6550)
add_text, add_table, border = layout.add_text, layout.add_table, layout.border
p, center = layout.p, layout.center
reg, only = source.region, source.only

def ps(values,size=1080,bold=False,align="LEFT",ratio=90,color="#161616",line=1250):
    if isinstance(values,str): values=[values]
    return [p(t,size,bold,color,align=align,line=line,ratio=ratio) for t in values]

def c(i,w,h,v,fill="1",*,bold=False,align="LEFT",size=1080,ratio=90,color="#161616",span=1,cols=1,line=1250):
    return cell(i,w,h,ps(v,size,bold,align,ratio,color,line),fill,span,cols)

def label(i,w,h,v,fill=None,**kwargs):
    return c(i,w,h,v,fill or gray,bold=True,align="CENTER",**kwargs)

def tab(rows,gap=0):
    return add_table(rows,gap=gap)

gray=border("#E9E9E9",top="soft",bottom="soft")
gray2=border("#D8D8D8",top="strong",bottom="soft",sides="soft")
white=border(top="soft",bottom="soft",sides="soft")
dark=border("#686868",top="strong",bottom="soft")
outline=border(top="strong",bottom="soft",sides="soft")
grid=border(bottom="soft",sides="soft")
striped=border("#E9E9E9",top="strong",bottom="soft",sides="soft",pattern=True)
W=49900
add_text(only(190,220,70,74),1800,True,align="CENTER",line=2400,after=1000)
tab([[label(0,7000,2800,"평가내용 01",dark,color="#FFFFFF",size=1000,ratio=82),
      c(1,42900,2800,only(120,135,111,116),striped,size=1120,ratio=77)]],1100)

def section_heading(num,y,gap=450):
    tab([[label(0,2850,2200,str(num),dark,color="#FFFFFF",size=1720,line=1850),
          c(1,47050,2200,only(90,100,y,y+3),gray,bold=True,size=1470,ratio=84,line=1800)]],gap)

section_heading(1,149)
tab([[label(0,5600,3480,"추진배경",gray2),
      c(1,21000,3480,reg(110,120,178,198),white,ratio=83),
      c(2,23300,3480,reg(320,330,178,198),white,ratio=75)]],260)
add_text(only(170,180,214,218),1120,True,align="CENTER",line=1500,after=190)
for y,labeltext,fill in [(236,"일자리 비전",gray2),(262,"일자리 목표",white)]:
    tab([[label(0,5900,2230,labeltext),c(1,44000,2230,only(185,450,y,y+3),fill,
          bold=y==236,align="CENTER",size=1120)]],360)

# Numeric table with grouped category rows and merged source and unit labels.
w=[5900,2570,5380,4100,4100,4100,4100,4100,15550]
assert sum(w)==49900
H=[1800,1550,1550,1550,1550,1550]
def num(i,j,v):
    return c(i,w[i],H[j],v,border(bottom="strong" if j==5 else "soft",sides="strong") if i==3 else grid,align="RIGHT",size=1110,ratio=94)
heads=[label(0,w[0],sum(H),"세부목표",span=6),
       label(1,w[1]+w[2],H[0],"구분 (단위:명)",gray2,cols=2)]
for i,v in enumerate(("’25년","~’27년","~’29년","~’32년","~’35년","설정근거"),3):
    heads.append(label(i,w[i],H[0],v,border("#686868",top="strong",bottom="soft",sides="strong") if i==3 else gray2,color="#FFFFFF" if i==3 else "#161616",ratio=87))
basis=["∙「2035 중장기 경영전략」 내 10개년","  인력계획･매출증가율 반영",
       "∙중장기 「일자리 혁신 전략」 반영한","  누적 13만명(’35년) 일자리 창출목표","  (연평균성장률 10.28%) 설정"]
rows=[heads]
for j,(name,values) in enumerate([
    ("정규직채용",["125","293","211","364","215"]),("체험형인턴",["110","172","156","234","234"]),
    ("주요사업",["4,109","9,656","12,010","23,301","31,790"]),("민간지원",["211","441","468","756","826"]),
    ("합  계",["4,555","10,562","12,845","24,655","33,065"])],1):
    row=[]
    if j in (1,3): row.append(label(1,w[1],H[j]*2,"공공" if j==1 else "민간",gray,span=2,size=1000))
    if j==5: row.append(label(1,w[1]+w[2],H[j],name,gray,cols=2))
    else: row.append(c(2,w[2],H[j],name,gray,align="CENTER",size=1060))
    row.extend(num(i,j,v) for i,v in enumerate(values,3))
    if j==1: row.append(c(8,w[8],sum(H[1:]),basis,white,size=1030,ratio=83,span=5))
    rows.append(row)
tab(rows,420)
for y,h,labeltext,is_head in [(392,2200,"추진전략",True),(419,4750,"추진과제",False)]:
    row=[label(0,5900,h,labeltext)]
    ranges=[(150,170),(300,320),(450,470)] if is_head else [(120,125),(265,275),(410,418)]
    for i,(x0,x1) in enumerate(ranges,1):
        v=reg(x0,x1,y,y+(4 if is_head else 30))
        if is_head: v=[f"{'①②③'[i-1]} {v[0]}"]
        row.append(c(i,14667 if i<3 else 14666,h,v,gray2 if is_head else white,bold=is_head,align="CENTER" if is_head else "LEFT",ratio=81 if not is_head and i==3 else 87))
    tab([row],460 if is_head else 950)

section_heading(2,472,380)
add_text(only(50,60,498,502),1380,True,line=1720,after=250,ratio=93)
# Small filled tag boxes inside a box: 배경 lines and card titles (PDF: tag and text on one line).
tag_fill=border("#686868")
def background_line(line,tag,gap=0):
    if not line.startswith("∙"+tag):
        raise ValueError(f"배경 line {line!r} does not start with ∙{tag}")
    return layout.tagged(tag,line[len(tag)+1:].strip(),45500,1300,tag_fill,lead="∙",tag_size=950,
                         size=1040,ratio=78,bold=False,align="LEFT",space=150,gap=gap)
direction=reg(100,450,535,539)
tab([[label(0,3900,3380,"배경"),cell(1,46000,3380,
      background_line(only(100,105,520,523),"환경분석",gap=250)+
      background_line(direction[0]+" ① "+direction[1]+" ② "+direction[2]+" ③ "+direction[3],"추진방향"),white)]],410)
# Three editable strategy cards with narrow gutters.
card_width=15650
gap_width=1475
# Each card title starts with a small filled tag box inside the title box.
card_tags=("예측 고도화","정부협의 체계화","고용유지 최대화")
def cards_row(y,h,mode):
    row=[]
    for i,(l,r) in enumerate([(57,220),(229,390),(400,560)]):
        if i: row.append(c(i*2-1,gap_width,h,"+" if mode=="body" else "",align="CENTER",bold=True,size=1450,color="#777777",line=1650))
        v=reg(l,r,y,y+3) if mode!="body" else reg(l,r,y,y+30)
        if mode=="head":
            title=only(l,r,y,y+3)
            if not title.startswith(card_tags[i]+" "):
                raise ValueError(f"Card title {title!r} does not start with tag {card_tags[i]!r}")
            row.append(cell(i*2,card_width,h,layout.tagged(card_tags[i],title[len(card_tags[i]):].strip(),
                            card_width-300,1400,tag_fill),outline,margin=dict(left=150,right=150)))
            continue
        if mode=="body" and i==0: v[-1]="→ "+v[-1]
        row.append(c(i*2,card_width,h,v,{"head":outline,"body":white,"result":gray2}[mode],
                     bold=mode!="body",align="LEFT" if mode=="body" else "CENTER",
                     size=1080,ratio=80 if mode=="head" else (77 if mode=="result" and i==2 else 87)))
    return row
tab([cards_row(560,1830,"head"),cards_row(578,4320,"body"),cards_row(623,2190,"result")],520)
heading=add_text(only(50,60,647,650),1320,True,line=1680,after=240,ratio=85)
# The 지적사항 tag is a smaller run on the same line, as in the PDF.
tag=layout.sub(heading,"hp:run",charPrIDRef=layout.char(1000,True,"#161616",85))
layout.sub(tag,"hp:t").text="  ■ 지적사항 개선"
tab([[label(0,3000,2150,"현황",gray2),c(1,19400,2150,only(90,95,671,674),white,ratio=87),
      label(2,1450,2150,"▶","1",size=1100),label(3,3000,2150,"개선",dark,color="#FFFFFF"),
      c(4,23050,2150,"① "+only(340,350,671,674)+" ② "+only(460,470,671,674),white,ratio=82)]],380)
left=reg(60,65,715,731)
right_a=reg(310,320,715,731)
tab([[label(0,24750,1800,"① "+only(150,155,696,699),gray2),c(1,400,1800,""),label(2,24750,1800,"② "+only(395,400,696,699),gray2)],
     [c(0,24750,3250,left,white,ratio=80),c(1,400,3250,""),c(2,24750,3250,
       [right_a[0]+" → "+only(475,480,715,718),right_a[1]+" → "+only(430,435,728,730)],white,ratio=78)]],470)
tab([[label(0,5600,5150,"주요성과",dark,color="#FFFFFF",size=1160),
      c(1,44300,5150,reg(115,120,752,785),outline,bold=True,ratio=86,line=1390)]])
add_text("30    한전KDN㈜",1090,True,line=1400,before=1250)

print(layout.write(target))
