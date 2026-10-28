"""Generate PDF and editable Word CV from cv/content.json. Requires reportlab."""
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZipFile, ZIP_DEFLATED
import json
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak

ROOT = Path(__file__).resolve().parent
BASE = 'Mohammad_Imran_Hossain_CV'
DATA = json.loads((ROOT / 'cv/content.json').read_text(encoding='utf-8'))


def build_pdf():
    pairs = [(os.getenv('CV_FONT_REGULAR'), os.getenv('CV_FONT_BOLD')), ('C:/Windows/Fonts/calibri.ttf', 'C:/Windows/Fonts/calibrib.ttf'), ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')]
    for regular, bold in pairs:
        if regular and bold and Path(regular).is_file() and Path(bold).is_file():
            pdfmetrics.registerFont(TTFont('CV', regular))
            pdfmetrics.registerFont(TTFont('CV-Bold', bold))
            break
    else:
        raise RuntimeError('Set CV_FONT_REGULAR and CV_FONT_BOLD to Unicode TTF paths.')
    styles = {}
    definitions = {'body':(10.4,13.6,False,'29232A',0,6), 'title':(11.3,14,True,'29232A',7,3), 'meta':(9.5,12.6,False,'655B64',0,5), 'section':(13.5,17,True,'943B80',13,8), 'name':(25,29,True,'29232A',0,8), 'role':(11.8,16,True,'943B80',0,8), 'bullet':(10.4,13.6,False,'29232A',0,5)}
    for key,(size,leading,bold,color,before,after) in definitions.items():
        styles[key]=ParagraphStyle(key,fontName='CV-Bold' if bold else 'CV',fontSize=size,leading=leading,textColor=colors.HexColor('#'+color),spaceBefore=before,spaceAfter=after,keepWithNext=key in ['title','meta','section'],leftIndent=12 if key=='bullet' else 0,bulletIndent=0)
    story=[]
    def add(text,style='body',bullet=None):
        story.append(Paragraph(escape(text),styles[style],bulletText=bullet))
    def link(label,url):
        story.append(Paragraph('<link href="'+escape(url, {'"':'&quot;'})+'" color="#943B80">'+escape(label)+'</link>',styles['meta']))
    for i,page in enumerate(DATA['pages']):
        if i: story.append(PageBreak())
        else:
            add(DATA['name'],'name'); add(DATA['role'],'role')
            add(DATA['location']+' | '+DATA['email'],'meta')
            links = ' | '.join('<link href="'+escape(url, {'"':'&quot;'})+'" color="#943B80">'+escape(label)+'</link>' for label,url in DATA['links'])
            story.append(Paragraph(links,styles['meta']))
            add('ACADEMIC CURRICULUM VITAE | Updated October 2026','meta')
        for section in page:
            add(section['heading'],'section')
            for entry in section['entries']:
                if entry.get('title'): add(entry['title'],'title')
                if entry.get('meta'): add(entry['meta'],'meta')
                for text in entry.get('paragraphs',[]): add(text)
                for text in entry.get('bullets',[]): add(text,'bullet','•')
                if entry.get('url'): link(entry.get('link_label',entry['url']),entry['url'])
    def footer(canvas,doc):
        canvas.saveState(); canvas.setStrokeColor(colors.HexColor('#E3D9E0'))
        canvas.line(43,39,A4[0]-43,39); canvas.setFont('CV',8)
        canvas.setFillColor(colors.HexColor('#655B64'))
        canvas.drawString(43,26,DATA['name']+' | Academic CV')
        canvas.drawRightString(A4[0]-43,26,str(doc.page)); canvas.restoreState()
    doc=SimpleDocTemplate(str(ROOT/(BASE+'.pdf')),pagesize=A4,leftMargin=43,rightMargin=43,topMargin=35,bottomMargin=52,title=DATA['name']+' — Academic Curriculum Vitae',author=DATA['name'],subject='Medical AI, computational oncology, and academic research',pageCompression=1)
    doc.build(story,onFirstPage=footer,onLaterPages=footer)


def build_docx():
    rels=[]
    def p(text,style='Normal'):
        return '<w:p><w:pPr><w:pStyle w:val="'+style+'"/></w:pPr><w:r><w:t xml:space="preserve">'+escape(text)+'</w:t></w:r></w:p>'
    def link(label,url):
        rid='rIdLink'+str(len(rels)+1)
        rels.append('<Relationship Id="'+rid+'" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="'+escape(url, {'"':'&quot;'})+'" TargetMode="External"/>')
        return '<w:p><w:hyperlink r:id="'+rid+'"><w:r><w:rPr><w:color w:val="943B80"/><w:u w:val="single"/></w:rPr><w:t>'+escape(label)+'</w:t></w:r></w:hyperlink></w:p>'
    body=[p(DATA['name'],'Title'),p(DATA['role'],'Subtitle'),p(DATA['location']+' | '+DATA['email'])]
    header_links = [link(label,url) for label,url in DATA['links']]
    body.append('<w:p>'+'<w:r><w:t xml:space="preserve"> | </w:t></w:r>'.join(t.removeprefix('<w:p>').removesuffix('</w:p>') for t in header_links)+'</w:p>')
    body.append(p('ACADEMIC CURRICULUM VITAE | Updated October 2026','Meta'))
    for i,page in enumerate(DATA['pages']):
        if i: body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
        for section in page:
            body.append(p(section['heading'],'Heading1'))
            for entry in section['entries']:
                if entry.get('title'): body.append(p(entry['title'],'Heading2'))
                if entry.get('meta'): body.append(p(entry['meta'],'Meta'))
                body.extend(p(t) for t in entry.get('paragraphs',[]))
                body.extend(p('• '+t) for t in entry.get('bullets',[]))
                if entry.get('url'): body.append(link(entry.get('link_label',entry['url']),entry['url']))
    ns='xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
    sect='<w:sectPr><w:footerReference w:type="default" r:id="rIdFooter"/><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="700" w:right="860" w:bottom="950" w:left="860" w:footer="450"/></w:sectPr>'
    doc='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document '+ns+'><w:body>'+''.join(body)+sect+'</w:body></w:document>'
    styles='<w:styles '+ns+'><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="21"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="100" w:line="280"/><w:widowControl/></w:pPr></w:pPrDefault></w:docDefaults><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'
    for name,size,color,bold,keep,before in [('Title',48,'29232A',True,True,0),('Subtitle',24,'943B80',True,True,0),('Heading1',27,'943B80',True,True,220),('Heading2',23,'29232A',True,True,130),('Meta',19,'655B64',False,True,0)]:
        styles+='<w:style w:type="paragraph" w:styleId="'+name+'"><w:name w:val="'+name+'"/><w:basedOn w:val="Normal"/><w:pPr>'+('<w:keepNext/>' if keep else '')+'<w:spacing w:before="'+str(before)+'" w:after="90"/></w:pPr><w:rPr><w:sz w:val="'+str(size)+'"/><w:color w:val="'+color+'"/>'+('<w:b/>' if bold else '')+'</w:rPr></w:style>'
    styles+='</w:styles>'
    relns='http://schemas.openxmlformats.org/package/2006/relationships'
    wordrels='<Relationships xmlns="'+relns+'"><Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rIdFooter" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>'+''.join(rels)+'</Relationships>'
    types='<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
    for path,kind in [('document','document.main'),('styles','styles'),('footer1','footer')]: types+='<Override PartName="/word/'+path+'.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.'+kind+'+xml"/>'
    types+='</Types>'
    footer='<w:ftr '+ns+'><w:p><w:pPr><w:jc w:val="right"/></w:pPr><w:r><w:rPr><w:sz w:val="16"/></w:rPr><w:t>'+escape(DATA['name'])+' | Academic CV | </w:t></w:r><w:fldSimple w:instr="PAGE"/></w:p></w:ftr>'
    with ZipFile(ROOT/(BASE+'.docx'),'w',ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml',types)
        z.writestr('_rels/.rels','<Relationships xmlns="'+relns+'"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
        z.writestr('word/document.xml',doc); z.writestr('word/styles.xml',styles)
        z.writestr('word/_rels/document.xml.rels',wordrels); z.writestr('word/footer1.xml',footer)


if __name__=='__main__':
    build_pdf(); build_docx()
    for ext in ['pdf','docx']:
        path=ROOT/(BASE+'.'+ext)
        print(f'{path.name}: {path.stat().st_size:,} bytes')
