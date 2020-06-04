import django_filters

from .models import *

class indexFilter(django_filters.FilterSet):
    class Meta:
        model = AnimeTitle
        fields = [ 'title',]
