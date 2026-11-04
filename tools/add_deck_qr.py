"""Add the presentation QR to the introduction and Q&A in the local PowerPoint."""
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
REL = 'http://schemas.openxmlformats.org/package/2006/relationships'
URL = 'https://range-et.github.io/AI_arch_resources/'
NS = {'p': P, 'a': A}
for prefix, uri in [('p', P), ('a', A), ('r', R)]: ET.register_namespace(prefix, uri)
def inch(n): return str(round(n * 914400))
def qr_picture(shape_id, x, y, width):
    height = width * 600 / 520
    return ET.fromstring(f'''<p:pic xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}">
    <p:nvPicPr><p:cNvPr id="{shape_id}" name="Presentation website QR" descr="Scan to follow the presentation"><a:hlinkClick r:id="rIdDeckQRLink"/></p:cNvPr><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>
    <p:blipFill><a:blip r:embed="rIdDeckQRImage"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>
    <p:spPr><a:xfrm><a:off x="{inch(x)}" y="{inch(y)}"/><a:ext cx="{inch(width)}" cy="{inch(height)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>''')

def main():
    path = ROOT/'AI in Architecture - Presentation.pptx'
    with zipfile.ZipFile(path) as z: files = {n: z.read(n) for n in z.namelist()}
    targets = []
    for name in files:
        if not name.startswith('ppt/slides/slide') or not name.endswith('.xml'): continue
        tree = ET.fromstring(files[name])
        text = [''.join(t.text or '' for t in sp.findall('.//a:t', NS)).strip() for sp in tree.findall('.//p:sp', NS)]
        if name == 'ppt/slides/slide1.xml' or 'Questions and Answers' in text:
            targets.append((name, tree, 'Questions and Answers' in text))
    assert len(targets) == 2
    for name, tree, qna in targets:
        shapes = tree.find('p:cSld/p:spTree', NS)
        for shape in list(shapes):
            if any(x.get('name') == 'Presentation website QR' for x in shape.findall('.//p:cNvPr', NS)): shapes.remove(shape)
        relpath = 'ppt/slides/_rels/' + Path(name).name + '.rels'
        existing_rels = ET.fromstring(files[relpath])
        if any(rel.get('Target', '').rstrip('/') == URL.rstrip('/') for rel in existing_rels):
            continue
        shape_id = 1 + max(int(x.get('id', '0')) for x in tree.findall('.//p:cNvPr', NS))
        if qna:
            for shape in shapes.findall('p:sp', NS):
                if ''.join(t.text or '' for t in shape.findall('.//a:t', NS)).strip() == 'Questions and Answers':
                    shape.find('.//a:xfrm/a:off', NS).set('y', inch(.55))
            shapes.append(qr_picture(shape_id, 3.8, 1.55, 2.4))
        else: shapes.append(qr_picture(shape_id, 7.75, .45, 1.7))
        files[name] = ET.tostring(tree, encoding='utf-8', xml_declaration=True)
        relpath = 'ppt/slides/_rels/' + Path(name).name + '.rels'
        rels = ET.fromstring(files[relpath])
        if any(rel.get('Target', '').rstrip('/') == URL.rstrip('/') for rel in rels):
            continue  # The Google Slides export already contains this QR.
        for rel in list(rels):
            if rel.get('Id') in ('rIdDeckQRImage', 'rIdDeckQRLink'): rels.remove(rel)
        ET.SubElement(rels, '{'+REL+'}Relationship', Id='rIdDeckQRImage', Type=R+'/image', Target='../media/presentation-website-qr.png')
        ET.SubElement(rels, '{'+REL+'}Relationship', Id='rIdDeckQRLink', Type=R+'/hyperlink', Target=URL, TargetMode='External')
        files[relpath] = ET.tostring(rels, encoding='utf-8', xml_declaration=True)
    files['ppt/media/presentation-website-qr.png'] = (ROOT/'web/deck-qr.png').read_bytes()
    types = ET.fromstring(files['[Content_Types].xml'])
    if not any(x.get('Extension') == 'png' for x in types):
        ET.SubElement(types, '{http://schemas.openxmlformats.org/package/2006/content-types}Default', Extension='png', ContentType='image/png')
        files['[Content_Types].xml'] = ET.tostring(types, encoding='utf-8', xml_declaration=True)
    temp = path.with_suffix('.tmp.pptx')
    with zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in files.items(): z.writestr(name, data)
    temp.replace(path)
    print('Added QR to:', ', '.join(name for name, _, _ in targets))

if __name__ == '__main__': main()
