# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, get_object_or_404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse
from django.core.mail import send_mail, EmailMessage

from django.http import HttpResponse
from django.http import HttpResponseRedirect

from cadavre.forms import UserLoginForm, UserProfileForm, UserForm, ResetPassForm, NewCadavreForm, EmailCadavreForm, \
PassAccountForm, UsernameAccountForm, EmailAccountForm, NewSentanceForm

from .models import UserProfile, Cadavre, Sentance
from django.db import models
from django.contrib.auth.models import User

import hashlib, datetime, random
from django.utils import timezone

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

def explorer(request):

    cadavres = Cadavre.objects.all()

    return render(request, "cadavre/explorer.html", locals())

def rules(request):
    return render(request, "cadavre/rules.html", locals())

def profil(request, username):
    u = get_object_or_404(User, username=username)
    se = Sentance.objects.filter(user_id=u.id)

    return render(request, "cadavre/profil.html", locals())

def home(request):
    
    user = request.user

    if user.is_active:
        return HttpResponseRedirect(reverse(home_cadavre))

    if request.method == "POST":

        form_log = UserLoginForm(request.POST)
        form_create = UserForm(request.POST)
        form_create_profile = UserProfileForm(request.POST, request.FILES)
   
        if form_log.is_valid():
               
            username = form_log.cleaned_data["username"]
            password = form_log.cleaned_data["password"]
            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:

                    login(request, user)

                return HttpResponseRedirect(reverse(home_cadavre))

       

        if form_create.is_valid() and form_create_profile.is_valid():

            username = form_create.cleaned_data['username']
            email = form_create.cleaned_data['email']
            avatar = form_create_profile.cleaned_data['avatar']

            random_string = str(random.random()).encode('utf8')
            salt = hashlib.sha1(random_string).hexdigest()[:5]
            salted = (salt + email).encode('utf8')

            activation_key = hashlib.sha1(salted).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            user = form_create.save()
            profile = form_create_profile.save(commit=False)
            profile.user = user
            profile.activation_key = activation_key
            profile.key_expires = key_expires
            profile.avatar = avatar
            profile.save()

            title = 'Bonjour'
            content = "Salut %s ! Pour activer ton compte, clic sur ce lien (avant 48h) \
            http://localhost:8000/cadavre/confirm/%s" % (username, activation_key)
                
            send_mail(title, content, 'eddine.zeroual@gmail.com', [email], fail_silently=False)

            return HttpResponseRedirect(reverse(home_cadavre))

        else:
            return HttpResponseRedirect(reverse(home))
    else:
        form_log = UserLoginForm()
        form_create = UserForm()
        form_create_profile = UserProfileForm()

    return render(request, 'cadavre/home.html', locals())

def home_cadavre(request):

    user = request.user
    id_user = user.id
    
    cadavre = Cadavre.objects.exclude(user_id=user.id).filter(completed=False)[0]
    sentance_id = cadavre.id
    sentance = Sentance.objects.filter(cadavre_id=sentance_id).latest('id')

    last_word = str(sentance.sentance).split(" ")

    sentance_len = cadavre.sentance_len
    sentance_max = cadavre.sentance_max

    error = False

    if request.method == "POST":

        form_cadavre = NewCadavreForm(request.POST)
        form_sentance = NewSentanceForm(request.POST)
        form_mail = EmailCadavreForm(request.POST)

        form_join_sentance = NewSentanceForm(request.POST)

