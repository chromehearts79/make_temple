"""Rebuild KDN's physical PDF page 51 from the user's original PDF."""

from hwpx_layout import Layout, cell
from pdf_coords import recipe_inputs

source, target = recipe_inputs(51, '인턴운영 체계 확립')
layout = Layout(top=3100)
add_text, add_table, border = layout.add_text, layout.add_table, layout.border
p, center = layout.p, layout.center
reg, only = source.region, source.only

def c(i,w,h,v,fill="1",*,bold=False,align="LEFT",size=1080,ratio=90,color="#161616",span=1,cols=1,line=1250):
    if isinstance(v,str): v=[v]
    return cell(i,w,h,[p(t,size,bold,color,align=align,line=line,ratio=ratio) for t in v],fill,span,cols)

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

add_table([[label(0,3350,1680,"01",dark,color="#FFFFFF",size=1380)],
           [label(0,3350,5960,list("경영관리"),gray2,size=950,line=1160)]],floating=(57800,15000))
tab([[c(0,30700,1680,"",border(bottom="soft")),c(1,19200,1680,only(380,385,36,39),align="RIGHT",ratio=90)]],1800)
def section_heading(n,y,tag=""):
    tab([[label(0,2850,2220,str(n),dark,color="#FFFFFF",size=1720,line=1850),
          c(1,47050,2220,only(90,100,y,y+3)+tag,gray,bold=True,size=1480,ratio=86,line=1800)]],560)
section_heading(3,74,"  ■ 지적사항 개선")
for j,(head,body_y,res) in enumerate([(104,120,157),(183,202,235)]):
    a,b,d=1840,3220,2060
    top=[]; body=[]; result=[]
    for k,xs in enumerate(((60,73,110,145,305),(313,325,370,380,558))):
        x0,x1,x2,x3,x4=xs
        i=k*3
        if k:
            for row,h in ((top,a),(body,b),(result,d)):row.append(c(2,500,h,""))
        top.extend([label(i,6900,a,f"{'①②③④'[2*j+k]} "+only(x1,x2,head,head+3),dark,color="#FFFFFF",size=1050),
                    label(i+1,17800,a,only(x3,x4,head-0.5,head+2),gray2,size=1100,ratio=86)])
        body.append(c(i,24700,b,reg(x0,x4,body_y,body_y+19),outline,cols=2,ratio=80))
        result.append(label(i,24700,d,only(x0,x4,res,res+3),gray2,cols=2,ratio=77 if k else 92))
    tab([top,body,result],470 if j==0 else 1190)
section_heading(4,272)
add_text(only(55,60,297,300)+"  ■ Best Practice",1400,True,line=1750,ratio=88,after=240)
ws=[2820,18730,18730,9620]
heads=reg(55,555,321,325)
fair=[[label(i,w,1800,t,dark if i==3 else gray2,color="#FFFFFF" if i==3 else "#161616") for i,(w,t) in enumerate(zip(ws,heads))]]
for j,(y0,y1,h,sy0,sy1) in enumerate([(339,391,5530,0,0),(395,422,3000,395,420),(426,464,4190,425,461)]):
    row=[label(0,ws[0],h,reg(60,65,y0,y1),gray,size=1070),
         c(1,ws[1],h,reg(85,270,y0,y1),grid,ratio=75),
         c(2,ws[2],h,reg(275,295,y0,y1),grid,ratio=70 if j==2 else 75)]
    if j==0:
        chart=[
            p("서류전형 블라인드 위배 건수",810,True,align="CENTER",line=1020,ratio=76),
            p("’24년 ━━━━ 152건",850,align="CENTER",line=1050,ratio=86),
            p("’25년 ━ 8건",850,align="CENTER",line=1050,ratio=86),
            p("▼ 144건 감소",1040,True,align="CENTER",line=1290)]
        row.append(cell(3,ws[3],h,chart,outline,1,1))
    else: row.append(c(3,ws[3],h,reg(460,480,sy0,sy1),outline,align="CENTER",ratio=83,size=1060))
    fair.append(row)
tab(fair,620)
add_text(only(55,60,472,476),1400,True,line=1750,after=260)
survey=[
    [label(0,4250,3940,["多채널","의견수렴"],gray,span=2),
     label(1,9850,1850,only(105,110,497,500),gray2),label(2,1500,3940,"+", "1",span=2),
     label(3,9050,1850,only(225,230,497,500),gray2),label(4,1500,3940,"▶","1",span=2),
     label(5,23750,1850,only(400,420,497,500),gray2)],
    [c(1,9850,2090,only(120,125,516,519),white,align="CENTER"),
     c(3,9050,2090,only(220,230,516,519),white,align="CENTER"),
     c(5,23750,2090,"  ".join(f"{n} {t}" for n,t in zip("①②",reg(340,470,515,517))),white,align="CENTER",ratio=78)]]
tab(survey,550)
a,b,d,e=1850,5810,30850,11390
h1,h2,h3=2980,3000,4680
empathy=[
    [label(0,a+b,1800,"구분",gray2,cols=2),label(2,d,1800,"추진노력",gray2),label(3,e,1800,"추진성과",dark,color="#FFFFFF")],
    [label(0,a,h1+h2,"①",gray,span=2),label(1,b,h1,"절차 간소화",gray,ratio=85),
     c(2,d,h1,[only(79,81,560,563).split("∙",1)[1].join(["∙",""]),
                "→ "+only(150,160,574,576)],grid,ratio=85),
     c(3,e,h1,reg(449,461,560,576),outline,align="CENTER")],
    [label(1,b,h2,reg(80,97,590,606),gray),
     c(2,d,h2,reg(135,145,590,606),grid,ratio=80),
     c(3,e,h2,reg(450,470,591,607),outline,align="CENTER")],
    [label(0,a,h3,"②",gray),label(1,b,h3,reg(79,92,628,645),gray,ratio=89),
     c(2,d,h3,[only(135,140,621,623)+" → "+only(222,225,621,623),
                only(135,140,635,638)+" → "+only(234,238,635,638),only(135,140,650,652)],grid,ratio=80),
     c(3,e,h3,["평가 영역별 수준","직무 적합성 탁월 · 조직 적합성 우수",
                "의사소통 양호 · 자기소개 양호"],outline,align="CENTER",size=840,ratio=71,line=1170)]]
tab(empathy,650)
add_text(only(55,60,672,675),1400,True,line=1750,ratio=84,after=270)
tab([[label(0,24750,1970,"① "+only(130,135,699,701),outline),c(1,400,1970,""),label(2,24750,1970,"② "+only(385,390,699,701),outline)],
     [c(0,24750,3380,[only(60,65,718,720),only(60,65,732,735)+" → "+only(240,242,732,735)],white,ratio=81),
      c(1,400,3380,""),c(2,24750,3380,[only(312,315,718,720)+" → "+only(444,445,718,720),
       only(312,315,732,735)+" → "+only(409,411,732,735)],white,ratio=79)],
     [label(0,24750,2080,only(70,71,752,755),gray2,ratio=86),c(1,400,2080,""),label(2,24750,2080,only(313,315,752,755),gray2,ratio=82)]],490)
tab([[label(0,5550,2350,"주요성과",dark,color="#FFFFFF"),c(1,44350,2350,only(115,120,784,786),outline,bold=True,ratio=84)]])
add_text("2025년도 경영실적보고서   31",920,align="RIGHT",line=1300,before=1220)

print(layout.write(target))
