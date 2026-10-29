"""Build the scrolling deck from the final Google Slides PDF and PowerPoint exports.

Usage: python tools/build_web_deck.py path/to/export.pdf
Requires Poppler's pdftocairo. No Python packages are required.
"""
import concurrent.futures
import html
import hashlib
import re
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def esc(s): return html.escape(s, quote=True)

def asset(path):
    digest = hashlib.sha256((ROOT/path).read_bytes()).hexdigest()[:10]
    return f'{path}?v={digest}'

DOT_PATTERN = '<pattern id="web-dot-grid" width="15" height="15" patternUnits="userSpaceOnUse"><circle cx="7.5" cy="7.5" r="0.5" fill="#c9ced4" fill-opacity="0.65"/></pattern>'
GRID_IMAGE_HASHES = {
    'source-7': '7212bb6a7cc9',
    'source-6': '936f7cf56daa',
}

def soften_grid(path):
    """Replace only the shared background image from the Slides export."""
    svg = path.read_text()
    for image_id, digest in GRID_IMAGE_HASHES.items():
        match = re.search(r'<image id="' + image_id + r'"[^>]*/>', svg)
        if not match:
            return  # The appendices have no shared grid background.
        href = re.search(r'xlink:href="([^"]+)"', match[0])[1]
        if hashlib.sha256(href.encode()).hexdigest()[:12] != digest:
            raise ValueError(f'Background changed in {path}; inspect it before replacing it.')
    group = r'<g mask="url\(#mask-0\)">\s*<use xlink:href="#source-6"[^>]*/>\s*</g>'
    svg, count = re.subn(group, '<rect width="720" height="405" fill="url(#web-dot-grid)"/>', svg)
    if count != 1:
        raise ValueError(f'Expected one shared grid in {path}, found {count}.')
    for image_id in GRID_IMAGE_HASHES:
        svg = re.sub(r'<image id="' + image_id + r'"[^>]*/>\s*', '', svg)
    svg = svg.replace('<defs>', '<defs>\n' + DOT_PATTERN, 1)
    path.write_text(svg)

