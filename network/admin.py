from django.contrib import admin

# Register your models here.
from .models import User, Post


class PostAdmin(admin.ModelAdmin):
    def get_mentioned_users(self, obj):
        return [user.username for user in obj.mentioned_users.all()]
        # return "\n".join([p.mentioned_users for p in self.mentions.all()])

    list_display = ('user', 'timestamp', 'text', 'get_mentioned_users')


admin.site.register(User)
admin.site.register(Post, PostAdmin)
