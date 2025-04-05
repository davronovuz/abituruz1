from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models
from apps.utility.models import Base
from django.contrib.auth.models import AbstractUser



NEW,CODE_VERIFIED,DONE='new','code_verified','done'
STUDENT,TEACHER,ADMIN,SUPERADMIN='student','teacher','admin','superadmin'

class User(AbstractUser,Base):

    USER_STATUS=(
        (NEW,NEW),
        (CODE_VERIFIED,CODE_VERIFIED),
        (DONE,DONE)
    )

    USER_ROLES=(
        (STUDENT,STUDENT),
        (TEACHER,TEACHER),
        (ADMIN,ADMIN),
        (SUPERADMIN,SUPERADMIN)
    )
    phone_regex=RegexValidator(
        regex='',
        message="Telefon raqam +998995757473 formatda bo`lishi kerak"

    )
    full_name=models.CharField(max_length=255,null=False,blank=False)
    auth_status=models.CharField(max_length=30,choices=USER_STATUS,default=NEW)
    user_roles=models.CharField(max_length=30,choices=USER_ROLES,default=STUDENT)
    phone_number = models.CharField(validators=[phone_regex],max_length=17,unique=True)
    data_of_birth=models.DateField(auto_now=True)
    avatar=models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg','png','jpeg','webp','gif','jfif'])]
    )

    def __str__(self):
        return self.full_name

    class Meta:
        db_table='users'
        verbose_name='user'
        verbose_name_plural='users'
        ordering=['created_at']

class UserConfirmation(Base, User):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
    auth_status = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    expires_time = models.DateTimeField(null=True, blank=True)
    attempts = models.PositiveIntegerField(default=0)

    def str(self):
        return f"{self.user} - {self.code}"




