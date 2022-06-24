from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3


class ContactForm(forms.Form):
    asunto = forms.CharField(max_length=300, widget=forms.TextInput(attrs={'class': 'input'}))
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'input'}))
    correo = forms.EmailField(max_length=150, widget=forms.TextInput(attrs={'class': 'input'}))
    mensaje = forms.CharField(max_length=2000, widget=forms.Textarea(attrs={'class': 'textarea'}))
    captcha = ReCaptchaField(widget=ReCaptchaV3)
