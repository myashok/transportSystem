from django.contrib import admin

# Register your models here.
from main_site.models import Driver, Vehicle, Request, Bill, Announcement, Trip, Status

admin.site.register(Driver)
admin.site.register(Vehicle)
admin.site.register(Request)
admin.site.register(Bill)
admin.site.register(Trip)
admin.site.register(Announcement)
admin.site.register(Status)
