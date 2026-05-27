from rest_framework import serializers


class APITokenReturnSerializer(serializers.Serializer):
    auth_token = serializers.CharField()
