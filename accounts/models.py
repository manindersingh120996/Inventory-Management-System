import email
from email.headerregistry import Address
import profile
import uuid
from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser,AbstractUser
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
import datetime
import os
# from base.emails import send_account_activation_email
# Create your models here.

def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('profile/', filename)     

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="profile")
    is_email_verified = models.BooleanField(default=True)
    email = models.CharField(max_length=100, null=True,blank=True)
    address = models.CharField(max_length=400,null=True,blank=True)
    phoneNumberRegex = RegexValidator(regex=r"^[6789]\d{9}$")
    contact = models.CharField(validators=[phoneNumberRegex],max_length=10)
    profile_image = models.ImageField(upload_to=filepath, null=True, blank=True)

    # def __self__(self):
    #     return self.email
    def __str__(self):
        return self.user.email


@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()


# @receiver(post_save,sender=User)
# def send_email(sender,instance,created,**kwargs):
#     try:
#         if created:
#             email_token=str(uuid.uuid4())
#             email = instance.email
#             send_account_activation_email(email,email_token)
#     except Exception as e:
#         print(e)
    
