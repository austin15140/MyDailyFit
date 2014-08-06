from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from users.models import UserProfile, PersonalTrainer

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'

class UserTypeInline(admin.StackedInline):
    model = PersonalTrainer
    can_delete = False
    verbose_name_plural = 'User Type'

class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, UserTypeInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

