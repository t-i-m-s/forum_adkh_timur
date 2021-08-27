from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from .managers import UserManager
from forum_adkh_timur.settings import USER_AVATAR_IMAGE_PATH as path2avatars


class BaseUser(AbstractBaseUser):
    nickname = models.CharField('nickname', max_length=100, unique=True,
                                blank=False)
    email = models.EmailField('authentication email', max_length=128,
                              blank=False, unique=True, primary_key=True)
    password = models.CharField('authentication password', blank=False,
                                max_length=255)
    is_staff = models.BooleanField('is staff', default=False)
    is_admin = models.BooleanField('is admin', default=False)
    is_active = models.BooleanField('active', default=True)

    # def save(self, *args, **kwargs):  # для поля slug
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     return super().save(*args, **kwargs)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def user_is_staff(self):
        return self.is_staff

    @property
    def user_is_admin(self):
        return self.is_admin

    def about_user(self):
        return self.user_info.about_user

    about_user.admin_order_field = 'about_user'


def user_avatar_image_path(user_info, filename):
    return ''.join((path2avatars, 'user_{0}/{1}'.format(user_info.user.nickname, filename)))


class UserInfo(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE,
                                primary_key=True, related_name="user_info")
    age = models.IntegerField(null=True)
    country = models.CharField(max_length=30, blank=True)
    job = models.CharField(max_length=30, blank=True)
    about_user = models.TextField(blank=True)
    avatar = models.FileField(upload_to=user_avatar_image_path, blank=True)
