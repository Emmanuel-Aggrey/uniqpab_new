from django import  forms
from .models import  Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model =Review
        fields = '__all__'


class SignupForm(forms.Form):
    phone = forms.CharField(max_length=15,label='phone')
    address = forms.CharField(max_length=200,help_text='your addres',required=False)
    location = forms.CharField(max_length=200,help_text='your location')

    def signup(self,request,user):
        user.phone = self.changed_data['phone']
        user.address = self.changed_data['address']
        user.location = self.changed_data['location']