from rest_framework import serializers
from .models import JobApplication, User

class JobApplicationSerializer(serializers.ModelSerializer):
    user_job_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = JobApplication
        fields = ['id', 'user_job_id', 
                  'title', 'company', 'position', 'status', 
                  'applied_date', 'notes', 'interview_feedback', 
                  'next_step']
        read_only_fields = ['id']

class UserSerializer(serializers.ModelSerializer):
    job_applications = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'job_applications']
        read_only_fields = ['id']

    def get_job_applications(self, obj):
        jobs = obj.job_applications.order_by('user_job_id')
        return JobApplicationSerializer(jobs, many=True).data