from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models
from apps.utility.models import BaseModel
from django.contrib.auth.models import AbstractUser

# CONSTANTS_FIELDS
NEW, CODE_VERIFIED, DONE = "new", "code_verified", "done"
STUDENT, TEACHER, ADMIN, SUPER_ADMIN = "student", "teacher", "admin", "super_admin"




class Account(BaseModel, AbstractUser):

    full_name = models.CharField(max_length=255, null=False, blank=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Telefon raqam quyidagi tartibda yozilishi kerak: +998901234567")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, null=False, blank=False)
    date_of_birth = models.DateField(null=False, blank=False)
    avatar = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "png", "jpeg", "webp", "gif", "jfif"])
        ]
    )

    USER_ROLE_CHOICES = (
        (STUDENT, "STUDENT"),
        (TEACHER, "TEACHER"),
        (ADMIN, "ADMIN"),
        (SUPER_ADMIN, "SUPER_ADMIN"),
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
    expired_time = models.DateTimeField(null=False, blank=False)
    attempts = models.IntegerField(null=False, blank=False, default=0)