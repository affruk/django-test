from django.shortcuts import render
from django.db import models
from .forms import userform , userprofileinfoform
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse , HttpResponseRedirect

# Create your views here.


def index(request):
    return render(request,'users/index.html')

def userlogin(request):
    if request.method== 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user= authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('users:index'))
            else:
                return HttpResponse("User is not active any more")
        else:
            print ("login not failed")
            print ("username {} and password {} dont match" .format(username,password))
            return HttpResponse("User Pass dont match")
    else:
        return render(request,'users/login.html')

@login_required
def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:index'))  #goto urls of app and look for index, only index will goto mainproject's urls

@login_required
def member_area(request):
    return HttpResponse("Welcome to the member area")

def register(request):
    registered= False

    if request.method == 'POST': #if any data is posted
        user_form = userform(data=request.POST)
        profile_form = userprofileinfoform(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save() #saves the data in db and returns model object , object var itself remains a form object 
            user.set_password(user.password)  # use the build in function to set the has password
            user.save()

            profile =profile_form.save(commit=False)  # after save we get model back from var instead of form
            profile.user= user
            print (type(profile))
            print (type(profile_form))

            if 'profile_pic' in request.FILES: # check if any file uploaded
                profile.profile_pic = request.FILES['profile_pic'] #update the pic in database

            profile.save() # save the data into model db
            registered=True
            return render (request,'users/register.html',{'registered':registered})

        else: #if forms not posted correctly
            print (user_form.errors , profile_form.errors)
            raise Exception( user_form.errors)
    else: # if no data is posted then show the form to user
        user_form = userform()
        profile_form = userprofileinfoform()
        return render (request ,'users/register.html',{'user_form':user_form, 'profile_form':profile_form})