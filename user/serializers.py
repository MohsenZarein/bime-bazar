from rest_framework import serializers
from django.contrib.auth import get_user_model


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('username', 'password',)
        extra_kwargs = {
            'password':{
                'write_only':True,
                'min_length':4
            }
        }
    

    def create(self, validated_data):
        """ Create a new user with encrypted password and return it """
        return get_user_model().objects.create_user(**validated_data)



class UserSerializer(serializers.ModelSerializer):
    """ Serilizer class for users """
    class Meta:
        model = get_user_model()
        fields = (
            'id', 'username','first_name',
            'last_name','email'
        )
        read_only_fields = ('id',)