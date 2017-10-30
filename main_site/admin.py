from django.contrib import admin

# Register your models here.
from main_site.models import Driver, Vehicle, TransportRequest, RequestType, VehicleType, Trip, \
    TripStatus

admin.site.register(Driver)
admin.site.register(Vehicle)
admin.site.register(TransportRequest)
admin.site.register(RequestType)
admin.site.register(VehicleType)
admin.site.register(Trip)
admin.site.register(TripStatus)
