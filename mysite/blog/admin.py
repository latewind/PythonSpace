from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug':('title',)}
    raw_id_fieds = ('author',)
    date_hieralrchy = 'publish'
    ordering = ['status', 'publish']



# Register your models here.

admin.site.register(Post, PostAdmin)