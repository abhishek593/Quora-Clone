from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.core.validators import RegexValidator


class QuoraUserManager(BaseUserManager):
    def create_user(self, username, email, date_of_birth, first_name, last_name, password=None, description=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            username=username,
            first_name=first_name,
            last_name=last_name,
            description=description,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, date_of_birth, first_name, last_name, password, description=None):
        user = self.create_user(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            description=description
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


USERNAME_REGEX = '^[a-zA-Z0-9.@+-]*$'


class UserFollowing(models.Model):
    # This field contains main user
    user_id = models.ForeignKey('QuoraUser', related_name='following', on_delete=models.CASCADE)
    #This field contains all the people whom one is following
    following_user_id = models.ForeignKey('QuoraUser', related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_id', 'following_user_id',)


class QuoraUser(AbstractBaseUser):
    username = models.CharField(max_length=120,
                                unique=True,
                                validators=[RegexValidator(
                                    regex=USERNAME_REGEX,
                                    message="Username must be alphanumeric or contain any of the following '@ . + -' ",
                                    code='invalid_username',
                                ), ])
    email = models.EmailField(
        verbose_name='email address',
        max_length=255, unique=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)
    # profile_image = models.ImageField(blank=True)

    objects = QuoraUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth', 'first_name', 'last_name', 'username', 'description']

    def __str__(self):
        return self.email


    @property
    def get_followers(self):
        followers = []
        for person in self.followers.all():
            followers.append(person.user_id)
        return followers

    @property
    def get_following(self):
        following = []
        for person in self.following.all():
            following.append(person.following_user_id)
        return following

    @property
    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def get_short_name(self):
        return self.first_name


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True









