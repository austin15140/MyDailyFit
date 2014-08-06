from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
import os

def get_image_path(instance, filename):
    return os.path.join(str(instance), 'images', filename)

def get_video_path(instance, filename):
    return os.path.join(str(instance), 'videos', filename)

def get_randfile_path(instance, filename):
    return os.path.join(str(instance), 'file', filename)

class PersonalTrainer(models.Model):
    user = models.OneToOneField(User)
    is_Personal_Trainer = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    weight = models.CharField(max_length='3', default='', blank=True, null=True)
    age = models.CharField(max_length='2', default='', blank=True, null=True)
    tagline = models.TextField(default='A work in progress.', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    photo = models.FileField(upload_to=get_image_path, blank=True, null=True)
    bg_img = models.FileField(upload_to=get_image_path, blank=True, null=True)
    prof_img = models.FileField(upload_to=get_image_path, blank=True, null=True)
    video = models.FileField(upload_to=get_video_path, blank=True, null=True)
    rand_file = models.FileField(upload_to=get_randfile_path, blank=True, null=True)
    location = models.CharField(max_length='75', default='', blank=True, null=True)

    def photo_name(self):
        return os.path.basename(self.photo.name)

    def video_name(self):
        return os.path.basename(self.video.name)

    def get_p_extension(self):
        name, extension = os.path.splitext(self.photo.name)
        return extension

    def get_v_extension(self):
        name, extension = os.path.splitext(self.video.name)
        return extension

    def get_r_extension(self):
        name, extension = os.path.splitext(self.rand_file.name)
        return extension

    def __unicode__(self):
        return self.user.username

class UserFile(models.Model):
    file = models.FileField(upload_to=get_randfile_path, blank=True)
    profile = models.ForeignKey(UserProfile, unique=False)

    def file_name(self):
        return os.path.basename(self.file.name)

    def __unicode__(self):
        return self.profile.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)