# New Corpse

        if form_cadavre.is_valid() and form_sentance.is_valid():

            sentance_len = 0


            if request.user.is_anonymous() is not False:

                username = str(random.randint(0, 100000))
                user = User(username=username, first_name='Anonymous', 
                    last_name='CZXVXIOseQfc16NugH4GCZXVXIOseQfc16NugH4G')
                user.set_unusable_password()
                user.save()
                
                user.username = user.id
                user.save()
            
            else:
                user = request.user


            title = form_cadavre.cleaned_data["title"]
            sentance_max = form_cadavre.cleaned_data["sentance_max"]
            sentance = form_sentance.cleaned_data["sentance"]

            cadavre = form_cadavre.save(commit=False)
            cadavre_sentance = form_sentance.save(commit=False)
                    
            cadavre.user = user
            cadavre.title = title
            cadavre.sentance_max = sentance_max
            cadavre.save()

            cadavre_sentance.user = user
            cadavre_sentance.cadavre = cadavre
            cadavre_sentance.sentance = sentance

            cadavre_sentance.save()

            sentance_len += 1

            cadavre.sentance_len = sentance_len
            cadavre.save()

            if form_mail.is_valid():

                email = form_mail.cleaned_data["email"]

                title = 'Demande de cadavre reçue'
                content = "Votre demande de cadavre est à disposition des internautes, \
                vous recevrez une notification lorsque celui-ci sera achevé"
                
                send_mail(title, content, 'eddine.zeroual@gmail.com', [email], fail_silently=False)

            if user.last_name == "CZXVXIOseQfc16NugH4GCZXVXIOseQfc16NugH4G":

                user.is_active = False
                user.save()

            if user.last_name == "CZXVXIOseQfc16NugH4GCZXVXIOseQfc16NugH4G":
                return HttpResponseRedirect(reverse(confirm_cadavre))

            else:
                return HttpResponseRedirect(reverse(home))

        else:
            error = True

# Join Corpse

        if form_join_sentance.is_valid():

            if request.user.is_anonymous() is not False:

                username = str(random.randint(0, 100000))
                user = User(username=username, first_name='Anonymous', 
                        last_name='CZXVXIOseQfc16NugH4GCZXVXIOseQfc16NugH4G')
                user.set_unusable_password()
                user.save()
                    
                user.username = user.id
                user.save()

            else:
                user = request.user

            sentance = form_join_sentance.cleaned_data["sentance"]

            cadavre_sentance = form_join_sentance.save(commit=False)

            cadavre_sentance.user = user
            cadavre_sentance.cadavre = cadavre
            cadavre_sentance.sentance = sentance

            cadavre_sentance.save()

            sentance_len += 1

            cadavre.sentance_len = sentance_len

            if sentance_len == sentance_max:
                cadavre.completed = True

            cadavre.save()

            if user.last_name == "CZXVXIOseQfc16NugH4GCZXVXIOseQfc16NugH4G":
                return HttpResponseRedirect(reverse(confirm_sentance))
            else:
                return HttpResponseRedirect(reverse(home))

        else:
            return HttpResponseRedirect(reverse(home_cadavre))  

        if form_mail.is_valid():

            if cadavre.completed is not True:

                email = form_mail.cleaned_data["email"]

                title = 'Participation au cadavre reçue'
                content = "Votre phrase a été prise en compte, \
                vous recevrez un courriel lorsque le cadavre associé sera achevé"
                    
                send_mail(title, content, 'eddine.zeroual@gmail.com', [email], fail_silently=False)

            else:

                players_sentance = Sentance.objects.filter(cadavre_id=cadavre.id)
                players_id = user.id
                players = User.objects.filter(id=players_id)

                email = form_mail.cleaned_data["email"]

                title = 'Cadavre achevé'
                content_players = "Voici le cadavre achevé auquel vous avez participé : %s" % (cadavre, )
                content_creator = "Voici votre cadavre achevé : %s" % (cadavre, )

                send_mail(title, content_players, 'eddine.zeroual@gmail.com', [players.user.email], fail_silently=False)

                send_mail(title, content_creator, 'eddine.zeroual@gmail.com', [cadavre.user.email], fail_silently=False)

        else:
            return HttpResponseRedirect(reverse(home_cadavre))  

            
    else:
        form_cadavre = NewCadavreForm()
        form_sentance = NewSentanceForm()
        form_mail = EmailCadavreForm()

        form_join_sentance = NewSentanceForm()

    return render(request, 'cadavre/home_cadavre.html', locals())

def confirm_cadavre(request):

    return render(request, 'cadavre/confirm_cadavre.html', locals())

