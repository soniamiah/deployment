import django_filters
from .models import Profile




class ProfileFilter(django_filters.FilterSet):

    class Meta:
        model = Profile
        fields = ( 'gender', 'birth_date')
