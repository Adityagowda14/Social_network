from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError("Email already exists")
        return value.lower()

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']
        user = User(
            email=email,
            username=username
        )
        user.set_password(validated_data['password'])
        user.save()
        return user