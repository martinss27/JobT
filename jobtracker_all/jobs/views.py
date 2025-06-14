from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .filters import JobApplicationFilter
from .serializers import JobApplicationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import JobApplication

class JobApplicationCreateView(generics.CreateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)
    
    def perform_create(self,serializer):
        user = self.request.user
        last_job = JobApplication.objects.filter(user=user).order_by('-user_job_id').first()
        next_user_job_id = (last_job.user_job_id + 1) if last_job else 1
        serializer.save(user=user, user_job_id=next_user_job_id)

class JobApplicationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JobApplicationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = JobApplicationFilter
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)
    
class JobApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user_job_id'
    
    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)