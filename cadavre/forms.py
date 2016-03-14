 # -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from cadavre.models import UserProfile, Cadavre, Sentance
from django.core.validators import RegexValidator
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.forms import PasswordResetForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

from django.core.exceptions import ValidationError

class UserLoginForm(forms.Form):

    username = forms.CharField(label="PSEUDONYME", widget=forms.TextInput(attrs={'placeholder': 'Identifiant'}), 
        max_length=40, error_messages={'required': 'Champs vide !'})
    password = forms.CharField(label="MOT DE PASSE", widget=forms.PasswordInput(attrs={'placeholder': 'Mot de Passe'}), 
        error_messages={'required': 'Champs vide !'})

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = False
        self.fields['password'].label = False



class UserForm(ModelForm):
    error_messages = {
        'password_mismatch': ("Veuillez entrer deux mots de passe identiques."),
    }

    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Prénom'}), error_messages={'required': 'Champs vide !'})
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nom'}), error_messages={'required': 'Champs vide !'})
    username = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'placeholder': 'Identifiant'}), 
        error_messages={'required': 'Champs vide !', 'unique': 'Ce pseudonyme appartient à un autre utilisateur'})
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}), error_messages={'required': 'Champs vide !'})
    password1 = forms.CharField(error_messages={'required': 'Champs vide !'}, widget=forms.PasswordInput(attrs={'placeholder': 'Mot de Passe'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmation'}), error_messages={'required': 'Champs vide !'})

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password1", "password2","email"]

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = False
        self.fields['last_name'].label = False
        self.fields['username'].label = False
        self.fields['email'].label = False
        self.fields['password1'].label = False
        self.fields['password2'].label = False

    def clean_password2(self):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.is_active = False
            user.save()

        return user

    def clean_email(self):

        data = self.cleaned_data['email']

        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email already used")

        return data

    

class UserProfileForm(forms.ModelForm):

    phone_number = forms.CharField(label="Telephone", widget=forms.TextInput(attrs={'placeholder': 'Téléphone'}), 
        error_messages={'incomplete': 'Entrez un numero de téléphone'}, validators=[RegexValidator(r'^\+?1?\d{9,10}$', 'Numéro invalide')])
    avatar = forms.ImageField(required=False)
    birthday = forms.DateField(label="Naissance", required=False, widget= SelectDateWidget(years=range(2015, 1900, -1)))
    

    class Meta:
        model = UserProfile
        fields = ["phone_number", "birthday", "avatar"]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].label = False
        self.fields['avatar'].label = False
        self.fields['birthday'].label = False


class EmailResetPassForm(forms.ModelForm):

    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}), error_messages={'required': 'Champs vide !'})

    class Meta:
        model = User
        fields = ["email"]

    def clean_email(self):

        data = self.cleaned_data['email']

        if User.objects.filter(email=data).exists() is not True:
            raise forms.ValidationError("utilisateur inexistant")

        return data

    def __init__(self, *args, **kwargs):
        super(EmailResetPassForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = False

class ResetPassForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': ("Veuillez entrer deux mots de passe identiques."),
    }
    
    password1 = forms.CharField(label= ("Mot de passe"), widget=forms.PasswordInput(attrs={'placeholder': 'password1'}), 
        error_messages={'required': 'Champs vide !'})
    password2 = forms.CharField(label= ("Confirmation"), widget=forms.PasswordInput(attrs={'placeholder': 'password2'}), 
        error_messages={'required': 'Champs vide !'})

    class Meta:
        model = User
        fields = ["password1", "password2"]


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        return password2

    def __init__(self, *args, **kwargs):
        super(ResetPassForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = False
        self.fields['password2'].label = False

class NewCadavreForm(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Titre'}), error_messages={'required': 'Champs vide !'})
    sentance_max = forms.IntegerField(label="Nombre de participants", widget= forms.NumberInput(attrs={'placeholder': '3 personnes minimum'}))

    class Meta:
        model = Cadavre
        fields = ["title", "sentance_max"]

    def __init__(self, *args, **kwargs):
        super(NewCadavreForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = False


class NewSentanceForm(forms.ModelForm):

    sentance = forms.CharField(widget= forms.TextInput(attrs={'placeholder': 'Entrez votre phrase ici'}))

    class Meta:
        model = Sentance
        fields = ["sentance"]

    def __init__(self, *args, **kwargs):
        super(NewSentanceForm, self).__init__(*args, **kwargs)
        self.fields['sentance'].label = False

class EmailCadavreForm(forms.ModelForm):

    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}), error_messages={'required': 'Champs vide !'})
    
    class Meta:
        model = User
        fields = ["email"]

    def __init__(self, *args, **kwargs):
        super(EmailCadavreForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = False


class PassAccountForm(forms.ModelForm):

    password = forms.CharField(label="MOT DE PASSE", widget=forms.PasswordInput(attrs={'placeholder': 'Ancien'}), 
        error_messages={'required': 'Champs vide !'})

    password1 = forms.CharField(label= ("Mot de passe"), widget=forms.PasswordInput(attrs={'placeholder': 'Nouveau'}), 
        error_messages={'required': 'Champs vide !'})
    password2 = forms.CharField(label= ("Confirmation"), widget=forms.PasswordInput(attrs={'placeholder': 'Nouveau'}), 
        error_messages={'required': 'Champs vide !'})


    class Meta:
        model = User
        fields = ["password", "password1", "password2"]

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if not self.user.check_password(password):
            raise ValidationError('Mot de passe invalide')

        return password

    def clean_password2(self):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        return password2

    def __init__(self, *args, **kwargs):
        super(PassAccountForm, self).__init__(*args, **kwargs)

        self.fields['password'].label = False
        self.fields['password1'].label = False
        self.fields['password2'].label = False


class EmailAccountForm(forms.ModelForm):

    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}), error_messages={'required': 'Champs vide !'})


    class Meta:
        model = User
        fields = ["email"]

    def __init__(self, *args, **kwargs):
        super(EmailAccountForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = False

    def clean_email(self):

        data = self.cleaned_data['email']

        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email already used")

        return data


class UsernameAccountForm(forms.ModelForm):

    username = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'placeholder': 'Identifiant'}), 
        error_messages={'required': 'Champs vide !', 'unique': 'Ce pseudonyme appartient à un autre utilisateur'})

    class Meta:
        model = User
        fields = ["username"]

    def __init__(self, *args, **kwargs):
        super(UsernameAccountForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = False