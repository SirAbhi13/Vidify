from rest_framework import serializers


class AuthenticationSerializer(serializers.Serializer):
    """Serializer to validate /signup/ requests"""

    username = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(required=True)
