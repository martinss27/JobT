from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import serializers
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer): #register logic
    password = serializers.CharField(write_only=True)
    '''create a password field that doesn't show up in the serialization'''

    class Meta: #it will use the user model and only ask for user/email, the password is being handled above
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
            user = User(
                username=validated_data['username'],
                email=validated_data['email']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user
            

class LoginSerializer(serializers.Serializer): #login logic
    username = serializers.CharField() #requesting username
    password = serializers.CharField(write_only=True) #requesting password


    def validate(self,data): #validate takes the entered data and calls authenticate to check if the username and password are correct
        print("data received at login:", data)
        user = authenticate(**data) #takes the unpacked data parameter and passes it to authenticate
        if user and user.is_active: #first checks if user is not None and then if the user is active
            return user #if the user is active, returns the user
        raise serializers.ValidationError("Invalid credentials") #otherwise, returns an invalid credentials error