def build(pdf):
    out = ROOT / 'web/slides'
    out.mkdir(parents=True, exist_ok=True)
    (ROOT/'web/dot-grid.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 405"><defs>' + DOT_PATTERN + '</defs><rect width="720" height="405" fill="#f8f9fa"/><rect width="720" height="405" fill="url(#web-dot-grid)"/></svg>\n')
    with zipfile.ZipFile(ROOT / 'AI in Architecture - Presentation.pptx') as z:
        pres = ET.fromstring(z.read('ppt/presentation.xml'))
        rels = ET.fromstring(z.read('ppt/_rels/presentation.xml.rels'))
        targets = {r.attrib['Id']: r.attrib['Target'] for r in rels}
        slides = []
        for item in pres.find('p:sldIdLst', NS):
            target = targets[item.attrib['{' + NS['r'] + '}id']]
            tree = ET.fromstring(z.read('ppt/' + target.lstrip('/').removeprefix('ppt/')))
            texts = [e.text or '' for e in tree.findall('.//a:t', NS)]
            paragraphs = [''.join(e.text or '' for e in p.findall('.//a:t', NS)).strip() for p in tree.findall('.//a:p', NS)]
            title = next((p for p in paragraphs if p and not p.startswith('AI in Architecture |')), 'Slide')
            relpath = 'ppt/slides/_rels/' + Path(target).name + '.rels'
            links = []
            if relpath in z.namelist():
                for r in ET.fromstring(z.read(relpath)):
                    url = r.attrib.get('Target', '')
                    if r.attrib.get('Type', '').endswith('/hyperlink') and url.startswith(('https://', 'http://')):
                        labels = [e.text or '' for run in tree.findall('.//a:r', NS) if any(h.attrib.get('{' + NS['r'] + '}id') == r.attrib['Id'] for h in run.findall('.//a:hlinkClick', NS)) for e in run.findall('.//a:t', NS)]
                        links.append({'url': url, 'label': ''.join(labels).strip() or 'Source'})
            slides.append({'number': len(slides)+1, 'title': title, 'text': '\n'.join(texts), 'links': links})
    def render(slide):
        n = slide['number']
        subprocess.run(['pdftocairo', '-svg', '-f', str(n), '-l', str(n), str(pdf), str(out/f'slide-{n:02}.svg')], check=True)
        soften_grid(out/f'slide-{n:02}.svg')
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(render, slides))
    videos = json.loads((ROOT/'tools/youtube-videos.json').read_text())['videos']
    by_slide = {v['slide']: v for v in videos}
    sections = []
    for s in slides:
        n = s['number']; title = s['title']; text = s['text']
        body = f'<img src="{asset(f'web/slides/slide-{n:02}.svg')}" alt="{esc(text)}" loading="{"eager" if n == 1 else "lazy"}" width="1280" height="720">'
        extra = '<div class="source-links">' + ' · '.join(f'<a href="{esc(link["url"])}" target="_blank" rel="noopener">{esc(link["label"])}</a>' for link in s['links']) + '</div>' if s['links'] else ''
        if n in by_slide:
            v = by_slide[n]; title = v['title']; s['video'] = v
            body = f'<iframe loading="lazy" src="https://www.youtube-nocookie.com/embed/{esc(v["id"])}?rel=0&amp;playsinline=1&amp;enablejsapi=1" title="{esc(title)}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>'
            extra = f'<div class="video-links"><span>{esc(title)}</span><span><a href="https://youtu.be/{esc(v["id"])}" target="_blank" rel="noopener">YouTube</a> · <a href="{esc(v["path"])}">MP4 backup</a></span></div>'
        if title.strip().lower() in ('q&a', 'q & a') or n == 33:
            body = '<div class="qna"><h2>Questions and Answers</h2><a class="qr" href="https://range-et.github.io/AI_arch_resources/"><img src="web/deck-qr.svg" width="180" height="180" alt="QR code: open the presentation and demos"><span>Presentation and demos</span><small>range-et.github.io/AI_arch_resources</small></a><div class="qna-footer">AI in Architecture | Indrajeet Haldar</div></div>'
        sections.append(f'<section class="slide" id="slide-{n:02}" aria-label="Slide {n}: {esc(title)}"><div class="slide-content"><div class="frame">{body}</div>{extra}</div></section>')
    options = ''.join(f'<option value="{s["number"]-1}">{s["number"]}. {esc(by_slide.get(s["number"], s)["title"])}</option>' for s in slides)
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="referrer" content="strict-origin-when-cross-origin"><meta name="description" content="AI in Architecture: a presentation with Rhino, Grasshopper and zoning demos."><title>AI in Architecture — Indrajeet Haldar</title><link rel="icon" href="data:,"><link rel="stylesheet" href="{asset('web/deck.css')}"><script src="web/deck.js" defer></script></head>
<body><a class="skip" href="#slides">Skip to slides</a><header><a href="#slide-01" class="brand">AI in Architecture</a><nav aria-label="Presentation controls"><button id="prev" aria-label="Previous slide">←</button><label><span class="sr-only">Go to slide</span><select id="jump">{options}</select></label><button id="next" aria-label="Next slide">→</button><button id="fullscreen">Full screen</button><a href="https://github.com/range-et/AI_arch_resources">Files</a></nav></header><main id="slides">{''.join(sections)}</main><footer>Scroll or use ↑ ↓ to move through the slides. Videos have captions and no audio. <a href="AI%20in%20Architecture%20-%20Presentation.pptx">PowerPoint</a> · <a href="https://github.com/range-et/AI_arch_resources#readme">Demo guide and sources</a></footer></body></html>'''
    (ROOT/'index.html').write_text(page)
    (ROOT/'web/slides.json').write_text(json.dumps(slides, indent=2, ensure_ascii=False)+'\n')
    (ROOT/'.nojekyll').touch()
    print(f'Built {len(slides)} slides with {len(videos)} videos.')

if __name__ == '__main__':
    build(Path(sys.argv[1]).resolve())
