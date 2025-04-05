from django.core.validators import RegexValidator, FileExtensionValidator
from apps.utility.models import BaseModel
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


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



class UserConfirmation(models.Model):
    AUTH_STATUS_CHOICES = (
        ('NEW', 'New'),
        ('PENDING', 'Pending'),
        ('VERIFIED', 'Verified'),
        ('EXPIRED', 'Expired'),
    )

    user = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='confirmations')
    code = models.CharField(max_length=6, null=False, blank=False)
    auth_status = models.CharField(
        max_length=20,
        choices=AUTH_STATUS_CHOICES,
        default='NEW',
        null=False,
        blank=False
    )
    is_confirmed = models.BooleanField(default=False)
    expired_time = models.DateTimeField(null=False, blank=False)
    attempts = models.PositiveIntegerField(default=0, null=False, blank=False)


    class Meta:
        verbose_name = "User Confirmation"
        verbose_name_plural = "User Confirmations"
        unique_together = ['user', 'code']

    def __str__(self):
        return f"{self.user} - {self.code} ({self.auth_status})"

    def is_expired(self):
        return timezone.now() > self.expired_time

    def increment_attempts(self):
        self.attempts += 1
        self.save(update_fields=['attempts'])


