from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Define 'password' as a write-only field

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'password', 'full_name',
                  'phone_number', 'address', 'city', 'country', 'date_of_birth')
        extra_kwargs = {'password': {'write_only': True}}  # Ensure 'password' is write-only

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            username=validated_data['username'],
            full_name=validated_data['full_name'],
            phone_number=validated_data['phone_number'],
            address=validated_data['address'],
            city=validated_data['city'],
            country=validated_data['country'],
            date_of_birth=validated_data['date_of_birth']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
