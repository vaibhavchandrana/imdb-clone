from rest_framework import serializers 
from django.contrib.auth.models import User


class RegistrationSerializers(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password','password2']
        extra_kwargs={
            'password':{
                'write_only':True
            }
        }

    def save(self):
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        
        
 
        if password!=password2:
            raise serializers.ValidationError({'Error':"Passwords are not same"})
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'Error':"Please use unique email "})

        account=User(first_name=self.validated_data['first_name'],
        last_name=self.validated_data['last_name'],username=self.validated_data['username'],email=self.validated_data['email'])
        account.set_password(password)
        account.save()

        return account
