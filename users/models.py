from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class userprofileinfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.DO_NOTHING) #link our model to users model from admin
    
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(blank=True ,upload_to='profile_pics')

    def __str__(self):
        return self.user.username