from datetime import timedelta
import random
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models
from django.utils import timezone
import uuid
from ..utility.models import Base




NEW, CODE_VERIFIED, DONE = 'new', 'code_verified', 'done'
STUDENT, TEACHER, ADMIN, SUPER_ADMIN = 'student', 'teacher', 'admin', 'super_admin'

USER_ROLE_CHOICES = [
    (STUDENT, "Student"),
    (TEACHER, "Teacher"),
    (ADMIN, "Admin"),
    (SUPER_ADMIN,
    "Super Admin"),
]

STATUS_CHOICES = [
    (NEW, "New"),
    (CODE_VERIFIED, "Code Verified"),
    (DONE, "Done"),
]




class User(AbstractUser,Base):
    phone_relax = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Telefon raqam formati +998954443424 bo`lishi kerak.")
    full_name=models.CharField(max_length=250,null=False,blank=False)
    phone_number = models.CharField(validators=[phone_relax], unique=True, max_length=17, null=True, blank=True)
    user_role= models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default=STUDENT)
    birth_date=models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NEW)
    avatar = models.ImageField(upload_to='avatars/',
                               null=True, blank=True,
                               validators=[
                                   FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'svg', 'gif'])])

    def __str__(self):
        return self.username



    def create_verify_code(self,verify_type): #kod yaritadigan qismi
        code="".join([str(random.randint(0,100)%10)for _ in range(4)]) # bu yerda random orqali aniqlab oladi
        UserConfirmation.objects.create( # keyin UserConfirmation modeli chaqiriladi
            user=self,
            code=code,
        )
        return code

    def check_username(self):  # usernamega taxminiy username yaratib beradi
        if not self.username:
            temp_username = f"app{uuid.uuid4().__str__().split('-')[-1]}"  # id yaratilgandan keyin oxirgi raqamdan tashkil topadi
            while User.objects.filter(username=temp_username):  # yartatilgan usernamga random orqali yana son qoyiladi
                temp_username += f"{temp_username}{random.randint(1, 100)}"
            self.username = temp_username


    def check_pass(self):  # parol ham usernamega o`xshab yaratib olinadi
        if not self.password:
            temp_password=f"app{uuid.uuid4().__str__().split('-')[-1]}"
            self.password=temp_password

    def hashing_pass(self): #parol heshlanganligini tekshiradi
        if not self.password.startswith("pbkdf2_sha256"):
            self.set_password(self.password)

    # def token(self):    #refresh va access tokin uchun funksiya
    #     refresh=RefreshToken.for_user(self)
    #     return {
    #         "access":str(refresh.access_token),
    #         "refresh":str(refresh)
    #     }

    def clean(self):
        self.check_pass()
        self.hashing_pass()
        self.check_username()

    def save(self, *args, **kwargs):
        self.clean()
        super(User,self).save(*args,**kwargs)





EXPIRE_TIME=timedelta(minutes=2)

class UserConfirmation(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    auth_status=models.BooleanField(default=False)
    is_confirmed=models.BooleanField(default=False)
    expires_time = models.DateTimeField(null=True, blank=True, minutes=5)
    attempts = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user} - {self.code}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expires_time=timezone.now() + EXPIRE_TIME
        super().save(*args, **kwargs)
