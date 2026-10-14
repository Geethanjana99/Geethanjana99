from pathlib import Path
import re
from markdown_it import MarkdownIt
from bs4 import BeautifulSoup
r=Path(__file__).resolve().parents[1]
md=MarkdownIt('commonmark',{'html':True}).enable('table')
soup=BeautifulSoup(md.render((r/'README.md').read_text()),'html.parser')
for h in soup.find_all(re.compile('^h[1-6]$')):
    h['id']=re.sub(r'[^a-z0-9 -]','',h.get_text().lower()).replace(' ','-')
base='''
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;font-size:16px;line-height:1.6;background:var(--bg);color:var(--fg)}
.preview-bar{max-width:1012px;margin:0 auto;padding:20px 28px;font-size:12px;letter-spacing:.06em;color:var(--muted)}
.markdown-body{max-width:1012px;padding:30px 32px 44px;margin:0 auto 56px;border:1px solid var(--border);border-radius:8px;overflow-wrap:break-word}
h1{font-size:30px;line-height:1.35;margin:26px 0 20px;font-weight:650;letter-spacing:-.02em;border-bottom:1px solid var(--border);padding-bottom:14px}
h2{font-size:25px;margin:40px 0 18px;line-height:1.25;padding-bottom:10px;border-bottom:1px solid var(--border)}
h3{font-size:20px;margin:26px 0 16px;line-height:1.4}p{margin:16px 0}img{max-width:100%;height:auto;vertical-align:middle}picture{display:block;margin:18px 0}picture img{display:block}a{color:var(--link);text-decoration:none}a:hover{text-decoration:underline}strong{font-weight:650}hr{border:0;background:var(--border);height:3px;margin:28px 0}
code{font-family:ui-monospace,SFMono-Regular,Consolas,"Liberation Mono",monospace;background:var(--code);border-radius:6px;padding:.22em .4em;font-size:85%;line-height:2.3}pre{overflow:auto;padding:16px;background:var(--code);border-radius:6px}pre code{padding:0;background:none}
table{display:block;width:max-content;max-width:100%;overflow-x:auto;border-collapse:collapse;margin:20px 0}th,td{padding:9px 13px;border:1px solid var(--border);vertical-align:top;text-align:left}th{font-weight:650;background:var(--code)}tr:nth-child(2n){background:var(--stripe)}details{margin:20px 0}summary{cursor:pointer;color:var(--link);padding:4px 0}details[open] summary{margin-bottom:14px}blockquote{margin:20px 0;border-left:4px solid var(--border);padding:0 16px;color:var(--muted)}p[align="center"] a img{margin:5px 2px}
@media(max-width:650px){.markdown-body{padding:15px;border:0;margin-bottom:0}.preview-bar{padding:12px 15px;font-size:10px}h1{font-size:25px}h2{font-size:23px}h3{font-size:19px}p[align="center"] a img{width:146px}td,th{padding:8px 10px;font-size:14px}table{width:auto}picture{margin:14px 0}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
'''
for name,palette in [
 ('preview.html','--bg:#0d1117;--fg:#e6edf3;--muted:#8b949e;--border:#30363d;--link:#79c0ff;--code:#161b22;--stripe:#10161e;'),
 ('preview-light.html','--bg:#ffffff;--fg:#1f2328;--muted:#636c76;--border:#d0d7de;--link:#0969da;--code:#f6f8fa;--stripe:#f6f8fa;')]:
    content=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Geethanjana | GitHub Profile Preview</title><style>:root{{{palette}}}{base}</style></head><body><div class="preview-bar">GEETHANJANA99 / README PREVIEW — LOCAL APPROXIMATION OF GITHUB STYLING</div><main class="markdown-body">{soup}</main></body></html>'''
    (r/name).write_text(content,encoding='utf-8')
print('Preview files built.')
