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

# q.subscribe(handler)

# q = PubSub(r, "channel")
# q.publish("test data")
# q = Pubq Sub(r, "channel")

# q.subscribe(handler)


# Create your views here.
def md5(text):
    m = hashlib.md5()
    m.update(str(text))
    hexdigest = m.hexdigest()
    return hexdigest


def new_instance_creator(instance):
    # objects=Emailfinder.objects.all().filter()
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
    # print type(filename)
    # file_contents = filename.read()

    # secret=md5(file_contents)
    # filename.close()
    dictofdata = csv.DictReader(filename)
    # new=dictofdata
    # print dict(dictofdata)
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
    # print rows
    # secret = md5(json.dumps(rows))
    # print secret

    # text=json.loads(filename.read())
    # domain=text['domain']
    # for name in text['name']:

    # newdata = Emailfinder(name=name, domain=domain)
    # newdata.save()
def help1(request):
    return render(request,'help.html',{})
@login_required
def home(request):
    # new=[]
    # n=[]

    if request.method == 'POST':

        form1 = Form1(request.POST)
        # print form1
        print form1.is_valid()
        if form1.is_valid():
            print 'checking form2'

            # objects = Emailfinder.objects.all()
            name = request.POST['name']
            domain = request.POST['domain']
            # print name
            # print domain
            print {'name': name, 'domain': domain, 'hello':'hello'}
            new_instance_creator((name, domain))
            # objects = Emailfinder.objects.all()

            return HttpResponseRedirect('/emailhack/people-lookup')
        form = Form(request.POST, request.FILES)
        if form.is_valid():
            # instance=form.save(commit=False)
            # instance.save()
            # objects = Emailfinder.objects.all()
            # new.append(request.FILES['file'])
            print type(request.FILES['file'])
            # new.append(request.FILES['file'])
            handle_uploaded_file(request.FILES['file'])
            # objects = Emailfinder.objects.all()

            return HttpResponseRedirect('/emailhack/people-lookup')
    else:
        # dictofdata = csv.DictReader(new[0])
    # print dict(dictofdata)
        # rows = []
        # for row in new:
            # rows.append(row)
        # secret = md5(json.dumps(rows))
        try:
            objects = Emailfinder.objects.all().filter(secret=new[-1])
        except:
            objects = Emailfinder.objects.all()
        # objects = Emailfinder.objects.all()
        form = Form()
        form1 = Form1()
        # del new[:]
    # return render(request,
# 'account/index.html',
# {'objects': objects})
    return render(request, 'index.html', {'form': form, 'form1': form1, 'objects': objects})

    # context = {"objects": objects}
    # return render(request, 'index.html', context)
@login_required
def logoutuser(request):
    # for user in User.objects.filter(is_active=True):
        # user.is_active=False
    logout(request)
    return HttpResponseRedirect('/emailhack')    

@login_required
def alldata(request):
    if request.method == 'POST':

        form1 = Form1(request.POST)
        # print form1
        print form1.is_valid()
        if form1.is_valid():
            print 'checking form2'

            # objects = Emailfinder.objects.all()
            name = request.POST['name']
            domain = request.POST['domain']
            # print name
            # print domain
            # print {name: name, domain: domain, 'hello':'hello'}
            new_instance_creator((name, domain))
            # objects = Emailfinder.objects.all()

            return HttpResponseRedirect('/emailhack/people-lookup')
        form = Form(request.POST, request.FILES)
        if form.is_valid():
            # instance=form.save(commit=False)
            # instance.save()
            # objects = Emailfinder.objects.all()
            # new.append(request.FILES['file'])
            print type(request.FILES['file'])
            # new.append(request.FILES['file'])
            handle_uploaded_file(request.FILES['file'])
            # objects = Emailfinder.objects.all()

            return HttpResponseRedirect('/emailhack/people-lookup')
    else:
        # dictofdata = csv.DictReader(new[0])
    # print dict(dictofdata)
        # rows = []
        # for row in new:
            # rows.append(row)
        # secret = md5(json.dumps(rows))
        # try:
            # objects = Emailfinder.objects.all().filter(secret=new[-1])
        # except:
            # objects = Emailfinder.objects.all()
        objects = Emailfinder.objects.all()
        form = Form()
        form1 = Form1()
        # del new[:]
    return render(request, 'index.html', {'form': form, 'form1': form1, 'objects': objects})

    # objects = Emailfinder.objects.all()
    # context = {"objects": objects}
    # return render(request, 'index.html', context)
