from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(default='Hi my name is ... ', max_length=355)

    def __str__(self) -> str:
        return self.first_name

class SavedCoin(models.Model):
    uuid = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    # Add the rest of the fields from the 'coin' dictionary in the same way
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

