"""Convert this specific docx-js brochure to print ready HTML (keeps cell shading, colours, sizes, bullets, images)."""
import sys, os, base64, html
import xml.etree.ElementTree as ET

D = sys.argv[1]          # unzipped docx folder
OUT = sys.argv[2]
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
WP = '{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}'

rels = {}
for rel in ET.parse(os.path.join(D, 'word/_rels/document.xml.rels')).getroot():
    rels[rel.get('Id')] = rel.get('Target')

def tw(v):  # twips to px
    return round(int(v) / 15, 1)

def attr(el, tag, a='val'):
    if el is None: return None
    x = el.find(W + tag)
    return None if x is None else x.get(W + a)

def run_html(r):
    rpr = r.find(W + 'rPr')
    st = []
    if rpr is not None:
        if rpr.find(W + 'b') is not None and rpr.find(W + 'b').get(W + 'val') not in ('0', 'false'): st.append('font-weight:700')
        if rpr.find(W + 'i') is not None and rpr.find(W + 'i').get(W + 'val') not in ('0', 'false'): st.append('font-style:italic')
        if rpr.find(W + 'u') is not None and rpr.find(W + 'u').get(W + 'val') not in ('none',): st.append('text-decoration:underline')
        c = attr(rpr, 'color')
        if c and c != 'auto': st.append('color:#' + c)
        sz = attr(rpr, 'sz')
        if sz: st.append('font-size:%gpt' % (int(sz) / 2))
        shd = rpr.find(W + 'shd')
        if shd is not None and shd.get(W + 'fill') not in (None, 'auto'): st.append('background:#' + shd.get(W + 'fill'))
    out = []
    for ch in r:
        if ch.tag == W + 't':
            out.append(html.escape(ch.text or ''))
        elif ch.tag == W + 'br':
            out.append('<span class="pb"></span>' if ch.get(W + 'type') == 'page' else '<br>')
        elif ch.tag == W + 'tab':
            out.append('&emsp;')
        elif ch.tag == W + 'drawing':
            blip = ch.find('.//' + A + 'blip')
            ext = ch.find('.//' + WP + 'extent')
            if blip is not None:
                tgt = rels[blip.get(R + 'embed')]
                data = open(os.path.join(D, 'word', tgt), 'rb').read()
                w = round(int(ext.get('cx')) / 9525) if ext is not None else ''
                h = round(int(ext.get('cy')) / 9525) if ext is not None else ''
                out.append('<img src="data:image/png;base64,%s" style="width:%spx;height:%spx">' % (base64.b64encode(data).decode(), w, h))
    s = ''.join(out)
    return '<span style="%s">%s</span>' % (';'.join(st), s) if st else s

def para_html(p):
    ppr = p.find(W + 'pPr')
    st = []
    bullet = False
    if ppr is not None:
        jc = attr(ppr, 'jc')
        if jc: st.append('text-align:' + {'both': 'justify', 'start': 'left', 'end': 'right'}.get(jc, jc))
        sp = ppr.find(W + 'spacing')
        if sp is not None:
            if sp.get(W + 'before'): st.append('margin-top:%spx' % tw(sp.get(W + 'before')))
            if sp.get(W + 'after'): st.append('margin-bottom:%spx' % tw(sp.get(W + 'after')))
            if sp.get(W + 'line') and sp.get(W + 'lineRule', 'auto') == 'auto': st.append('line-height:%.2f' % (int(sp.get(W + 'line')) / 240 * 1.15))
        shd = ppr.find(W + 'shd')
        if shd is not None and shd.get(W + 'fill') not in (None, 'auto'): st.append('background:#' + shd.get(W + 'fill'))
        if ppr.find(W + 'numPr') is not None: bullet = True
    inner = []
    for ch in p:
        if ch.tag == W + 'r':
            inner.append(run_html(ch))
        elif ch.tag == W + 'hyperlink':
            href = rels.get(ch.get(R + 'id'), '#')
            inner.append('<a href="%s">%s</a>' % (html.escape(href), ''.join(run_html(r) for r in ch.findall(W + 'r'))))
    body = ''.join(inner) or '&nbsp;'
    cls = ' class="li"' if bullet else ''
    return '<p%s style="%s">%s</p>' % (cls, ';'.join(st), body)

def border_css(b, side):
    if b is None: return ''
    x = b.find(W + side)
    if x is None: return ''
    if x.get(W + 'val') in ('nil', 'none'): return 'border-%s:none;' % side
    sz = int(x.get(W + 'sz', '4')) / 8
    col = x.get(W + 'color', '000000')
    col = '000000' if col == 'auto' else col
    return 'border-%s:%.2fpt solid #%s;' % (side, max(sz, .5), col)

def table_html(t):
    tpr = t.find(W + 'tblPr')
    tb = tpr.find(W + 'tblBorders') if tpr is not None else None
    grid = [tw(g.get(W + 'w')) for g in t.find(W + 'tblGrid')]
    total = sum(grid)
    rows = []
    for tr in t.findall(W + 'tr'):
        cells = []
        for tc in tr.findall(W + 'tc'):
            tcpr = tc.find(W + 'tcPr')
            st = []
            if tcpr is not None:
                w = attr(tcpr, 'tcW', 'w')
                if w and attr(tcpr, 'tcW', 'type') == 'dxa': st.append('width:%spx' % tw(w))
                shd = tcpr.find(W + 'shd')
                if shd is not None and shd.get(W + 'fill') not in (None, 'auto'): st.append('background:#' + shd.get(W + 'fill'))
                va = attr(tcpr, 'vAlign')
                if va: st.append('vertical-align:' + {'center': 'middle'}.get(va, va))
                mar = tcpr.find(W + 'tcMar')
                if mar is not None:
                    for side in ('top', 'right', 'bottom', 'left'):
                        m = mar.find(W + side)
                        if m is not None and m.get(W + 'w'): st.append('padding-%s:%spx' % (side, tw(m.get(W + 'w'))))
                b = tcpr.find(W + 'tcBorders')
                cb = ''.join(border_css(b if b is not None else tb, s) for s in ('top', 'right', 'bottom', 'left'))
                st.append(cb)
            span = attr(tcpr, 'gridSpan')
            content = ''.join(para_html(x) if x.tag == W + 'p' else table_html(x) for x in tc if x.tag in (W + 'p', W + 'tbl'))
            cells.append('<td%s style="%s">%s</td>' % (' colspan="%s"' % span if span else '', ';'.join(st), content))
        rows.append('<tr>%s</tr>' % ''.join(cells))
    tw_ = attr(tpr, 'tblW', 'w') if tpr is not None else None
    width = '%spx' % tw(tw_) if tw_ and attr(tpr, 'tblW', 'type') == 'dxa' else '100%'
    jc = attr(tpr, 'jc') if tpr is not None else None
    mx = 'margin:0 auto;' if jc == 'center' else ''
    return '<table style="width:%s;%s"><colgroup>%s</colgroup>%s</table>' % (width, mx, ''.join('<col style="width:%spx">' % g for g in grid), ''.join(rows))

doc = ET.parse(os.path.join(D, 'word/document.xml')).getroot()
body = doc.find(W + 'body')
parts = []
kids=[ch for ch in body if ch.tag in (W + 'p', W + 'tbl')]
i=0
while i < len(kids):
    ch=kids[i]
    if ch.tag == W + 'tbl' and len(ch.findall(W + 'tr'))==1 and len(ch.find(W + 'tr').findall(W + 'tc'))==1 and i+2 < len(kids):
        grp=[ch]+kids[i+1:i+3]
        parts.append('<div style="break-inside:avoid">'+''.join(para_html(x) if x.tag==W+'p' else table_html(x) for x in grp)+'</div>')
        i+=3; continue
    parts.append(para_html(ch) if ch.tag == W + 'p' else table_html(ch)); i+=1
footer = ''
fp = os.path.join(D, 'word/footer1.xml')
if os.path.exists(fp):
    footer = ''.join(para_html(p) for p in ET.parse(fp).getroot().iter(W + 'p'))

page = '''<!doctype html><html><head><meta charset="utf-8"><style>
@page { size: A4; margin: 14mm 17.6mm 20mm 17.6mm; @bottom-center { content: "Kids' Cerebral Academy  |  KCA INDIA  |  Since 2008  |  www.kcaindia.com"; font-family: Arial, Helvetica, sans-serif; font-size: 8.5pt; color: #92278F; } }
body { font-family: Arial, Helvetica, sans-serif; font-size: 11pt; color:#000; margin:0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
p { margin:0; }
p.li { padding-left: 1.4em; text-indent: -1em; }
p.li::before { content: "\\2022"; display:inline-block; width:1em; text-indent:0; color:#E6007E; }
table { border-collapse: collapse; table-layout: fixed; }
td { padding: 4px 8px; }
tr { break-inside: avoid; }
a { color: inherit; }
.pb { display:block; break-after: page; }
.ft { position: fixed; bottom: -12mm; left: 0; right: 0; text-align:center; }
</style></head><body>%s</body></html>''' % (''.join(parts),)
open(OUT, 'w').write(page)
print('ok', len(page))
