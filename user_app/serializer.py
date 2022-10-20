from rest_framework import serializers

from user_app.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        write_only = ('password',)
