from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):

    def _create_user(self, nickname, email, password, **kwargs):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, nickname, email, password, **kwargs):
        kwargs.setdefault('is_admin', False)
        if kwargs['is_admin']:
            kwargs['is_staff'] = True
        else:
            kwargs.setdefault('is_staff', False)
        return self._create_user(nickname, email, password, **kwargs)

    def create_superuser(self, nickname, email, password, **kwargs):

        kwargs['is_staff'] = True
        kwargs['is_admin'] = True

        return self._create_user(nickname, email, password, **kwargs)
