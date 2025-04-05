from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models
from apps.utility.models import Base

#CONSTANT FIELDS
NEW,CODE,VERIFIED,DONE='new','code','verified','done'
STUDENT,TEACHER,ADMIN,SUPERADMIN='student','teacher','admin','superadmin'


class User(Base,AbstractUser):
    full_name = models.CharField(max_length=250,null=False,blank=False)
    password = models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    phone_regex=RegexValidator(
        phone_regex=r'^\+?1?\d{9,15}$',
        message="Telefon raqam +998(91)123-45-67 formatida bo'lishi kerak")
    phone=models.CharField(validators=[phone_regex], max_length=17, blank=True)
    avatar=models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    date_of_birth=models.DateTimeField(null=True,blank=True)

    USER_ROLES=(
        (STUDENT,STUDENT),
        (TEACHER,TEACHER),
        (ADMIN,ADMIN),
        (SUPERADMIN,SUPERADMIN),
    )
    user_role=models.CharField(max_length=20,choices=USER_ROLES,default=STUDENT)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table='users'
        verbose_name='user'
        verbose_name_plural='users'
        ordering=['created_at']

class Confirmation(Base):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, null=False, blank=False)
    auth_status = models.CharField(max_length=20, null=False, blank=False, default=NEW)
    is_confirmed = models.BooleanField(default=False)
    expired_time = models.DateTimeField(null=False, blank=False)
    attempts = models.IntegerField(null=False, blank=False, default=0)