def confirm_sentance(request):

    return render(request, 'cadavre/confirm_sentance.html', locals())

# Account

@login_required
def account(request):

    user = request.user

    if request.method == 'POST':

        form_account_pass = PassAccountForm(request.POST)
        form_account_email = EmailAccountForm(request.POST)
        form_account_username = UsernameAccountForm(request.POST)

        form_account_pass.user = request.user

        if form_account_pass.is_valid():

            user.set_password(form_account_pass.cleaned_data["password2"])
            user.save()

            return HttpResponseRedirect(reverse(home))

        if form_account_email.is_valid():

            email = form_account_email.cleaned_data["email"]

            random_string = str(random.random()).encode('utf8')
            salt = hashlib.sha1(random_string).hexdigest()[:5]
            salted = (salt + email).encode('utf8')

            activation_key = hashlib.sha1(salted).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            user.email = email
            user.is_active = False
            user.activation_key = activation_key
            user.key_expires = key_expires

            user.save()

            title = 'Bonjour'
            content = "Salut! Pour activer ton compte, clic sur ce lien (avant 48h) \
            http://localhost:8000/cadavre/confirm/%s" % (activation_key)
                
            send_mail(title, content, 'eddine.zeroual@gmail.com', [email], fail_silently=False)

            return HttpResponseRedirect(reverse(home))

        if form_account_username.is_valid():

            username = form_account_username.cleaned_data["username"]

            user.username = username
            user.save()

            return HttpResponseRedirect(reverse(home))


    else:
        form_account_pass = PassAccountForm()
        form_account_email = EmailAccountForm()
        form_account_username = UsernameAccountForm()

    return render(request, 'cadavre/account.html', locals())

def logout_page(request):
	
    logout(request)
	
    return HttpResponseRedirect(reverse(home))

def register_confirm(request, activation_key):

    if request.user.is_anonymous() is not True:
        return HttpResponseRedirect(reverse(home))
    else:
        user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

        if user_profile.key_expires < timezone.now():
            return render_to_response('cadavre/confirm_expired.html')

        user = user_profile.user
        user.is_active = True
        user.save()

        return render_to_response('cadavre/confirm.html')   

def email_reset_pass(request):

    if request.method == 'POST':

        form_email_pass = EmailResetPassForm(data=request.POST)

        if form_email_pass.is_valid():

            email = form_email_pass.cleaned_data["email"]

            user_email = get_object_or_404(User, email=email)
            user_profile = get_object_or_404(UserProfile, user=user_email)

            random_string = str(random.random()).encode('utf8')
            salt = hashlib.sha1(random_string).hexdigest()[:5]
            salted = (salt + email).encode('utf8')
            activation_key = hashlib.sha1(salted).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            user_profile.activation_key = activation_key
            user_profile.key_expires = key_expires
            username = user_email.username

            user_profile.save()
                
            title = 'wesh'
            content = "Salut %s ! Pour activer ton compte, clic sur ce lien (avant 48h) \
            http://localhost:8000/cadavre/reset/%s" % (username, activation_key)
            
            send_mail(title, content, 'eddine.zeroual@gmail.com', [email], fail_silently=False)

            return HttpResponseRedirect(reverse(login_page))

    else:
        form_email_pass = EmailResetPassForm()

    return render(request, 'cadavre/email_reset_pass.html', locals())

def reset_pass(request, activation_key):
    
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
    user_id = user_profile.user_id
    user = get_object_or_404(User, id=user_id)
    
    if request.user.is_anonymous() is not True:
        return HttpResponseRedirect(reverse(home))

    else:

        if user_profile.key_expires < timezone.now():
            return render_to_response('cadavre/confirm_expired.html')

        else:

            if request.method == 'POST':

                form_reset_pass = ResetPassForm(data=request.POST)

                if form_reset_pass.is_valid():

                    user.set_password(form_reset_pass.cleaned_data["password1"])
                    user.save()

                    return HttpResponseRedirect(reverse(login_page))

            else:
                form_reset_pass = ResetPassForm()

        return render(request, 'cadavre/reset_pass.html', locals())





    







