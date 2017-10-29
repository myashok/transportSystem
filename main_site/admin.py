from django.contrib import admin

# Register your models here.
from main_site.models import Driver, Vehicle, TransportRequest, RequestType, RequestStatus

admin.site.register(Driver)
admin.site.register(Vehicle)
admin.site.register(TransportRequest)
admin.site.register(RequestType)
admin.site.register(RequestStatus)


