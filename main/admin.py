from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ForumUser, Post, Entry
from .forms import SignUpForm, ForumUserChangeForm


# Register your models here.

class ForumAdmin(UserAdmin):
    add_form = SignUpForm
    form = ForumUserChangeForm
    model = ForumUser
    list_display = ['username']


admin.site.register(ForumUser, ForumAdmin)
admin.site.register(Post)
admin.site.register(Entry)
