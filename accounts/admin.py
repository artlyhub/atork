from django.contrib import admin

from accounts.models import Profile, ProfileImage


class ProfileImageTabularInline(admin.TabularInline):
    model = ProfileImage


class ProfileAdmin(admin.ModelAdmin):
    inlines = [ProfileImageTabularInline]

    class Meta:
        model = Profile

admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfileImage)
