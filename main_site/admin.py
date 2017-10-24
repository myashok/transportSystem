from django.contrib import admin

# Register your models here.
from main_site.models import Driver, Vehicle, Request, RequestType, RequestStatus

admin.site.register(Driver)
admin.site.register(Vehicle)
admin.site.register(Request)
admin.site.register(RequestType)
admin.site.register(RequestStatus)


