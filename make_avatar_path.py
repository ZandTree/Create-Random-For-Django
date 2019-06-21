# path for media folder: Profile model with image attr
# 1.create path for upload_to = function
#2. adjust size of uploaded file and (if needed) its' name
# 3. plus signals

from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image


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
