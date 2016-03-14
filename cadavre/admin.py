from django.contrib import admin

from cadavre.models import Cadavre, Sentance, UserProfile

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

@admin.register(Cadavre)
class Cadavre(admin.ModelAdmin):
	pass

@admin.register(Sentance)
class Sentance(admin.ModelAdmin):
	pass
		

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
