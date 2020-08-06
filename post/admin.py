from django.contrib import admin
from .models import UserPost,PostComment,PostLike

# Register your models here.
admin.site.register(UserPost)
admin.site.register(PostComment)
admin.site.register(PostLike)
