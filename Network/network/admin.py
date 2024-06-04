from django.contrib import admin
from .models import Post, User, Likes

class PostAdmin(admin.ModelAdmin):
    list_display = ('id','get_author_username', 'content', 'timestamp')

    def get_author_username(self, obj):
        return obj.author.username
    
    get_author_username.short_description = 'Author'
    
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'display_followers', 'display_following')
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ('followers', 'following')

    def display_followers(self, obj):
        return ", ".join([follower.username for follower in obj.followers.all()])
    display_followers.short_description = 'Followers'

    def display_following(self, obj):
        return ", ".join([following.username for following in obj.following.all()])
    display_following.short_description = 'Following'

admin.site.register(Post, PostAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Likes)