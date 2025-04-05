from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.utility.models import Base
from django.core.validators import FileExtensionValidator,RegexValidator


#CONSTANT FIELDS
NEW,CODE_VERIFIED,DONE='new','code_verified','done'
STUDENT,TEACHER,ADMIN,SUPERADMIN='student','teacher','admin','superadmin'
EXPIRATION_TIME=2

class User(Base,AbstractUser):
    phone_regex=RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Telfon raqam +998901234567 formatda bo'lishi kerak")
    full_name=models.CharField(max_length=255,null=False,blank=False)
    phone=models.CharField(validators=[phone_regex],max_length=17,unique=True)
    avatar=models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg','png','jpeg','webp','gif','jfif'])]
        )
    date_of_birth=models.DateField(null=True,blank=True)

    USER_ROLES = (
        (STUDENT, STUDENT),
        (TEACHER, TEACHER),
        (ADMIN, ADMIN),
        (SUPERADMIN, SUPERADMIN),
    )
    user_role=models.CharField(max_length=20,choices=USER_ROLES,default=STUDENT)
    def __str__(self):
        return self.full_name

    class Meta:
        db_table='users'
        verbose_name='user'
        verbose_name_plural='users'
        ordering=['created_at']










