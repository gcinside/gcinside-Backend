from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ngettext_lazy as _

from .utils import random_name_generator


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    profile_image = models.ImageField(
        blank=True,
        null=True,
        upload_to="user_profile",
        default="user_profile/default.jpg",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["USERNAME_FILED"]

    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = random_name_generator()
            while User.objects.filter(username=self.username):
                self.username = random_name_generator()
        super(User, self).save()


class ReportUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="report")
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    reported_at = models.DateTimeField()

    def __str__(self) -> str:
        return "report " + self.user.username
