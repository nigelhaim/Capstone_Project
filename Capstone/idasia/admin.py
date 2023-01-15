from django.contrib import admin
from .models import User, Profile, idea, category, thread, proj_files, replies
# Register your models here.

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(idea)
admin.site.register(category)
admin.site.register(thread)
admin.site.register(proj_files)
admin.site.register(replies)