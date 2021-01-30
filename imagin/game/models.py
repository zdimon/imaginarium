from django.db import models


class Gameuser(models.Model):
    login = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=250)
    image = models.ImageField(upload_to='user_images',null=True,blank=True)
    sids = models.TextField(default='')
    is_online = models.BooleanField(default=False)

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
        from game.utils import update_online_users_in_json
        if self.is_online != value:
            self.is_online = value
            self.save()
        update_online_users_in_json()
    
      

    def check_online(self):
        if(len(self.sids)>5):
            self.set_online(True)
        else:
            self.set_online(False)