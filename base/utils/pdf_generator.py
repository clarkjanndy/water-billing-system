from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO

class PDFGenerator():
    
    def __init__(self, template, context):
        self.template = template
        self.context = context
    
    def generate(self):
        #create a blank pdf file 
        pdf = BytesIO()
         
        #render the data to the html template
        template = get_template(self.template)
        html = template.render(self.context)
        
        #write data to the pdf file
        if pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=pdf).err:
            raise BufferError('Error Generating PDF')
        
        pdf.seek(0)
        return pdf

pdf_generator = PDFGenerator