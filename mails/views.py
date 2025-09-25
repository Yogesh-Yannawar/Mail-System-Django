from django.shortcuts import render,redirect
from .models import Mail
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from datetime import datetime
# Create your views here.

def signup_view(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request,'signup_temp.html',context={'form':form})
    form=RegisterForm()
    return render(request,'signup_temp.html',context={'form':form})

def login_view(request): 
    if request.method=='POST':
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect("dashboard")
        return render(request,'login_temp.html',context={'form':AuthenticationForm(),'errors':form.errors})
    form=AuthenticationForm()
    return render(request,'login_temp.html',context={'form':form})
            
@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    return render(request,'dashboard_temp.html')

def compose_view(request):
    if request.method=='POST':
        from_user = request.user.email
        to_user = request.POST.get('to_user')
        sub=request.POST.get('subject')
        content=request.POST.get('mail_content')
        date=datetime.now()
        file=request.FILES.get('attachment')
        Mail.objects.create(from_user=from_user,to_user=to_user,subject=sub,mail_content=content,datetime=date,attachment=file)
        return redirect('sent')
    return render(request,'compose.html')

def inbox_view(request):
    qs=Mail.objects.filter(to_user=request.user.username)
    return render(render,'inbox.html',context={'qs':qs})

def view_content(request,id):
    data=Mail.objects.get(id=id)
    return render(request,'content.html',context={'data':data})

def delete_view(request,id):
    data=Mail.objects.get(id=id)
    data.delete()
    return redirect('inbox')

def sent_view(request):
    qs=Mail.objects.filter(from_user=request.user.email)
    return render(request,'sent_mails.html',context={'qs':qs})

def sent_content(request,id):
    data=Mail.objects.get(id=id)
    return render(request,'sent_content.html',{'data':data})

def update_password(request):
    if request.method=='POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request,user)
            return render(request,'change_password.html',context={'msg':'Password Changed Successfully'})
        return render(request,'change_password.html',context={'errors':form.errors})
    form=PasswordChangeForm(user=request.user)
    return render(request,'change_password.html',context={'form':form})







