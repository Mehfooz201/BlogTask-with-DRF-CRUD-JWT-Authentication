from django.contrib import admin
from .models import BlogPost

# Register your models here.

@admin.register(BlogPost)
class PostModelAdmin(admin.ModelAdmin):
    list_display= ['id', 'title', 'content']