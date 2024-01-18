from django.contrib import admin

# Register your models here.


# main/admin.py
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'

from .models import Post, Like, Comment

from django.contrib import admin
from .models import Like

admin.site.register(Like)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'content', 'created_at')
    search_fields = ['post__title', 'content']
    list_filter = ('created_at',)


# company registeration
from .models import CompanyRegistration
admin.site.register(CompanyRegistration)


# seller_registertion

from .models import Company
admin.site.register(Company)
