from django.forms import ModelForm
from game.models import Gameuser

# Create the form class.
class GameuserForm(ModelForm):
    class Meta:
        model = Gameuser
        fields = ['login', 'password', 'image'] 

        