from datetime import  datetime,date
import os
from smtplib import SMTPException
import threading

from django.core.files.base import ContentFile
#from weasyprint import HTML
from django.core.files import File
from main_site.models import Trip
from googletrans import Translator
from transport.settings import BASE_DIR, EMAIL_HOST_USER
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

PER_KM_RATE=4.5
PEAK_HOUR_START=datetime.strptime('18:00', '%H:%M').time()
PEAK_HOUR_END=datetime.strptime('6:00', '%H:%M').time()
NORMAL_RATE_PER_TWO_HOURS=150
PEAK_RATE_PER_TWO_HOURS=200

def calculate_fare(start_date,start_time,end_date,end_time,distance):
    time_diff=datetime.combine(end_date,end_time)-datetime.combine(start_date,start_time)
    fare_for_dist=distance*PER_KM_RATE
    fare_for_time=time_diff.days*(3*NORMAL_RATE_PER_TWO_HOURS+9*PEAK_RATE_PER_TWO_HOURS)
    if start_time>=PEAK_HOUR_START:
        fare_for_time+=((time_diff.seconds//3600)*PEAK_RATE_PER_TWO_HOURS)/2
    else:
        fare_for_time+=((time_diff.seconds//3600)*NORMAL_RATE_PER_TWO_HOURS)/2

    return fare_for_dist,fare_for_time

class MP3Generation(threading.Thread):
    def __init__(self,trip):
        self.trip=trip
        threading.Thread.__init__(self)
    def run(self):
        from gtts import gTTS

        import os
        mytext = 'You have to report at '+self.trip.request.source+' on '+\
                 str(self.trip.request.start_date)+' at '+str(self.trip.request.start_time)\
                 +'with vehicle '+self.trip.vehicle.registration_no
        translator = Translator()
        x = translator.translate(mytext, dest='hi')
        language = 'hi'

        myobj = gTTS(text=x.text, lang=language, slow=False)

        myobj.save(str(self.trip.driver_id)+'_'+str(self.trip.id)+'.mp3')


        # trip=Trip.objects.get(id=self.trip.id)
        # fh = open(str(self.trip.id)+'.mp3', "r")
        # if fh:
        #     # Get the content of the file
        #     file_content = ContentFile(fh.read())
        #     # Set the media attribute of the article, but under an other path/filename
        #     trip.audiofile.save(, file_content)
        #     # Save the article
        #     new_article.save()
        # Close the file and delete it
        #fh.close()


def generate_mp3(trip):
    MP3Generation(trip).start()


