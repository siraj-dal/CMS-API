from django.db import models


# TODO :: Create Model for User Details
class info_user(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=8)
    creation_date = models.DateTimeField(auto_now=True)

# TODO :: Create Model for Post/Blog Details
class post_blog(models.Model):
    post_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.CharField(max_length=50)
    post_type = models.CharField(max_length=50)
    publish_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(blank=True, null=True)

# TODO :: Create Model for Like Details
class like_data(models.Model):
    like_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    post_id = models.IntegerField()
    likes = models.IntegerField(max_length=50)
    dislikes = models.IntegerField(max_length=50)
    creation_date = models.DateTimeField(auto_now=True)
