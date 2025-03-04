from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Records

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Records
        fields = ['added', 'type', 'size', 'sphere', 'currency', 'user_id']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            validated_data.pop('password')
        return super().update(instance, validated_data)