from django.db import models
from django.conf import settings

def get_image_path(instance,filename):
    return '{0}/{1}'.format(instance.user.username,filename)

class profile(models.Model):

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('custom', 'Custom'),
        ('nottosay', 'Prefer Not To Say'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    bio = models.TextField(max_length=150,default="")
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES,default='nottosay')
    profile_pic = models.ImageField(upload_to=get_image_path,
                    default='defaultPic/default_profile_pic.jpg')
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    total_posts = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)