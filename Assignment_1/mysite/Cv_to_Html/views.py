from django.shortcuts import render
from .forms import ResumeForm
import fitz  

def upload_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save()
            pdf_file = resume.pdf.path

            html_content = convert_pdf_to_html(pdf_file)

            return render(request, 'Cv_to_Html/result.html', {'html_content': html_content})
    else:
        form = ResumeForm()

    return render(request, 'Cv_to_Html/resume_upload.html', {'form': form})

def convert_pdf_to_html(pdf_file):

    pdf_document = fitz.open(pdf_file)
    html_content = ""

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text("html")
        html_content += text

    pdf_document.close()
    return html_content
