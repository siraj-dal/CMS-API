from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(info_user)
class info_usersAdmin(admin.ModelAdmin):
    list_display = ['user_id','name','email','password', 'creation_date']


@admin.register(post_blog)
class post_blogAdmin(admin.ModelAdmin):
    list_display = ['post_id', 'user_id', 'title','description','content', 'post_type', 'publish_date', 'update_date']


@admin.register(like_data)
class like_dataAdmin(admin.ModelAdmin):
    list_display = ['like_id', 'user_id', 'post_id', 'likes', 'creation_date']