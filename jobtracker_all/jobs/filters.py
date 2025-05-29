import django_filters
from .models import JobApplication

class JobApplicationFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr='icontains')
    company = django_filters.CharFilter(lookup_expr='icontains')
    position = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = JobApplication
        fields = ['status', 'company', 'position']