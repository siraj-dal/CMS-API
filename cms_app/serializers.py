from rest_framework import serializers
from .models import *

class info_usersSerializer(serializers.Serializer):
    # id = serializers.IntegerField()
    # user_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=8,min_length=8,style={'input-type':'password','placeholder':'Password'})

    def create(self, validated_data):
        return info_user.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # instance.user_id = validated_data.get('user_id',instance.user_id)
        instance.name = validated_data.get('name',instance.name)
        instance.email = validated_data.get('email',instance.email)
        instance.password = validated_data.get('password',instance.password)
        instance.save()
        return instance

    # class Meta:
    #     model = post_blog
    #     fields = ['user_id', 'name', 'email', 'password', 'creation_date']

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = post_blog
        # fields = ['post_id', 'user_id', 'title', 'description', 'content', 'post_type', 'publish_date', 'update_date']
        fields = [field.name for field in post_blog._meta.get_fields()]
