from django.db.models.signals import pre_save,post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver
from django.db import models
from accounts.models import profile
import string
import random

def get_post_image(instance, filename):
    img_path = '{0}/posts/{1}'.format(instance.user.username,filename)
    return img_path

def get_random_string():
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(12))
    return result_str

def update_user_total_post(process):
    user_profile = profile.objects.get(user=self.user)
    if process == 'inc':
        user_profile.total_posts += 1
    elif process == 'dec':
        user_profile.total_posts -= 1
    else:
        user_profile.total_posts = user_profile.total_posts
    user_profile.save()



class UserPost(models.Model):
    title           = models.TextField(max_length=60)
    image           = models.ImageField(upload_to=get_post_image,null=False,blank=False)
    caption         = models.TextField(max_length=5000,blank=True)
    date_published  = models.DateTimeField(auto_now_add=True,verbose_name='Date Published')
    user            = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    slug            = models.SlugField(blank=True,unique=True)

    def __str__(self):
        return str(self.user)+'->'+str(self.title)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        update_user_total_post('inc')



@receiver(post_delete,sender=UserPost)
def submission_delete(sender,instance,**kwargs):
    instance.image.delete(False)
    update_user_total_post('dec')

def pre_save_user_post(sender,instance,**kwargs):
    if not instance.slug:
        slug_string = get_random_string()
        instance.slug = slugify(instance.user.usename+slug_string)

    if not instance.title:
        instance.title = str(instance.image)

pre_save.connect(pre_save_user_post,sender=UserPost)
