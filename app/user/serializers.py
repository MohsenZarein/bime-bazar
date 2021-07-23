from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


class CreateUserSerializer(serializers.ModelSerializer):
    """ serializer class for creating a new user """
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



class LoginSerializer(serializers.Serializer):
    """ serializer class for logging user """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):

        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )

        if not user:
            msg = 'Unable to authenticate with provided credetials'
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs

        
