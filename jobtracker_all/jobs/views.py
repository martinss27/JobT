from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import JobApplicationSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
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

class JobApplicationListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JobApplicationSerializer

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class JobApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user_job_id'
    
    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)