import os
from datetime import datetime
from smtplib import SMTPException
import threading
from django.utils._os import safe_join
from weasyprint import HTML

from main_site.models import Schedule
from transport.settings import BASE_DIR, EMAIL_HOST_USER
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string

def get_bill_as_pdf(request,bill):

    BILL_ROOT = os.path.join(BASE_DIR, 'files/Bill')
    fs = FileSystemStorage(BILL_ROOT)
    filename=str(bill.id)+".pdf"
    # if fs.exists(filename):
    #     with fs.open(filename) as pdf:
    #         response = HttpResponse(pdf, content_type='application/pdf')
    #         response['Content-Disposition'] = 'inline; filename='+"bill_"+filename
    #         return response

    html_string = render_to_string('custom_templates/bill_template.html', {'bill':bill})

    html = HTML(string=html_string)
    html.write_pdf(target=BILL_ROOT+"/"+filename)

    with fs.open(filename) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename='+"bill_"+filename
        return response

    return Http404

#does not work
def render_schedule():

    ROOT = os.path.join(BASE_DIR, 'files/')
    fs = FileSystemStorage(ROOT)
    filename=Schedule.objects.all().order_by('created_at')[0].file.name

    # if fs.exists(filename):
    #     with fs.open(filename) as pdf:
    #         response = HttpResponse(pdf, content_type='application/pdf')
    #         response['Content-Disposition'] = 'inline; filename='+"bill_"+filename
    #         return response

    with fs.open(filename) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename='+"bill_"+filename
        return response

    return Http404

class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run (self):
        msg = EmailMessage(self.subject, self.html_content, EMAIL_HOST_USER, self.recipient_list)
        msg.content_subtype = "html"
        try:
            msg.send()
        except SMTPException as e:
            print('error',e)

def send_html_mail(subject, html_content, recipient_list):
    EmailThread(subject, html_content, recipient_list).start()

# def validate_s    chedule(x,y):
#     slots=x.split(",")
#     times=y.split(",")
#     if len(slots) != len(times):
#         return False
#     for i in times:
#         try:
#             i=datetime.strptime(i, '%I:%M')
#         except ValueError:
#             print(i)
#             return False
#     return True



# def mail_to_admins(message=None):
#     admin_set=User.groups.filter(groups__name='TransportAdmin').values()
#     recepients=[]
#     if admin_set.exists():
#         for i in admin_set.iterator():
#             recepients.append(i.email)
#     send_email(title='Transport Schedule Changed',body=message,recepients=recepients)
