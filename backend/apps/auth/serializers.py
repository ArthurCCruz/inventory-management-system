from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, trim_whitespace=False, required=True)