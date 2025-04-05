from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models
from apps.utility.models import BaseModel



# Constants Fields
NEW, CODE_VERIFIED, DONE = 'new', 'code_verified', 'done'
STUDENT, TEACHER, ADMIN, SUPER_ADMIN = 'student', 'teacher', 'admin', 'super_admin'

USER_ROLE_CHOICES = [
    (STUDENT, "Student"),
    (TEACHER, "Teacher"),
    (ADMIN, "Admin"),
    (SUPER_ADMIN, "Super Admin"),
]

STATUS_CHOICES = [
    (NEW, "New"),
    (CODE_VERIFIED, "Code Verified"),
    (DONE, "Done"),
]

class Account(BaseModel,AbstractUser):
    phone_relax = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    full_name = models.CharField(max_length=100, null=False, blank=False)
    user_role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default=STUDENT)
    date_of_birth = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NEW)
    phone_number = models.CharField(validators=[phone_relax], unique=True, max_length=17, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/',
                               null=True, blank=True,
                               validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'svg', 'gif'])])

    def __str__(self):
        return self.full_name


class UserConfirmation(BaseModel):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='confirmations')
    code = models.CharField(max_length=6)
    auth_status = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    expires_time = models.DateTimeField(null=True, blank=True, minutes=5)
    attempts = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user} - {self.code}"
