import os
from datetime import datetime

# from weasyprint import HTML

from transport.settings import BASE_DIR
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

def send_email(title,body,recepients):
    email = EmailMessage(title, body, to=recepients)
    email.send()


def validate_schedule(x,y):
    slots=x.split(",")
    times=y.split(",")
    if len(slots) != len(times):
        return False
    for i in times:
        try:
            i=datetime.strptime(i, '%I:%M')
        except ValueError:
            print(i)
            return False
    return True



def mail_to_admins(message=None):
    admin_set=User.groups.filter(groups__name='TransportAdmin').values()
    emails=[]
    if admin_set.exists():
        for i in admin_set.iterator():
            emails.append(i.email)
    send_email(title='Transport Schedule Changed',body=message,recepients=emails)
