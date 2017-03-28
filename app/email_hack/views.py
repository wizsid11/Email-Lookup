import json
from .forms import Form, Form1, LoginForm
from django.shortcuts import render, HttpResponseRedirect,HttpResponse
from .models import Emailfinder
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import csv
import hashlib
import json
import redis
import string
# import json
r = redis.Redis()
new=[]
flag=0
def user_login(request):
    if request.method == 'POST':

        form = LoginForm(request.POST)
        print 'yes'
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect('/emailhack/people-lookup')
                else:
                    return HttpResponse('Diasbled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request,'login.html',{'form':form})

class PubSub(object):

    def __init__(self, redis, channel="default"):
        self.redis = redis
        self.channel = channel

    def publish(self, data):
        self.redis.publish(self.channel, json.dumps(data))

    def subscribe(self, handler):
        redis = self.redis.pubsub()
        redis.subscribe(self.channel)

        for data_raw in redis.listen():
            if data_raw['type'] != "message":
                continue

            data = json.loads(data_raw["data"])
            handler(data)


def handler(data):
    print "Data received: %r" % data


q = PubSub(r, "channel")

def md5(text):
    m = hashlib.md5()
    m.update(str(text))
    hexdigest = m.hexdigest()
    return hexdigest


def new_instance_creator(instance):

    secret = md5(json.dumps(instance))
    new.append(secret)
    print secret
    objects=Emailfinder.objects.all().filter(secret=secret)
    if len(objects)<1:
        newdata = Emailfinder(name=string.capwords(instance[0].strip()), domain=instance[1].strip().lower(), secret=secret)
        newdata.save()
        print 'newdata'
        q.publish({'id': newdata.id, 'name': instance[
              0].strip().lower(), 'domain': instance[1].strip().lower(), 'secret': secret})


def handle_uploaded_file(filename):

    dictofdata = csv.DictReader(filename)

    rows = []
    for row in dictofdata:
        rows.append(row)
    secret = md5(json.dumps(rows))
    new.append(secret)
    objects=Emailfinder.objects.all().filter(secret=secret)
    if len(objects)<1:
        for row in rows:
            print row
            newdata = Emailfinder(
                name=string.capwords(row['name'].strip()), domain=row['domain'].strip().lower(), secret=secret)

            newdata.save()
            q.publish({'id': newdata.id, 'name': row['name'].strip().lower(), 'domain': row[
                      'domain'].strip().lower(), 'secret': secret})

def help1(request):
    return render(request,'help.html',{})

@login_required
def home(request):

    if request.method == 'POST':

        form1 = Form1(request.POST)

        print form1.is_valid()
        if form1.is_valid():


            name = request.POST['name']
            domain = request.POST['domain']

            print {'name': name, 'domain': domain, 'hello':'hello'}
            new_instance_creator((name, domain))


            return HttpResponseRedirect('/emailhack/people-lookup')
        form = Form(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])


            return HttpResponseRedirect('/emailhack/people-lookup')
    else:

        try:
            objects = Emailfinder.objects.all().filter(secret=new[-1])
        except:
            objects = Emailfinder.objects.all()

        form = Form()
        form1 = Form1()

    return render(request, 'index.html', {'form': form, 'form1': form1, 'objects': objects})

@login_required
def logoutuser(request):

    logout(request)
    return HttpResponseRedirect('/emailhack')    

@login_required
def alldata(request):
    if request.method == 'POST':

        form1 = Form1(request.POST)

        print form1.is_valid()
        if form1.is_valid():
            print 'checking form2'

            name = request.POST['name']
            domain = request.POST['domain']

            new_instance_creator((name, domain))


            return HttpResponseRedirect('/emailhack/people-lookup')
        form = Form(request.POST, request.FILES)
        if form.is_valid():

            print type(request.FILES['file'])

            handle_uploaded_file(request.FILES['file'])


            return HttpResponseRedirect('/emailhack/people-lookup')
    else:

        objects = Emailfinder.objects.all()
        form = Form()
        form1 = Form1()

    return render(request, 'index.html', {'form': form, 'form1': form1, 'objects': objects})


