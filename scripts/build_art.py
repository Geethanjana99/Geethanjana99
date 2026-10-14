#!/usr/bin/env python3
"""Rebuild the local SVG artwork. Add --animate for GIFs (Pillow + CairoSVG).
No network access is used. Generated assets contain no scripts or external fonts.
"""
from __future__ import annotations
import argparse, html, math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
BG='#080D18'; PANEL='#101929'; LINE='#22344A'; WHITE='#EDF5FF'; MUTED='#93A8C1'; CYAN='#66E3F1'; PURPLE='#AA9AFF'; GREEN='#A0E5B0'

def txt(x,y,s,size=20,color=WHITE,weight=400,mono=False,anchor='start',spacing=None):
    family='Courier New, monospace' if mono else 'Arial, Helvetica, sans-serif'
    a=f' letter-spacing="{spacing}"' if spacing is not None else ''
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{family}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}"{a}>{html.escape(str(s))}</text>'
def rect(x,y,w,h,fill=PANEL,stroke=LINE,r=16,extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" {extra}/>'
def path(d,stroke=CYAN,width=2,fill='none',extra=''):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'
def circle(x,y,r,fill='none',stroke=CYAN,width=1,extra=''):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" {extra}/>'
def line(x1,y1,x2,y2,stroke=LINE,width=1,extra=''):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}" {extra}/>'
def group(body,x=0,y=0,scale=1,extra=''):
    return f'<g transform="translate({x} {y}) scale({scale})" {extra}>{body}</g>'
def shell(w,h,body,title='Geethanjana | Engineering between code and reality'):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(title,quote=True)}">
<title>{html.escape(title)}</title>
<defs>
 <linearGradient id="bg" x2="1" y2="1"><stop stop-color="#101B2E"/><stop offset=".55" stop-color="#080D18"/><stop offset="1" stop-color="#15162B"/></linearGradient>
 <linearGradient id="accent"><stop stop-color="#66E3F1"/><stop offset="1" stop-color="#AA9AFF"/></linearGradient>
 <linearGradient id="body" x2=".3" y2="1"><stop stop-color="#D3E1EF"/><stop offset=".23" stop-color="#8299B3"/><stop offset=".56" stop-color="#344960"/><stop offset="1" stop-color="#18283C"/></linearGradient>
 <linearGradient id="glass" x2=".7" y2="1"><stop stop-color="#173951"/><stop offset=".4" stop-color="#0C1425"/><stop offset="1" stop-color="#252543"/></linearGradient>
 <radialGradient id="lens"><stop stop-color="#0B1730"/><stop offset=".56" stop-color="#172E48"/><stop offset=".8" stop-color="#58ADBD"/><stop offset="1" stop-color="#102138"/></radialGradient>
 <radialGradient id="haze"><stop stop-color="#424981" stop-opacity=".28"/><stop offset="1" stop-color="#15223A" stop-opacity="0"/></radialGradient>
 <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M 40 0 L 0 0 0 40" fill="none" stroke="#7CACC9" stroke-opacity=".07" stroke-width=".7"/></pattern>
