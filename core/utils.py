# core/utils.py
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def render_to_pdf(template_src, context, filename):
    tpl = get_template(template_src)
    html = tpl.render(context)
    out = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=out)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    response = HttpResponse(out.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
