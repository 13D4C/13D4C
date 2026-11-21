"""Render the profile's native graphic layouts and looped mascot components.

The original generated illustration is retained unchanged. Motion comes from
positioning that illustration in the layout, with animated vector-like accents.
"""

from pathlib import Path
from functools import lru_cache
from html import escape
import json
import math
import os
from PIL import Image, ImageDraw, ImageFont, ImageChops

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'profile'
DATA = json.loads((ROOT / 'profile.json').read_text())
OUT.mkdir(parents=True, exist_ok=True)
BG = '#071b25'
PANEL = '#0d2836'
LINE = '#254c60'
WHITE = '#f4fbff'
MUTED = '#b0c8d3'
CYAN = '#68dce8'
GO = '#00add8'
GOLD = '#ffd166'
SOURCE = Image.open(OUT / 'gopher-duck.png').convert('RGBA')


@lru_cache(maxsize=None)
def font(size, style='sans'):
    filenames = {'sans': 'DejaVuSans.ttf', 'bold': 'DejaVuSans-Bold.ttf',
                 'serif': 'DejaVuSerif.ttf', 'mono': 'DejaVuSansMono.ttf'}
    candidates = [Path(os.environ.get('PROFILE_FONT_DIR', '.')) / filenames[style],
                  Path('/usr/share/fonts/truetype/dejavu') / filenames[style]]
    windows = {'sans': 'arial.ttf', 'bold': 'arialbd.ttf', 'serif': 'georgia.ttf', 'mono': 'consola.ttf'}
    candidates.append(Path('C:/Windows/Fonts') / windows[style])
    for candidate in candidates:
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default(size=size)


def txt(im, x, y, value, size=24, color=WHITE, style='sans'):
    ImageDraw.Draw(im).text((round(x), round(y)), str(value), font=font(size, style), fill=color)


def wrap(value, width, size=24, style='sans'):
    result = []
    for paragraph in value.split('\n'):
        line = ''
        for word in paragraph.split():
            candidate = (line + ' ' + word).strip()
            if line and font(size, style).getlength(candidate) > width:
                result.append(line)
                line = word
            else:
                line = candidate
        result.append(line)
    return result


def para(im, x, y, value, width, size=24, color=MUTED, leading=None, style='sans'):
    leading = leading or round(size * 1.48)
    for line in wrap(value, width, size, style):
        txt(im, x, y, line, size, color, style)
        y += leading
    return y


def box(im, xy, fill=PANEL, radius=18, outline=LINE):
    ImageDraw.Draw(im).rounded_rectangle(xy, radius, fill=fill, outline=outline, width=1)


def rule(im, x, y, w):
    ImageDraw.Draw(im).line((x, y, x + w, y), fill=LINE, width=1)


def canvas(w, h):
    im = Image.new('RGBA', (w, h), BG)
    d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / h
        d.line((0, y, w, y), fill=(round(10-3*t), round(37-10*t), round(50-13*t)))
    for x in range(0, w, 36):
        d.line((x, 0, x, h), fill='#0c2c39')
    for y in range(0, h, 36):
        d.line((0, y, w, y), fill='#0c2c39')
    return im


def rounded(im):
    mask = Image.new('L', im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, im.width-1, im.height-1), 24, fill=255)
    im.putalpha(mask)
    ImageDraw.Draw(im).rounded_rectangle((0, 0, im.width-1, im.height-1), 24, outline=LINE, width=2)
    return im


@lru_cache(maxsize=12)
def mascot(size):
    return SOURCE.resize((size, size), Image.Resampling.LANCZOS)


def stamp(im, x, y, size):
    im.alpha_composite(mascot(size), (round(x), round(y)))


def header(im, number, title, caption, mobile=False):
    p = 36 if mobile else 56
    txt(im, p, 30, f'{number} / {caption}', 17, CYAN, 'mono')
    txt(im, p, 72, title, 35 if mobile else 44, WHITE, 'serif')
    stamp(im, im.width-(112 if mobile else 166), -12 if mobile else -18, 108 if mobile else 156)


def orbit(im, cx, cy, radius, phase=0):
    d = ImageDraw.Draw(im)
    d.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), outline='#1c6078', width=1)
    d.ellipse((cx-radius-25, cy-radius*.45, cx+radius+25, cy+radius*.45), outline='#1c6078', width=1)
    for offset, color in [(0, CYAN), (2.4, GOLD), (4.5, GO)]:
        angle = phase * math.tau + offset
        x = cx + math.cos(angle) * radius
        y = cy + math.sin(angle) * radius
        d.ellipse((x-4, y-4, x+4, y+4), fill=color)


