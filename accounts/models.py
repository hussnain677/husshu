from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='user/', default="user/default.png")
    number = models.CharField(null=True, blank=True, max_length = 12)

    def __str__(self):
        return "Profile of user {}".format(self.user.username)