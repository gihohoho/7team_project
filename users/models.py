from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, mbti, tmi, blog, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email or not password or not username:
            raise ValueError('Users must have an email address and password and username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            mbti=mbti,
            tmi=tmi,
            blog=blog,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
            mbti=None,   # createsuperuser 명령어 입력시 나오는 과정에 mbti,tmi,blog 값을 넣어주는 방법을 몰라 그냥 임의로 None값을 집어넣어줌
            tmi=None,
            blog=None,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        verbose_name='Username',
        max_length=30,
        unique=True
    )
    last_login = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name='last login')
    date_joined = models.DateTimeField(
        auto_now_add=True, verbose_name='date joined')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    mbti = models.CharField(max_length=4, null=True, blank=True)
    tmi = models.TextField(null=True, blank=True)
    blog = models.EmailField(unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
