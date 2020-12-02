from django.shortcuts import render, redirect, get_object_or_404
from django.http import StreamingHttpResponse
from django.shortcuts import render
import json
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.contrib.admin import AdminSite
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
import json
from django.http import HttpResponse
import csv
from datetime import datetime, timedelta
from django.db.models import Sum
from .models import *
from .forms import *

# Create your views here.
def index(request):
    return render(request, 'index.html')
# Create your views here.

def add_results(request):

    if request.method == "POST":
        ttn_code = TTN.objects.filter(ttn_no=request.POST['ttn_code'])
        if ttn_code:
            post = {}
            for keys in request.POST:
                post[keys] = request.POST[keys]
            post['ttn_code'] = ttn_code[0].id
            form = TestResultsForm(post)
            if form.is_valid():
                instance = form.save(commit=True)
                return render(request, 'add_results.html', {'message':'message'})
            else:
                return render(request, 'add_results.html', {'errors':form.errors})

        else:
            return render(request, 'add_results.html', {'errors':'ttn code does not exist'})
    return render(request, 'add_results.html')

def validate_email(request):
    email = request.GET.get("email", None)

    data = {

        'exists' : TestResults.objects.filter(email__iexact=email).exists()
    }

    return JsonResponse(data)

def admin_home(request):
    if 'admin_logged' in request.session:
        return render(request, 'adminPanel/index.html')
    else:
        return redirect('admin_login')

def delete_ttn_no(request, id):
    if 'admin_logged' in request.session:
        instance = TTN.objects.get(id=id)
        instance.delete()
        return redirect('ttn')
    else:
        return redirect('admin_login')

def delete_test_result(request, id):
    if 'admin_logged' in request.session:
        instance = TestResults.objects.get(id=id)
        instance.delete()
        return redirect('test_results')
    else:
        return redirect('admin_login')

def ttn(request):
    if 'admin_logged' in request.session:
        ttn_nos = TTN.objects.all().order_by('-id')

        if request.method == "POST":
            form = ttnForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=True)
                return redirect('ttn')
            else:
                return render(request, 'adminPanel/ttn.html', {'ttn_nos':ttn_nos, 'errors':form.errors})

        return render(request, 'adminPanel/ttn.html', {'ttn_nos':ttn_nos})
    else:
        return redirect('admin_login')

def test_results(request):
    if 'admin_logged' in request.session:
        test_resultss = TestResults.objects.all().order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(test_resultss, 1)
        try:
            test_resultss = paginator.page(page)
        except PageNotAnInteger:
            test_resultss = paginator.page(1)
        except EmptyPage:
            test_resultss = paginator.page(paginator.num_pages)

        return render(request, 'adminPanel/test_results.html', {'test_results':test_resultss})
    else:
        return redirect('admin_login')

def get_results(request):


    results = []
    results.append(TestResults.objects.filter(test_result="positive").count())
    results.append(TestResults.objects.filter(test_result="negative").count())
    results.append(TestResults.objects.filter(test_result="inconclusive").count())

    data = {

        'results' : results
    }

    return JsonResponse(data)

def get_positive_by_age(request):


    results = []
    results.append(TestResults.objects.filter(test_result="positive", age__gte=0, age__lte=20).count())
    results.append(TestResults.objects.filter(test_result="positive", age__gt=20, age__lte=40).count())
    results.append(TestResults.objects.filter(test_result="positive", age__gt=40, age__lte=60).count())
    results.append(TestResults.objects.filter(test_result="positive", age__gt=60).count())

    data = {

        'results' : results
    }

    return JsonResponse(data)

def get_infection_by_age(request):


    results = []
    total = float(TestResults.objects.all().count()+0.001)
    results.append(TestResults.objects.filter(test_result="positive", age__gte=0, age__lte=20).count()/total*100)
    results.append(TestResults.objects.filter(test_result="positive", age__gt=20, age__lte=40).count()/total*100)
    results.append(TestResults.objects.filter(test_result="positive", age__gt=40, age__lte=60).count()/total*100)
    results.append(TestResults.objects.filter(test_result="positive", age__gt=60).count()/total*100)

    data = {

        'results' : results
    }

    return JsonResponse(data)

def get_infection_by_postcode(request):
    postcode = request.GET.get("postcode")
    total = float(TestResults.objects.all().count()+0.001)
    results = []
    results.append(TestResults.objects.filter(test_result="positive", postcode=postcode).count()/total*100)

    data = {

        'results' : results,

    }

    return JsonResponse(data)


def get_positive_by_postcode(request):
    postcode = request.GET.get("postcode")
    results = []
    results.append(TestResults.objects.filter(test_result="positive", postcode=postcode).count())

    data = {

        'results' : results,

    }

    return JsonResponse(data)

def admin_login(request):
    request.session.flush()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        adm = admin.objects.filter(username__iexact = username).exists()

        if adm:
            adm = admin.objects.filter(username__iexact = username)[0]
            if check_password(password,adm.password):
                request.session['admin_logged'] = adm.id
                request.session['admin_name'] = adm.username
                return redirect('admin_home')

        context = {

            'no_match' : True
        }
        return render(request, 'adminPanel/admin_login.html', context)

    return render(request, 'adminPanel/admin_login.html')

def logout(request):
    request.session.flush()
    return redirect('admin_home')