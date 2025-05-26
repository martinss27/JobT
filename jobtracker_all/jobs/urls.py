from django.urls import path
from .views import JobApplicationCreateView, JobApplicationListView, JobApplicationDetailView

urlpatterns = [
    path('job-create/', JobApplicationCreateView.as_view(), name='job-application-create'),
    path('job-list/', JobApplicationListView.as_view(), name='job-application-list'),
    path('job-list/<int:user_job_id>/', JobApplicationDetailView.as_view(), name='job-application-detail'),
]