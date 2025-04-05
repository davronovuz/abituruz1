from django.db import models
import uuid

class Base(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    created_at=models.DateField(auto_now_add=True)
    Updated_at=models.DateField(auto_now=True)

    class Meta:
        abstract=True

