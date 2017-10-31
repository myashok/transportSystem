from django.forms import models

from main_site.models import Trip


class TripForm(models.ModelForm):
    class Meta:
        model=Trip
