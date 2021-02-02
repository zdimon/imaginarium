from django.db import models
from django.utils.safestring import mark_safe



USER_STATES = (
    ("gessor", "gessor"),
    ("gessed", "gessed"),
    ("betor", "betor"),
    ("beted", "beted"),
    ("proposer", "proposer"),
    ("proposed", "proposed")
)

class Gameuser(models.Model):
    login = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=250)
    image = models.ImageField(upload_to='user_images',null=True,blank=True)
    sids = models.TextField(default='')
    is_online = models.BooleanField(default=False)
    state = models.CharField(max_length=10,
                            choices=USER_STATES,
                            default="betor")

    def __str__(self):
        return self.login

    def add_sid(self,sid):
        sids = self.sids.split(';')
        if sid not in sids:
            sids.append(sid)
        self.sids = ';'.join(sids)
        self.save()
        self.check_online()
        

    @staticmethod
    def remove_sid(sid):
        user = Gameuser.objects.get(sids__contains=sid)
        sids = user.sids.split(';')
        if sid in sids:
            sids.remove(sid)
        user.sids = ';'.join(sids)
        user.save() 
        user.check_online() 

    def set_online(self,value):
        if self.is_online != value:
            self.is_online = value
            self.save()
      
    
      

    def check_online(self):
        if(len(self.sids)>5):
            self.set_online(True)
        else:
            self.set_online(False)

    def save(self, *args, **kwargs):
        from game.utils import update_online_users_in_json
        super(Gameuser, self).save(*args, **kwargs)
        update_online_users_in_json()

class Card(models.Model):
    on_hand = models.BooleanField(default=False)
    image = models.ImageField(upload_to='user_images',null=True,blank=True)    

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width=100 />')


POSITION = (
    ("hand", "hand"),
    ("table", "table")
)

class Card2User(models.Model):
    user = models.ForeignKey(Gameuser,on_delete=models.CASCADE)
    card = models.ForeignKey(Card,on_delete=models.CASCADE)
    position = models.CharField(max_length=10,
                        choices=POSITION,
                        default="hand")
    is_right = models.BooleanField(default=False)

class Propose(models.Model):
    proposer = models.ForeignKey(Gameuser,on_delete=models.CASCADE,related_name='proposer')
    owner = models.ForeignKey(Gameuser,on_delete=models.CASCADE,related_name='owner')
    card = models.ForeignKey(Card,on_delete=models.CASCADE)
    
    is_right = models.BooleanField(default=False)