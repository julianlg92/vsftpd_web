from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

import uuid


class AccountManager(BaseUserManager):

    def create_user(self, username, label, password=None, **kwargs):
        if not username:
            raise ValueError("Username is required")

        user = self.model(username=username, label=label, **kwargs)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, label, password, **kwargs):
        user = self.create_user(
            username=username,
            password=password,
            label=label
        )

        user.is_enabled = True
        user.is_superuser = True
        user.is_moderator = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class AccountGroupModel(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def __str__(self):
        return self.name


class AccountModel(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=15, unique=True)
    label = models.CharField(max_length=40, )
    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True)
    group = models.ForeignKey(AccountGroupModel, null=True, on_delete=models.SET_NULL, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['label']

    objects = AccountManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.label

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        super(AccountModel, self).save(*args, **kwargs)
