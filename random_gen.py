#C:\Users\tanja\Desktop\projects_help

import random
import string



def make_random_id(chars=(string.ascii_uppercase +string.digits),size=4):
    """
    return string made of random (ascii-chars,digits)of length = size
    """
    output = [random.choice(chars) for _ in range(size)]
    return "".join(output)

print(make_random_id())
print(make_random_id())
print(make_random_id())

# using upper and lower case ascii

def rand_string(n):
    """
    return a string from ascii chars with random letters and numbers
    """
    mix = string.ascii_letters + string.digits
    final_string = [random.choice(mix) for item in range(n)]
    return "".join(final_string)

# info about dif instance.__class__(vs instance.__class__.__name__
"""
>>> s = A()
>>> one = s.__class__         # type(class)
>>> one
<class '__main__.A'> 
>>> two = s.__class__.__name__
>>> two
'A'                           #type(string)
>>>
"""



def create_profile_uid(instance):
    """
    create unique id for instance based on random letters and digits
    which have attr = uid
    """
    klass = instance.__class__
    start_unid = rand_string(4)
    if klass.objects.filter(unid=start_unid).exists():
        instance.unid = rand_string(4)
        return create_profile_uid(instance)
    return start_unid


def make_avatar(instance,file):
    
    """
    make path to uploaded file (avatar) and adjust file name if needed

    """
    time = timezone.now().strftime("Y-%m-%d")
    tail = file.split('.')[-1]
    head = file.split('.')[0]
    if len(head) >10:
        head = head[:10]
    file_name = head + '.' + tail
    user_folder = instance.user_id
    return  os.path.join('avatars',user_folder,file_name)

# example of Profile model

from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    avatar = models.ImageField(blank=True,null=True,upload_to=make_avatar)


    def __str__(self):
        return self.user.username
    
      
    def get_absolute_url(self):
        return reverse('profiles:profile',kwargs={'pk':self.user_id})
    
    @property
    def get_ava_path(self,*args,**kwargs):
        if self.avatar:
            return '/media/{}'.format(self.avatar)
        else:
            return '/static/img/day.jpg/'

    def save(self,*args,**kwargs):
        print('save method profile calling')
        super().save(*args,**kwargs)
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height >200 or img.width >200:
                output_size = (200,200)
                img.thumbnail(output_size)
                img.save(self.avatar.path)


# 2 signals: simalt creation User obj ==> Profile obj

# def created_profile(sender,instance,created,*args,**kwargs):
#     if created and instance.email:
#         print('creating a profile for this user')
#         Profile.objects.get_or_create(user=instance,email=instance.email)
# post_save.connect(created_profile,sender=User)

@receiver(post_save,sender = User)
def create_user_profile(sender,instance,created,**kwargs):
    """As New User created, create Profile"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    """As New User created, save Profile"""
    instance.profile.save()

