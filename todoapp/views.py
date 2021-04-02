from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from random import randrange
from finalproj.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from .models import TodoModel
from .forms import TodoForm
import requests

# Create your views here.

def usignup(request):
	if request.method == "POST":
		un = request.POST.get('un')
		em = request.POST.get('em')
		try:
			usr = User.objects.get(username=un)
			return render(request, 'usignup.html',{'msg':'Username Already Exists'})
		except User.DoesNotExist:
			try:
				usr = User.objects.get(email=em)
				return render(request, 'usignup.html',{'msg':'Email Already Registered'})
			except User.DoesNotExist:
				pw = ""
				text = "1234567890"

				for i in range(6):
					pw = pw + text[randrange(len(text))]
	

				subject = "Welcome to Pranav's Project"
				msg = "Your Password is: " + str(pw)
				send_mail(subject, msg, EMAIL_HOST_USER, [em])
				usr = User.objects.create_user(username=un, password=pw)
				usr.save()
				return redirect('ulogin')
	else:
		return render(request, 'usignup.html')


def ulogin(request):
	if request.method == "POST":
		un = request.POST.get('un')
		pw = request.POST.get('pw')
		usr = authenticate(username=un, password=pw)
		if usr is None:
			return render(request, 'ulogin.html',{'msg':'Invalid Username/Password'})
		else:
			login(request, usr)
			return redirect('home')
	else:
		return render(request, 'ulogin.html')

def ulogout(request):
	logout(request)
	return redirect('ulogin')



def home(request):
	if request.user.is_authenticated:
		user = request.user
		msg = TodoModel.objects.all().filter(user_id=request.user)
		try:
			res = requests.get("https://ipinfo.io")
			data = res.json()
			city_name = data['city']
		except Exception as e:
			print("Error",e)


		try:
			a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
			a2 = "&q=" + city_name        
			a3 = "&appid=c6e315d09197cec231495138183954bd"
			api_address =  a1 + a2  + a3
			res=requests.get(api_address)  
			data=res.json()
			loc_temp=data['main']['temp']
		except Exception as e:
			print("Temp issue ",e)
  


		return render(request, 'home.html',{'msg':msg,'city':city_name,'temp':loc_temp})
	else:
		return redirect('ulogin')

def create(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			f = TodoForm(request.POST)
			if f.is_valid():
				obj = f.save(commit=False)
				obj.user = User.objects.get(pk=request.user.id)
				obj.save()
				fm = TodoForm()
				return render(request, 'create.html',{'fm':fm,'msg':'Task Added'})
			else:
				return render(request, 'create.html',{'fm':f,'msg':'Check Errors'})
		else:
			fm = TodoForm()
			return render(request, 'create.html',{'fm':fm})

def delete(request, id):
	ds = TodoModel.objects.get(id=id)
	ds.delete()
	return redirect('home')
