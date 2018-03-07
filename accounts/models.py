import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

def scramble_uploaded_image(instance, filename):
    extension = filename.split(".")[-1]
    return "profile/{}.{}".format(uuid.uuid4(), extension)


class ProfileManager(models.Manager):
    user_for_related_field = True

    def toggle_follow(self, username, to_toggle_user):
        profile, created = Profile.objects.get_or_create(user=username)
        if to_toggle_user in profile.following.all():
            profile.following.remove(to_toggle_user)
            added = False
        else:
            profile.following.add(to_toggle_user)
            added = True
        return added

    def is_following(self, username, followed_by_user):
        profile, created = Profile.objects.get_or_create(user=username)
        if created:
            return False
        if followed_by_user in profile.following.all():
            return True
        return False


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                to_field='username',
                                related_name='profile',
                                primary_key=True)
    name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=11, blank=True)
    address = models.CharField(max_length=100, blank=True)
    status_msg = models.CharField(max_length=100, blank=True)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name='followed_by',
                                       blank=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ProfileManager()

    def __str__(self):
        return "{}".format(self.user.username)

    @property
    def following_list(self):
        following = self.following.all()
        return following.exclude(username=self.user.username)

    @property
    def followed_by_list(self):
        followed_by = self.user.followed_by.all()
        return followed_by.exclude(user=self.user.username)

    @property
    def items_list(self):
        items = self.user.items.all()
        return items

    @property
    def profile_image(self):
        profile_image = self.profile_images.order_by('-created').first()
        if profile_image != None:
            profile_image = profile_image.image.url
        return profile_image


class ProfileImage(models.Model):
    profile = models.ForeignKey(Profile,
                                on_delete=models.CASCADE,
                                related_name='profile_images')
    image = models.ImageField(upload_to=scramble_uploaded_image)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} ({})'.format(self.profile.user.username, self.id)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