def hero(mobile=False, phase=0):
    w, h = (640, 886) if mobile else (1200, 500)
    im = canvas(w, h)
    p = 36 if mobile else 56
    txt(im, p, 30, '13D4C / GO GOPHER × DUCK OF IT', 17, CYAN, 'mono')
    txt(im, p, 80, 'Atibodee', 59 if mobile else 76, WHITE, 'serif')
    txt(im, p, 152 if mobile else 169, 'Kuiprasert.', 59 if mobile else 76, WHITE, 'serif')
    txt(im, p, 232 if mobile else 270, DATA['tagline'], 35 if mobile else 38, GOLD, 'serif')
    txt(im, p, 287 if mobile else 328, 'Web. Cloud. Networks. AI.', 24, MUTED)
    dy = math.sin(phase * math.tau) * 7
    if mobile:
        orbit(im, 320, 556, 212, phase)
        stamp(im, 25, 255+dy, 590)
        rule(im, p, 779, 568)
        txt(im, p, 808, 'IT STUDENT @ KMITL', 21, CYAN, 'mono')
        txt(im, p, 848, 'Curious by nature. Adaptable by choice.', 21, MUTED)
    else:
        orbit(im, 947, 243, 188, phase)
        stamp(im, 689, -20+dy, 520)
        rule(im, p, 389, 596)
        txt(im, p, 420, 'IT STUDENT @ KMITL', 20, CYAN, 'mono')
        txt(im, 799, 449, 'GO GOPHER × DUCK', 17, CYAN, 'mono')
    return rounded(im)


def about(mobile=False):
    w, h = (640, 540) if mobile else (1200, 405)
    im = canvas(w, h)
    header(im, '00', 'Curious by nature.', 'ABOUT ME', mobile)
    if mobile:
        end = para(im, 36, 150, DATA['introduction'], 568, 25, WHITE, 37)
        rule(im, 36, end+18, 568)
        txt(im, 36, end+43, 'Thailand · IT KMITL', 23, CYAN, 'mono')
    else:
        rule(im, 56, 145, 1088)
        txt(im, 56, 177, 'A little of', 41, WHITE, 'serif')
        txt(im, 56, 232, 'everything.', 41, GOLD, 'serif')
        txt(im, 56, 315, 'Thailand · IT KMITL', 21, CYAN, 'mono')
        para(im, 498, 176, DATA['introduction'], 632, 24, WHITE, 36)
    return rounded(im)


