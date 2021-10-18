from django.contrib import admin
from .models import *


# Used to add likes to posts via django admin
class PostLikeAdmin(admin.TabularInline):
    model = PostLike


# Adds search functionality in django admin
class PostAdmin(admin.ModelAdmin):
    inlines = [PostLikeAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['user__email', 'title', 'description']

    class Meta:
        model = Post


# Used to add likes to comments via django admin
class CommentLikeAdmin(admin.TabularInline):
    model = CommentLike


# Adds search functionality in django admin
class CommentAdmin(admin.ModelAdmin):
    inlines = [CommentLikeAdmin]
    list_display = ['__str__', 'post']
    search_fields = ['user', 'detail', 'post']


admin.site.register(Product)
admin.site.register(Article)
admin.site.register(Template)
admin.site.register(Star)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile)

