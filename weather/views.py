from django.shortcuts import render ,redirect
from django.contrib.auth.models import User , auth
from django.contrib import messages
from django.contrib.auth import authenticate
import json
import urllib.request

# Create your views here.
def index(request):
    if request.method == 'POST':
        city = request.POST['cityname']
        res = urllib.request.urlopen('https://api.openweathermap.org/data/2.5/weather?q=' + city +  '&appid=f4bea4304f582b1af3dc6343835f1ed9').read()
        load_data = json.loads(res)
        data = {
            "country_code":str(load_data['sys']['country']),
            "coordinate": str(load_data['coord']['lon']) + ' ' + str(load_data['coord']['lat']),
            "temp":str(load_data['main']['temp']) + ' K',
            "pressure": str(load_data['main']['pressure']),
            "humidity":str(load_data['main']['humidity'])

        }
    else:
        data = {}
        city =''
    return render(request , 'home.html' , {'data': data , 'city':city})





def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username , password = password)

        if user is not None:
            auth.login(request , user)
            return redirect('/')
        else:
            messages.info(request , 'Invalid username or password')
            return redirect('login')
    else:
        return render(request , 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeat_password = request.POST['repeat_password']

        if password == repeat_password:
            if User.objects.filter(username=username).exists():
                messages.info(request , 'Username already exsist')
                return redirect('register')
            else:
                user = User.objects.create_user(username = username , email = email , password = password)
                user.save()
                return redirect('login')
        else:
            messages.info(request , 'Password does not matched')
            return redirect('register')
    else:
        return render(request , 'register.html')
           