def projects(mobile=False):
    w = 640 if mobile else 1200
    h = 1528 if mobile else 894
    im = canvas(w, h)
    header(im, '01', 'Built. Shipped. Shared.', 'WORK & CONTRIBUTIONS', mobile)
    cards = DATA['work'] + [{'name':'Teaching Assistant', 'category':'TEACHING & COMMUNITY',
        'role':'IT KMITL', 'description':'Computer Networks\nObject-Oriented Programming\nData Structures & Algorithms',
        'highlights':['Knowledge sharing', 'Student support']}]
    for i, item in enumerate(cards):
        x = 36 if mobile else 56+(i%2)*556
        y = 150+i*336 if mobile else 156+(i//2)*350
        cw, ch = (568, 314) if mobile else (532, 326)
        box(im, (x,y,x+cw,y+ch))
        txt(im, x+24, y+24, item['category'], 16, CYAN, 'mono')
        txt(im, x+24, y+57, item['name'], 26 if mobile else 25, WHITE, 'bold')
        role_end = para(im, x+24, y+102, item['role'], cw-48, 18, GOLD, 25)
        para(im, x+24, role_end+18, item['description'], cw-48, 22 if mobile else 21, MUTED, 31)
        txt(im, x+24, y+ch-43, ' · '.join(item['highlights']), 17 if mobile else 16, CYAN)
    return rounded(im)


def research(mobile=False):
    w, p = (640,36) if mobile else (1200,56)
    cw = w-2*p
    size, leading = (26,38) if mobile else (25,36)
    rows = []
    for item in DATA['research']:
        lines = wrap(item['title'], cw-48, size)
        focus = wrap(item['focus'], cw-48, 19)
        rows.append((item, lines, focus, 104+len(lines)*leading+len(focus)*28))
    h = 156+sum(r[3] for r in rows)+20*(len(rows)-1)+36
    im = canvas(w,h)
    header(im,'02','Notes from the lab.','RESEARCH',mobile)
    y = 156
    for item, title_lines, focus_lines, rh in rows:
        box(im,(p,y,p+cw,y+rh))
        txt(im,p+24,y+24,item['venue'],18,GOLD,'mono')
        yy = y+66
        for line in title_lines:
            txt(im,p+24,yy,line,size,WHITE)
            yy += leading
        yy += 16
        for line in focus_lines:
            txt(im,p+24,yy,line,19,CYAN)
            yy += 28
        y += rh+20
    return rounded(im)


def awards(mobile=False):
    w,p = (640,36) if mobile else (1200,56)
    size = 25 if mobile else 24
    rows = []
    for item in DATA['awards']:
        tw = w-2*p-(48 if mobile else 154)
        title_lines = wrap(item['title'],tw,size)
        detail_lines = wrap(item['details'],tw,20 if mobile else 19)
        rh = 91+len(title_lines)*36+len(detail_lines)*29
        rows.append((item,title_lines,detail_lines,rh))
    h=156+sum(row[3] for row in rows)+20*(len(rows)-1)+36
    im=canvas(w,h)
    header(im,'03','Learning in the arena.','COMPETITIONS',mobile)
    y=156
    for item,titles,details,rh in rows:
        box(im,(p,y,w-p,y+rh))
        x=p+24 if mobile else p+132
        if not mobile:txt(im,p+24,y+42,item['rank'],44,GOLD,'serif')
        txt(im,x,y+22,item['award'].upper(),17,GOLD,'mono')
        yy=y+59
        for line in titles:
            txt(im,x,yy,line,size,WHITE)
            yy+=36
        yy+=12
        for line in details:
            txt(im,x,yy,line,20 if mobile else 19,MUTED)
            yy+=29
        y+=rh+20
    return rounded(im)


def toolkit(mobile=False):
    groups=[
      ('Code & web',['Languages','Web']),
      ('Cloud & delivery',['Cloud','Deployment & IaC']),
      ('Data & systems',['Databases','Systems & Tools']),
      ('Networks & observability',['Networking','Monitoring & Testing']),
      ('AI & hardware',['AI / ML','Hardware']),
      ('Design',['Design'])]
    skills=dict(DATA['skills'])
    w,p=(640,36) if mobile else (1200,56)
    cw=568 if mobile else 532
    size,leading=(24,36) if mobile else (21,32)
    cards=[]
    for title,categories in groups:
        values=' · '.join(word for category in categories for word in skills[category])
        content=wrap(values,cw-48,size)
        cards.append((title,content,100+len(content)*leading))
    if mobile:
        h=156+sum(c[2] for c in cards)+20*(len(cards)-1)+36
    else:
        rowh=[max(cards[i][2],cards[i+1][2]) for i in range(0,6,2)]
        h=156+sum(rowh)+40+36
    im=canvas(w,h)
    header(im,'04','A toolkit without borders.','SKILLS & TOOLS',mobile)
    yy=156
    for i,(title,content,ch) in enumerate(cards):
        x=p if mobile else p+(i%2)*556
        if mobile:
            y=yy
        else:
            y=156+sum(rowh[:i//2])+(i//2)*20
            ch=rowh[i//2]
        box(im,(x,y,x+cw,y+ch))
        txt(im,x+24,y+24,title,26 if mobile else 24,WHITE,'bold')
        for j,line in enumerate(content):txt(im,x+24,y+78+j*leading,line,size,MUTED)
        if mobile:yy+=ch+20
    return rounded(im)


def techstack(mobile=False):
    im=canvas(640 if mobile else 1200,148)
    header(im,'04','Tech Stack.','THE TOOLS BEHIND MY WORK',mobile)
    return rounded(im)


def credentials(mobile=False):
    w,h=(640,520) if mobile else (1200,340)
    im=canvas(w,h)
    header(im,'05','Solid foundations.','CERTIFICATIONS',mobile)
    for i,(code,name,issuer) in enumerate(DATA['certifications']):
        x=36 if mobile else 56+i*556
        y=156+i*166 if mobile else 156
        cw,ch=(568,144) if mobile else (532,144)
        box(im,(x,y,x+cw,y+ch))
        txt(im,x+24,y+24,issuer.upper(),17,CYAN,'mono')
        txt(im,x+24,y+68,code,36,GOLD,'serif')
        txt(im,x+214,y+78,name,25,WHITE)
    return rounded(im)


def footer(mobile=False,phase=0):
    w,h=(640,530) if mobile else (1200,274)
    im=canvas(w,h)
    p=36 if mobile else 56
    txt(im,p,30,'GO GOPHER × DUCK / KEEP EXPLORING',16,CYAN,'mono')
    txt(im,p,76,'Stay curious.' if mobile else 'Stay curious. Keep building.',44 if mobile else 46,WHITE,'serif')
    txt(im,p,139 if mobile else 145,'Keep building. Keep exploring.' if mobile else 'A little of everything. Always learning.',23,MUTED)
    dy=math.sin(phase*math.tau)*5
    if mobile:
        orbit(im,320,325,126,phase)
        stamp(im,150,153+dy,340)
        rule(im,p,454,568)
        txt(im,p,481,'atibodee.13chady.com  ↗',23,CYAN,'mono')
    else:
        orbit(im,1020,137,110,phase)
        stamp(im,864,-8+dy,308)
        txt(im,p,208,'atibodee.13chady.com  ↗',23,CYAN,'mono')
    return rounded(im)


def save_gif(path,render,mobile=False,frames=36):
    images=[render(mobile,i/frames) for i in range(frames)]
    palette=images[0].convert('RGB').quantize(colors=255,method=Image.Quantize.MEDIANCUT)
    values=palette.getpalette()[:255*3]+[255,0,255]
    palette.putpalette(values)
    indexed=[]
    for im in images:
        q=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE)
        mask=im.getchannel('A').point(lambda a:255 if a<128 else 0)
        q.paste(255,mask=mask)
        q.info['transparency']=255
        indexed.append(q)
    indexed[0].save(path,save_all=True,append_images=indexed[1:],duration=100,
                    loop=0,transparency=255,disposal=1,optimize=True)
    return path.stat().st_size


def picture(name,alt,animated=False):
    ext='gif' if animated else 'png'
    still=''
    if animated:
        still=f'  <source media="(prefers-reduced-motion: reduce) and (max-width: 640px)" srcset="./assets/profile/{name}-mobile.png">\n  <source media="(prefers-reduced-motion: reduce)" srcset="./assets/profile/{name}.png">\n'
    return '<picture>\n'+still+f'  <source media="(max-width: 640px)" srcset="./assets/profile/{name}-mobile.{ext}">\n  <img src="./assets/profile/{name}.{ext}" width="100%" alt="{escape(alt,quote=True)}">\n</picture>'


def readme():
    descriptions={
      'hero':f"{DATA['name']} (D), 13D4C — The Duck of IT. IT student at KMITL, Thailand. Animated Go Gopher and duck coding together. Web, cloud, networks, and AI.",
      'about':DATA['introduction'],
      'projects':'Selected work: D-judge / Judge-DD, AI-assisted homework assessment and rubric generation; IT KMITL Timetable, Project Manager and Frontend Developer; Smartpot / Smart Farm IoT, team project member; Teaching Assistant at IT KMITL for Computer Networks, OOP, and DSA.',
      'research':'; '.join(r['title']+' — '+r['venue'] for r in DATA['research']),
      'awards':'; '.join(a['award']+' — '+a['title'] for a in DATA['awards']),
      'toolkit':'Complete skills across languages, web, cloud, infrastructure as code, databases, systems, networking, observability, AI, hardware, and design. Full text below.',
      'techstack':'Tech Stack: languages, web, databases, cloud, infrastructure as code, AI, networking, monitoring, hardware, systems, and design, with the original technology logos.',
      'certifications':'; '.join(code+' — '+name+' · '+issuer for code,name,issuer in DATA['certifications']),
      'footer':'Go Gopher × Duck of IT. Stay curious. Keep building. atibodee.13chady.com.'}
    out=[picture('hero',descriptions['hero'],True),'','<p align="center">']
    for name,url in DATA['links']:
        out.append(f'  <a href="{url}"><img src="./assets/profile/link-{name.lower()}.svg" width="142" height="36" alt="{name}"></a>')
    out+=['</p>','']
    for name in ['about','projects','research','awards','techstack','certifications']:
        out += [picture(name,descriptions[name]),'']
        if name=='techstack':
            for group in json.loads((ROOT/'tech-stack.json').read_text()):
                out += ['### '+group['category'],'','<p>'+group['html']+'</p>','']
        if name=='projects':
            out += ['<p align="center"><a href="https://github.com/13D4C/Physical-Com-Project">Smart Farm IoT repository ↗</a> · <a href="https://13d4c.github.io/Physical-Com-Project/">Smartpot website ↗</a> · <a href="https://atibodee.13chady.com">Portfolio ↗</a></p>','']
    out += ['<details>','<summary><strong>Read the full profile and complete technology stack as text</strong></summary>','',
            '## About me','',DATA['introduction'],'',
            f"- **Name:** {DATA['name']} ({DATA['nickname']})",
            f"- **Education:** {DATA['education']}",f"- **Based in:** {DATA['location']}",'',
            '## Selected work','']
    for item in DATA['work']:
        out += ['### '+item['name'],'','**'+item['role']+'** — '+item['description'],'']
        if item['url']:out += ['[View repository]('+item['url']+')','']
    out += ['### Teaching Assistant','',DATA['teaching']['organization'],'',
            ' · '.join(DATA['teaching']['subjects']),'','## Research','']
    out += ['- **'+r['title']+'** — *'+r['venue']+'*' for r in DATA['research']]
    out += ['','## Competitions','']
    out += ['- **'+a['award']+'** — '+a['title']+'. '+a['details'] for a in DATA['awards']]
    out += ['','## Skills & tools','','| Area | Technologies |','| :-- | :-- |']
    out += ['| **'+category+'** | '+', '.join(skills)+' |' for category,skills in DATA['skills']]
    out += ['','## Certifications','']
    out += ['- **'+code+' — '+name+'** · '+issuer for code,name,issuer in DATA['certifications']]
    out += ['','## Connect','']
    out += ['- ['+name+']('+url+')' for name,url in DATA['links']]
    out += ['','</details>','', '<a href="https://atibodee.13chady.com">',picture('footer',descriptions['footer'],True),'</a>','',
      '<sub>Go Gopher by [Renée French](https://go.dev/blog/gopher), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Mascot duo: AI-generated adaptation with an original duck.</sub>','']
    (ROOT/'README.md').write_text('\n'.join(out))


def badges():
    for name,url in DATA['links']:
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="142" height="36" viewBox="0 0 142 36"><title>{escape(name)}</title><rect x="1" y="1" width="140" height="34" rx="17" fill="#103548" stroke="#2a6880"/><text x="14" y="24" font-family="Arial,sans-serif" font-size="16" fill="{WHITE}">{escape(name)}</text><text x="120" y="24" font-family="Arial,sans-serif" font-size="18" fill="{CYAN}">↗</text></svg>\n'
        (OUT/f'link-{name.lower()}.svg').write_text(svg)


def previews():
    for mobile in (False,True):
        names=['hero','about','projects','research','awards','techstack','certifications','footer']
        pics=[]
        for name in names:
            im=Image.open(OUT/(name+('-mobile' if mobile else '')+'.png')).convert('RGBA')
            width=384 if mobile else 840
            pics.append(im.resize((width,round(im.height*width/im.width)),Image.Resampling.LANCZOS))
        gap=16
        sheet=Image.new('RGB',(pics[0].width+32,sum(p.height for p in pics)+gap*(len(pics)+1)+44),'#f6f8fa')
        y=gap
        for i,im in enumerate(pics):
            sheet.paste(im,(gap,y),im)
            y+=im.height+gap
            if i==0:y+=44
        sheet.save(OUT/('preview-mobile.png' if mobile else 'preview-full.png'))
        if not mobile:
            sheet.crop((0,0,872,round(pics[0].height+pics[1].height+pics[2].height+108))).save(OUT/'preview.png')


def main():
    panels={'hero':hero,'about':about,'projects':projects,'research':research,'awards':awards,
            'toolkit':toolkit,'techstack':techstack,'certifications':credentials,'footer':footer}
    for name,render in panels.items():
        for mobile in (False,True):
            path=OUT/(name+('-mobile' if mobile else '')+'.png')
            render(mobile).save(path,optimize=True)
        print('Rendered',name,flush=True)
    for name,render in [('hero',hero),('footer',footer)]:
        for mobile in (False,True):
            path=OUT/(name+('-mobile' if mobile else '')+'.gif')
            size=save_gif(path,render,mobile)
            print('Animated',path.name,round(size/1024),'KiB',flush=True)
    badges()
    readme()
    previews()
    print('Profile ready.',flush=True)


if __name__=='__main__':
    main()
