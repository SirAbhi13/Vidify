from rest_framework import serializers


class AuthenticationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(required=True)