</defs>
{rect(.5,.5,w-1,h-1,'url(#bg)',LINE,24)}
{body}
</svg>'''
def save(name,s):
    p=ASSETS/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s,encoding='utf-8'); return p

def icon(kind,color=CYAN):
    # Original line icons, on a 48 x 48 design grid.
    base={
      'code':path('M16 12 L4 24 L16 36 M32 12 L44 24 L32 36 M28 7 L21 41',color,2.5),
      'vr':path('M8 14 Q3 14 3 22 L3 30 Q3 36 9 36 L17 36 L22 30 L26 30 L31 36 L39 36 Q45 36 45 30 L45 22 Q45 14 39 14 Z',color,2.2)+circle(14,25,5,'none',color,2)+circle(34,25,5,'none',color,2)+path('M10 14 L13 8 L35 8 L38 14',color,2),
      'cube':path('M24 3 L43 14 L43 35 L24 46 L5 35 L5 14 Z M5 14 L24 25 L43 14 M24 25 L24 46 M14 9 L34 20',color,2),
      'db':f'<ellipse cx="24" cy="10" rx="17" ry="6" fill="none" stroke="{color}" stroke-width="2"/>'+path('M7 10 L7 36 C7 44 41 44 41 36 L41 10 M7 23 C7 31 41 31 41 23',color,2),
      'cloud':path('M13 35 C0 35 1 18 13 18 C11 3 34 2 35 18 C48 14 51 35 38 35 Z',color,2.2)+path('M17 40 L24 33 L31 40 M24 33 L24 47',color,2),
      'network':path('M24 12 L24 24 M8 34 L8 24 L40 24 L40 34',color,2)+rect(17,1,14,11,'none',color,2)+rect(1,34,14,11,'none',color,2)+rect(17,34,14,11,'none',color,2)+rect(33,34,14,11,'none',color,2)+line(24,24,24,34,color,2),
      'shield':path('M24 3 L41 10 L41 23 Q40 38 24 46 Q8 38 7 23 L7 10 Z M15 24 L22 31 L34 17',color,2),
      'route':path('M8 11 L31 11 Q43 11 43 22 Q43 32 31 32 L18 32',color,2.3)+circle(8,11,5,BG,color,2)+circle(13,32,5,BG,color,2)+path('M28 40 L33 45 L43 34',color,2.3),
      'health':path('M7 23 L17 23 L22 12 L28 36 L34 23 L43 23',color,2.6)+rect(2,3,44,42,'none',color,9),
      'terminal':rect(3,6,42,36,'none',color,5)+path('M11 16 L18 23 L11 30 M23 30 L35 30',color,2.5),
      'layers':path('M24 4 L45 15 L24 26 L3 15 Z M3 24 L24 35 L45 24 M3 33 L24 44 L45 33',color,2),
      'document':path('M10 3 L30 3 L40 13 L40 44 L10 44 Z M30 3 L30 13 L40 13 M17 21 L33 21 M17 28 L29 28 M17 35 L26 35',color,2),
      'graduate':path('M2 17 L24 7 L46 17 L24 28 Z M10 22 L10 33 Q24 42 38 33 L38 22 M45 19 L45 34',color,2),
      'mail':rect(3,8,42,32,'none',color,5)+path('M5 12 L24 27 L43 12',color,2),
      'arrow':path('M9 39 L39 9 M17 9 L39 9 L39 31',color,2.5),
      'react':''.join(f'<ellipse cx="24" cy="24" rx="22" ry="8" fill="none" stroke="{color}" stroke-width="1.7" transform="rotate({r} 24 24)"/>' for r in (0,60,120))+circle(24,24,4,color,color),
      'git':path('M24 2 L46 24 L24 46 L2 24 Z',color,2)+path('M17 12 L31 26 L31 34 M22 17 L22 34',color,2)+circle(17,12,3,color,color)+circle(22,34,3,color,color)+circle(31,34,3,color,color),
      'docker':''.join(rect(x,y,8,8,'none',color,1) for x,y in [(4,20),(14,20),(24,20),(34,20),(14,10),(24,10),(24,0)])+path('M1 32 L42 32 Q36 47 17 44 Q6 43 1 32 Z',color,2),
      'figma':path('M24 24 L24 41 Q9 49 9 35 Q9 27 24 27 M24 24 L24 3 L13 3 Q0 3 10 15 Q0 26 13 26 L24 26 M24 3 L34 3 Q48 3 38 15 L24 15',color,2)+circle(35,24,9,'none',color,2),
    }
    return base.get(kind,txt(24,32,kind,22,color,700,True,'middle'))

def headset(x=0,y=0,s=1):
    b=path('M46 85 C27 -25 260 -33 264 85','#52677C',18)+path('M53 81 C40 -7 248 -18 257 81','#A9BACA',3)
    b+=path('M16 83 C24 62 50 57 85 55 L249 48 C275 51 291 68 294 91 L290 158 C284 184 258 196 230 189 L169 173 Q151 166 138 183 L113 207 L61 207 Q16 200 10 171 Z','none',0,'url(#body)')
    b+=path('M33 89 Q42 72 71 73 L250 65 Q276 71 278 90 L275 144 Q271 170 246 168 L188 153 Q162 145 151 163 L131 183 L65 185 Q35 181 32 161 Z','#6F8B9D',1.2,'url(#glass)')
    b+=f'<ellipse cx="92" cy="128" rx="40" ry="36" fill="url(#lens)" stroke="#70C5CF" stroke-width="1"/><ellipse cx="222" cy="115" rx="39" ry="34" fill="url(#lens)" stroke="#978FC6" stroke-width="1"/>'
    b+=f'<ellipse cx="92" cy="128" rx="24" ry="21" fill="#0A1327" stroke="#407D95"/><ellipse cx="222" cy="115" rx="23" ry="20" fill="#0A1327" stroke="#58629C"/>'
    b+=path('M55 91 Q146 65 254 85','#D2F8FF',2,extra='opacity=".4"')+circle(279,123,3,CYAN,CYAN)+path('M50 201 L71 221 L111 218 L117 205','#41566D',2,'#1A2B40')
    # Detached controller, an original stylised device rather than a product photograph.
    b+=f'<g transform="translate(281 164) rotate(-23)"><ellipse cx="0" cy="0" rx="24" ry="18" fill="none" stroke="#889AAF" stroke-width="7"/>{rect(-13,0,26,66,'url(#body)','#607084',12)}{circle(0,17,6,'#13253C','#789AAD')}{circle(0,40,2,CYAN,CYAN)}</g>'
    return group(b,x,y,s)

def chip(x,y,label,color=CYAN,w=None):
    w=w or max(84,len(label)*8.0+28)
    return rect(x,y,w,31,'#122032',color,7,extra='stroke-opacity=".35"')+txt(x+w/2,y+21,label,12,color,600,True,'middle')

def hero(t=0):
    w,h=1280,560
    b=f'<rect x="650" y="1" width="629" height="558" rx="24" fill="url(#grid)"/>'
    b+=f'<ellipse cx="980" cy="305" rx="310" ry="265" fill="url(#haze)"/>'
    b+=txt(56,53,'G /',24,CYAN,700,True)+txt(118,51,'ENGINEERING BETWEEN CODE & REALITY',12,MUTED,400,True,spacing=1.2)
    b+=txt(1224,51,'FULL STACK  /  XR',12,MUTED,400,True,'end')
    b+=line(56,80,1224,80,LINE)
    b+=txt(54,168,'Hi, I\u2019m',29,MUTED)
    b+=txt(50,252,'Geethanjana.',86,WHITE,700,spacing=-4)
    b+=txt(56,311,'Building software.',32,WHITE,600)+txt(56,353,'Exploring immersive worlds.',32,MUTED,400)
    b+=line(56,390,99,390,CYAN,3)+txt(115,396,'CLEAN ARCHITECTURE. PRACTICAL SOLUTIONS.',12,CYAN,400,True,spacing=.3)
    b+=chip(56,432,'NEXT.JS',w=97)+chip(163,432,'ASP.NET CORE',PURPLE,w=145)+chip(318,432,'UNITY / OPENXR',CYAN,w=158)
    b+=txt(56,515,'FULL-STACK DEVELOPER  /  SOFTWARE ENGINEERING UNDERGRADUATE',11,MUTED,400,True)
    # An orbit behind the immersive hardware.
    b+=f'<ellipse cx="991" cy="284" rx="221" ry="167" fill="none" stroke="#293A57" stroke-width="1" transform="rotate(-23 991 284)"/>'
    b+=f'<ellipse cx="991" cy="284" rx="191" ry="146" fill="none" stroke="#384461" stroke-width="1" stroke-dasharray="3 10" transform="rotate(-23 991 284)"/>'
    for phase in (0,.46,.77):
        a=(t+phase)*math.tau
        b+=circle(991+211*math.cos(a),284+150*math.sin(a),3.3,CYAN if phase==0 else PURPLE,'none')
    # Developer terminal floating above the hardware.
    bb=rect(0,0,190,108,'#121E32','#3B5677',10)+line(0,25,190,25,'#34445B')
    bb+=txt(14,17,'workspace.ts',9,MUTED,400,True)
    bb+=txt(15,49,'const build = () => {',10,PURPLE,400,True)+txt(26,67,'return experience;',10,CYAN,400,True)+txt(15,85,'};',10,MUTED,400,True)
    bb+=rect(32,76,6,10,CYAN,'none',0,extra=f'opacity="{.6+.3*math.sin(t*math.tau)}"')
    b+=group(bb,1032,114,.92,extra='opacity=".95"')
    b+=headset(795,208+5*math.sin(t*math.tau),1.09)
    b+=group(icon('cube',PURPLE),797,127,1.05)
    b+=group(icon('code',CYAN),1142,417,.95)
    b+=chip(838,466,'VIRTUAL REALITY',CYAN,155)+txt(1007,487,'x',15,MUTED,400,True)+chip(1028,466,'SOFTWARE',PURPLE,125)
    return shell(w,h,b,'Geethanjana. Full-stack developer and virtual reality researcher. Building software. Exploring immersive worlds.')

def console():
    w,h=1120,340
    b=txt(37,37,'developer.config.ts',13,MUTED,400,True)+txt(1082,37,'PERSONAL CONFIGURATION',11,MUTED,400,True,'end')+line(1,59,1119,59)
    rows=[('01','const developer = {'),('02','  name: "Geethanjana",'),('03','  role: "Full-Stack Developer",'),('04','  workplace: "Cogent Solutions",'),('05','  focus: ["web", "backend", "cloud", "VR"],'),('06','  approach: "practical, maintainable, human-centred"'),('07','};')]
    for i,(n,s) in enumerate(rows):
        y=102+i*31
        b+=txt(36,y,n,14,'#536A84',400,True)+txt(80,y,s,17,CYAN if i in (1,3,4) else WHITE,400,True)
    b+=group(icon('layers',CYAN),929,106,1.65)+txt(970,225,'CLARITY',11,MUTED,400,True,'middle',2)+txt(970,247,'BY DESIGN',11,MUTED,400,True,'middle',2)
    return shell(w,h,b,'Developer configuration: Geethanjana, Full-Stack Developer at Cogent Solutions, focused on web, backend, cloud, and VR.')

def section(num,label,statement,kind='code',color=CYAN):
    b=txt(30,43,num,22,color,600,True)+line(77,21,77,59,LINE)+txt(99,35,label.upper(),11,MUTED,400,True,spacing=1.8)+txt(99,62,statement,25,WHITE,600)
    b+=group(icon(kind,color),1044,22,.85)
    return shell(1120,85,b,f'{label}: {statement}')

STACKS=[
 ('frontend','FRONTEND','Interfaces that bring products to life.',CYAN,[('Next.js','N'),('React','react'),('TypeScript','TS'),('JavaScript','JS'),('HTML5','</>'),('CSS3','CSS'),('Tailwind','~')]),
 ('backend','BACKEND','The systems behind the experience.',PURPLE,[('Python','Py'),('PHP','php'),('Node.js','node'),('Express','ex'),('ASP.NET Core','.NET')]),
 ('data','DATABASES','Structured data. Connected applications.',GREEN,[('MySQL','db'),('MongoDB','db'),('Firebase','F'),('Supabase','S'),('PostgreSQL','db')]),
 ('tooling','CLOUD / DEVOPS / TOOLS','From local development to delivery.',CYAN,[('Azure','cloud'),('Docker','docker'),('Git','git'),('GitHub','GH'),('Postman','>_'),('Figma','figma'),('VS Code','code')]),
 ('xr','IMMERSIVE TECHNOLOGY','Software beyond the screen.',PURPLE,[('Unity','cube'),('OpenXR','vr'),('SteamVR','vr'),('REST APIs','network'),('JWT','shield'),('WebSockets','route')]),
]
def stack_board(name,title,subtitle,color,items):
    b=txt(31,36,title,12,color,600,True,spacing=1.6)+txt(31,67,subtitle,22,WHITE,500)
    count=len(items); gap=17; tw=(1120-62-gap*(count-1))/count; start=31
    for i,(label,kind) in enumerate(items):
        x=start+i*(tw+gap)
        b+=rect(x,97,tw,121,'#111D2E',LINE,12)
        b+=group(icon(kind,color),x+(tw-42)/2,113,.88)
        b+=txt(x+tw/2,197,label,14,WHITE,500,False,'middle')
    return shell(1120,243,b,f'{title}: '+', '.join(n for n,k in items))

def project(name,num,caption,focus,kind,color):
    b=f'<rect x="734" y="1" width="385" height="265" rx="24" fill="url(#grid)"/>'
    b+=txt(34,40,f'SELECTED WORK / {num}',11,color,400,True,spacing=1.3)+txt(30,103,name,53,WHITE,700,spacing=-1.5)
    b+=txt(34,141,caption,21,MUTED,400)+txt(34,217,focus,12,color,500,True)
    # Each project gets distinct conceptual product art, not a purported screenshot.
    if kind=='document':
        b+=group(icon('document',color),874,64,2.1)
        b+=rect(806,69,97,46,'#15283D','#36556E',8)+txt(854,98,'PDF',20,color,700,True,'middle')
        b+=path('M899 159 C929 148 922 189 946 178 S963 151 980 164',PURPLE,3)
        b+=group(icon('shield',color),975,143,1.3)
        b+=path('M841 130 L841 203 L907 203',color,1.3,extra='stroke-dasharray="4 6"')
    elif kind=='route':
        b+=rect(887,27,129,215,'#172A3D','#536982',19)+rect(895,39,113,190,'#0B1424','#263D54',13)
        b+=path('M913 181 L951 181 L951 115 L985 115',color,3)+circle(913,181,6,BG,color,2)+circle(985,115,6,BG,color,2)
        b+=path('M906 73 L994 73 M906 104 L994 104 M922 63 L922 213 M975 63 L975 213',LINE,1)
        b+=rect(802,118,117,49,'#153044','#305E72',9)+txt(860,148,'WAYPOINT',12,color,600,True,'middle')
        b+=group(icon('route',color),1021,154,1.2)
        b+=line(928,49,973,49,'#819DB5',3)
    else:
        b+=circle(945,133,91,'#101F30','#2B4A55')+circle(945,133,66,'#10272D','#497B72')
        b+=group(icon('health',color),909,96,1.5)
        for x,y,k in [(805,48,'shield'),(1027,50,'db'),(1033,178,'network')]:
            b+=line(x+20,y+20,945,133,'#355F5B',1,extra='stroke-dasharray="3 5"')+rect(x-8,y-8,62,62,'#112329','#35554E',12)+group(icon(k,color),x,y,.96)
    return shell(1120,268,b,f'{name}: {caption}. {focus}. Conceptual project illustration.')

def vr_lab(t=0):
    b=f'<rect x="1" y="1" width="1118" height="409" rx="24" fill="url(#grid)"/>'
    b+=txt(33,42,'RESEARCH / IMMERSIVE NETWORKING',12,PURPLE,600,True,spacing=1.2)
    b+=txt(30,100,'A different way',40,WHITE,700)+txt(30,148,'to experience networks.',40,WHITE,700)
    b+=txt(33,192,'Interactive simulations. Tangible concepts.',17,MUTED)
    b+=txt(33,220,'A research focus on learning through VR.',17,MUTED)
    b+=chip(33,265,'UNITY',PURPLE,94)+chip(137,265,'OPENXR',CYAN,94)+chip(241,265,'STEAMVR',PURPLE,106)
    b+=txt(33,366,'EXPLORE   /   INTERACT   /   EVALUATE',12,CYAN,400,True,spacing=1)
    b+=headset(693,111+4*math.sin(t*math.tau),.96)
    nodes=[(640,60,'terminal'),(1010,68,'network'),(1024,292,'db')]
    for i,(x,y,k) in enumerate(nodes):
        ex,ey=831,238
        b+=line(x+25,y+25,ex,ey,'#39536C',1.3,extra='stroke-dasharray="3 7"')
        p=(t+i*.31)%1
        b+=circle((x+25)*(1-p)+ex*p,(y+25)*(1-p)+ey*p,3.5,CYAN if i%2==0 else PURPLE,'none')
        b+=rect(x-8,y-8,65,65,'#112137','#39516C',12)+group(icon(k,CYAN if i%2==0 else PURPLE),x,y,1)
    b+=txt(754,371,'VIRTUAL REALITY LAB',11,MUTED,400,True,spacing=2)
    return shell(1120,410,b,'Virtual reality research lab. Unity, OpenXR and SteamVR support interactive computer-networking simulations. Decorative network packets animate between devices and a headset.')

def academic():
    b=group(icon('graduate',CYAN),32,32,1.25)+txt(111,50,'UVA WELLASSA UNIVERSITY',14,CYAN,600,True,spacing=1)+txt(111,78,'BSc (Hons) in Industrial Information Technology',20,WHITE,500)
    b+=line(32,108,1088,108)
    b+=txt(33,200,'3.86',69,WHITE,700)+txt(36,230,'GPA',11,MUTED,600,True,spacing=2)
    b+=line(257,139,257,240)
    b+=txt(300,165,'BEST OVERALL',16,CYAN,600,True,spacing=1)+txt(300,197,'PERFORMANCE',24,WHITE,700)+txt(300,230,'Award recipient',15,MUTED)
    b+=line(622,139,622,240)
    b+=txt(666,165,"DEAN'S LIST",16,PURPLE,600,True,spacing=1)+txt(666,197,'2023 / 2024 / 2025',25,WHITE,700)+txt(666,230,'Academic excellence',15,MUTED)
    b+=txt(1087,44,'2022 - 2026',13,MUTED,400,True,'end')
    return shell(1120,270,b,'Uva Wellassa University of Sri Lanka. BSc (Hons) in Industrial Information Technology, 2022-2026. GPA 3.86. Best Overall Performance. Dean\u2019s List 2023, 2024 and 2025.')

def principles():
    b=''
    for i,(kind,title,ls,col) in enumerate([
      ('layers','CLARITY FIRST',['Clean architecture.','Readable, maintainable code.'],CYAN),
      ('network','SYSTEMS THAT CONNECT',['Thoughtful APIs.','Reliable data interactions.'],PURPLE),
      ('vr','EXPERIENCES THAT MATTER',['Practical software.','Curiosity beyond the screen.'],GREEN)]):
        x=31+i*365
        if i: b+=line(x-18,34,x-18,216)
        b+=group(icon(kind,col),x,30,1)+txt(x,113,title,13,col,600,True,spacing=.5)
        b+=txt(x,151,ls[0],18,WHITE)+txt(x,181,ls[1],17,MUTED)
    return shell(1120,247,b,'Engineering principles: clarity first, connected systems, and experiences that matter.')

def github_placeholder():
    b=group(icon('code',CYAN),44,46,1.45)+txt(143,62,'THE CODE CONTINUES HERE',13,CYAN,600,True,spacing=1.3)
    b+=txt(143,110,'Explore the repositories.',35,WHITE,700)+txt(143,153,'Projects, experiments, and the next idea worth building.',18,MUTED)
    b+=txt(44,221,'github.com / Geethanjana99',14,PURPLE,400,True)+group(icon('arrow',CYAN),1010,82,1.2)
    return shell(1120,256,b,'Explore Geethanjana99 on GitHub. This is a navigation card, not a generated statistics snapshot.')

def footer():
    b=f'<rect x="1" y="1" width="1118" height="225" rx="24" fill="url(#grid)"/>'
    b+=txt(560,68,'ALWAYS BUILDING. ALWAYS LEARNING.',12,CYAN,600,True,'middle',2)
    b+=txt(560,121,'Code. Build. Learn. Improve.',38,WHITE,700,False,'middle',-1)
    b+=txt(560,166,'Turning real-world problems into practical software.',17,MUTED,400,False,'middle')
    b+=line(410,195,710,195,'url(#accent)',2)
    return shell(1120,228,b,'Code. Build. Learn. Improve. Turning real-world problems into practical software.')

def button(label,kind='arrow',color=CYAN,w=178):
    b=group(icon(kind,color),17,13,.50)+txt(54,32,label,15,WHITE,600)+path(f'M{w-24} 27 L{w-16} 19 M{w-23} 19 L{w-16} 19 L{w-16} 26',color,1.5)
    return shell(w,50,b,label)

def gif(frames,out,w):
    import io
    import cairosvg
    from PIL import Image
    rgba=[Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode(),output_width=w))).convert('RGBA') for s in frames]
    imgs=[]
    for im in rgba:
        backdrop=Image.new('RGBA',im.size,'#0d1117')
        backdrop.alpha_composite(im)
        imgs.append(backdrop.convert('RGB'))
    # One palette across the loop avoids colour flicker; index 255 is reserved
    # for transparent rounded corners so the GIF also sits cleanly on light UI.
    palette=imgs[0].quantize(colors=192)
    pal=[]
    for im,source in zip(imgs,rgba):
        frame=im.quantize(palette=palette,dither=Image.Dither.NONE)
        colours=frame.getpalette()
        colours=(colours+[0]*768)[:768]
        frame.putpalette(colours)
        mask=source.getchannel('A').point(lambda a: 255 if a<128 else 0)
        frame.paste(255,mask=mask)
        pal.append(frame)
    pal[0].save(out,save_all=True,append_images=pal[1:],duration=100,loop=0,optimize=False,disposal=1,transparency=255)


def main():
    p=argparse.ArgumentParser(); p.add_argument('--animate',action='store_true'); args=p.parse_args()
    save('hero.svg',hero()); save('developer-console.svg',console())
    for a in STACKS: save(f'stack-{a[0]}.svg',stack_board(*a))
    sections=[('01','About','Full-stack thinking. Human-centred outcomes.','layers'),('02','Experience','Working across the full product lifecycle.','terminal'),('03','Technology','The tools behind the work.','code'),('04','Selected projects','Real problems. Purpose-built software.','cube'),('05','VR research','Making the abstract feel tangible.','vr'),('06','Education','Academic foundations. Continuous growth.','graduate'),('07','Beyond development','Learning, leadership, and collaboration.','network'),('08','GitHub','An evolving collection of ideas.','code'),('09','Connect','Let\u2019s talk software and immersive experiences.','mail')]
    for n,l,s,k in sections: save(f'sections/{n}.svg',section(n,l,s,k,PURPLE if n in ('05','07') else CYAN))
    save('project-truemarke.svg',project('TrueMarke','01','Enterprise electronic signature platform','DOCUMENT WORKFLOWS  /  AUDITABILITY  /  ADMINISTRATION','document',CYAN))
    save('project-waypoint.svg',project('WayPoint','02','Cross-platform shuttle management','PASSENGERS  /  DRIVERS  /  LIVE OPERATIONS','route',PURPLE))
    save('project-caresync.svg',project('CareSync','03','Connected healthcare support','RESPONSIVE INTERFACES  /  AUTHENTICATION  /  REAL-TIME DATA','health',GREEN))
    save('vr-lab.svg',vr_lab()); save('academic.svg',academic()); save('principles.svg',principles()); save('footer.svg',footer())
    # Do not overwrite a generated statistics snapshot when refreshing artwork.
    if not (ASSETS/'github-activity.svg').exists(): save('github-activity.svg',github_placeholder())
    for name,label,k,col in [('portfolio','Portfolio','arrow',CYAN),('linkedin','LinkedIn','in',PURPLE),('email','Email me','mail',CYAN),('github','Repositories','code',PURPLE)]: save(f'link-{name}.svg',button(label,k,col))
    for k in ['vr','cube','network','code','cloud','shield','terminal','route','health','document','layers','graduate','react','docker','git','mail']:
        save(f'icons/{k}.svg',shell(72,72,group(icon(k),12,12),k+' icon'))
    build_mobile()
    if args.animate:
        gif([hero(i/40) for i in range(40)],ASSETS/'hero.gif',1280)
        gif([vr_lab(i/40) for i in range(40)],ASSETS/'vr-lab.gif',1120)
    print('Artwork ready in',ASSETS)


def build_mobile():
    import textwrap
    b=txt(35,44,'G / ENGINEERING BETWEEN CODE & REALITY',12,CYAN,500,True)
    b+=line(35,70,605,70)+txt(35,123,'Hi, I\u2019m',26,MUTED)+txt(31,193,'Geethanjana.',65,WHITE,700,spacing=-3)
    b+=txt(35,249,'Building software.',30,WHITE,600)+txt(35,289,'Exploring immersive worlds.',29,MUTED)
    b+=txt(35,337,'FULL-STACK DEVELOPMENT / VR RESEARCH',12,CYAN,500,True)
    b+=f'<ellipse cx="338" cy="532" rx="235" ry="158" fill="url(#haze)" stroke="#293A57"/>'
    b+=headset(143,421,1.1)+group(icon('cube',PURPLE),55,431,1.1)+group(icon('code',CYAN),519,617,1)
    b+=chip(35,713,'NEXT.JS',w=98)+chip(143,713,'ASP.NET CORE',PURPLE,148)+chip(301,713,'UNITY / OPENXR',CYAN,167)
    b+=txt(35,785,'CLEAN ARCHITECTURE. PRACTICAL SOLUTIONS.',12,MUTED,400,True)
    save('mobile/hero.svg',shell(640,815,b,'Geethanjana. Full-stack developer and VR researcher.'))
    for name,title,sub,col,items in STACKS:
        rows=math.ceil(len(items)/2); h=100+rows*136+22
        b=txt(28,35,title,13,col,600,True)+txt(28,70,sub,22,WHITE,500)
        for i,(label,kind) in enumerate(items):
            x=28+(i%2)*300; y=101+(i//2)*136
            b+=rect(x,y,284,119,'#111D2E',LINE,12)+group(icon(kind,col),x+23,y+31,1.1)+txt(x+91,y+70,label,22,WHITE,500)
        save(f'mobile/stack-{name}.svg',shell(640,h,b,title+': '+', '.join(n for n,k in items)))
    for n,f in enumerate(sorted((ASSETS/'sections').glob('*.svg')),1):
        # Read the original accessible title instead of maintaining duplicate copy.
        import xml.etree.ElementTree as ET
        title=ET.fromstring(f.read_text()).find('{http://www.w3.org/2000/svg}title').text
        label,statement=title.split(': ',1)
        b=txt(27,55,f'{n:02}',25,CYAN,700,True)+line(76,23,76,102)
        b+=txt(99,31,label.upper(),13,MUTED,500,True)
        for j,t in enumerate(textwrap.wrap(statement,36)):
            b+=txt(99,66+j*30,t,25,WHITE,600)
        save(f'mobile/section-{n:02}.svg',shell(640,127,b,title))
    b=txt(28,41,'RESEARCH / IMMERSIVE NETWORKING',13,PURPLE,600,True)
    b+=txt(27,98,'A different way',40,WHITE,700)+txt(27,150,'to experience networks.',40,WHITE,700)
    b+=txt(28,195,'Interactive simulations. Tangible concepts.',22,MUTED)
    b+=headset(127,301,1.15)
    b+=group(icon('network',CYAN),530,263,1)+group(icon('terminal',PURPLE),47,280,1)+group(icon('db',CYAN),49,521,1)
    b+=line(85,310,190,359,'#40566E',1,extra='stroke-dasharray="3 6"')+line(496,384,550,316,'#40566E',1,extra='stroke-dasharray="3 6"')
    b+=chip(29,607,'UNITY',PURPLE,101)+chip(142,607,'OPENXR',CYAN,112)+chip(266,607,'STEAMVR',PURPLE,119)
    b+=txt(29,680,'EXPLORE / INTERACT / EVALUATE',14,MUTED,400,True)
    save('mobile/vr-lab.svg',shell(640,713,b,'Virtual reality for computer networking education. Unity, OpenXR, SteamVR.'))
    b=txt(28,36,'developer.config.ts',15,MUTED,400,True)+line(1,59,639,59)
    ls=['const developer = {','  name: "Geethanjana",','  role: "Full-Stack Developer",','  workplace: "Cogent Solutions",','  focus: ["web", "backend",','          "cloud", "VR"],','  approach: "practical & maintainable"','};']
    for i,t in enumerate(ls): b+=txt(28,105+i*34,t,22,CYAN if i in (1,3,4,5) else WHITE,400,True)
    save('mobile/developer-console.svg',shell(640,383,b,'Developer configuration: Geethanjana; Cogent Solutions; web, backend, cloud and VR.'))
    b=txt(27,43,'UVA WELLASSA UNIVERSITY',18,CYAN,600,True)+txt(27,80,'BSc (Hons) in Industrial Information Technology',21,WHITE)
    b+=txt(27,118,'2022 - 2026',18,MUTED)+line(27,144,612,144)
    b+=txt(26,237,'3.86',77,WHITE,700)+txt(212,233,'GPA',17,MUTED,600,True)
    b+=line(27,273,612,273)+txt(27,316,'BEST OVERALL PERFORMANCE',23,CYAN,600,True)+txt(27,351,'Award recipient',21,MUTED)
    b+=line(27,384,612,384)+txt(27,425,"DEAN'S LIST",23,PURPLE,600,True)+txt(27,461,'2023 / 2024 / 2025',26,WHITE,600)
    save('mobile/academic.svg',shell(640,492,b,'GPA 3.86. Best Overall Performance. Dean\u2019s List 2023, 2024, 2025.'))
    b=''
    for i,(k,title,a,z,c) in enumerate([('layers','CLARITY FIRST','Clean architecture.','Readable, maintainable code.',CYAN),('network','SYSTEMS THAT CONNECT','Thoughtful APIs.','Reliable data interactions.',PURPLE),('vr','EXPERIENCES THAT MATTER','Practical software.','Curiosity beyond the screen.',GREEN)]):
        y=i*172
        if i:b+=line(28,y,612,y)
        b+=group(icon(k,c),30,y+36,1.1)+txt(113,y+48,title,18,c,600,True)+txt(113,y+86,a,23,WHITE)+txt(113,y+122,z,22,MUTED)
    save('mobile/principles.svg',shell(640,525,b,'Clarity first. Systems that connect. Experiences that matter.'))

if __name__=='__main__': main()
