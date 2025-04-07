from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models
from apps.utility.models import BaseModel
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

# CONSTANTS_FIELDS

NEW, CODE_VERIFIED, DONE = "new", "code_verified", "done"
STUDENT, TEACHER, ADMIN, SUPER_ADMIN = "student", "teacher", "admin", "super_admin"
EXPIRATION_TIME = 2


class Account(BaseModel, AbstractUser):
    full_name = models.CharField(max_length=255, null=False, blank=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Telefon raqam quyidagi tartibda yozilishi kerak: +998901234567")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, null=False, blank=False, unique=True)
    date_of_birth = models.DateField(null=False, blank=False)
    avatar = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True,
        default="avatars/default.png",
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "png", "jpeg", "webp", "gif", "jfif"])
        ]
    )

    USER_ROLE_CHOICES = (
        (STUDENT, STUDENT),
        (TEACHER, TEACHER),
        (ADMIN, ADMIN),
        (SUPER_ADMIN, SUPER_ADMIN),
    )

    user_role = models.CharField(max_length=30, choices=USER_ROLE_CHOICES, default=STUDENT)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "account"
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ["-created_at"]


class UserConfirmation(BaseModel):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, null=False, blank=False)
    auth_status = models.CharField(max_length=20, null=False, blank=False, default=NEW)
    is_confirmed = models.BooleanField(default=False)
    expired_time = models.DateTimeField(null=True, blank=True)
    attempts = models.IntegerField(null=False, blank=False, default=0)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expired_time = timezone.now() + timedelta(minutes=EXPIRATION_TIME)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expired_time

    def __str__(self):
        return f"Confirmation for {self.user.phone_number}"

    class Meta:
        db_table = "user_confirmations"
        verbose_name = "Foydalanuvchi tasdiqlash"
        verbose_name_plural = "Foydalanuvchi tasdiqlashlari"
        ordering = ["-created_at"]