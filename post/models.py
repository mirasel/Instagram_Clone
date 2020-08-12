from django.db.models.signals import pre_save,post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver
from django.db import models
from accounts.models import profile
import string
import random

def get_post_image(instance, filename):
    img_path = '{0}/posts/{1}'.format(instance.uploader,filename)
    return img_path

def get_random_string():
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(12))
    return result_str

def update_user_total_post(process,user):
    user_profile = profile.objects.get(user=user)
    if process == 'inc':
        user_profile.total_posts += 1
    elif process == 'dec':
        user_profile.total_posts -= 1
    else:
        user_profile.total_posts = user_profile.total_posts
    user_profile.save()



class UserPost(models.Model):
    uploader        = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title           = models.TextField(max_length=50,blank=True)
    image           = models.ImageField(upload_to=get_post_image,null=False,blank=False)
    caption         = models.TextField(max_length=2000,blank=True)
    date_published  = models.DateTimeField(auto_now_add=True,verbose_name='Date Published')
    slug            = models.SlugField(blank=True,unique=True)
    likes           = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="post_likes")

    def __str__(self):
        return str(self.uploader)+'->'+str(self.title)

    def total_likes(self):
        return self.likes.count();

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        update_user_total_post('inc',self.uploader)



@receiver(post_delete,sender=UserPost)
def submission_delete(sender,instance,**kwargs):
    instance.image.delete(False)
    update_user_total_post('dec',instance.uploader)

def pre_save_user_post(sender,instance,**kwargs):
    slug_string = get_random_string()
    instance.slug = slugify(str(instance.uploader)+slug_string)
    instance.title = str(instance.image)

pre_save.connect(pre_save_user_post,sender=UserPost)


class PostComment(models.Model):
    post            = models.ForeignKey(UserPost,on_delete=models.CASCADE)
    commenter       = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    comment         = models.TextField(max_length=2000,blank=False,null=False)
    date_published  = models.DateTimeField(auto_now_add=True,verbose_name='Date Published')

    
    def __str__(self):
        return str(self.post)+' -> '+str(self.commenter)+' -> '+str(self.comment)[:len(self.comment)//2+1]
