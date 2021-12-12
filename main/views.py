from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from .models import Todo

# Create your views here.
def home(request):
    context = {'title': 'Todo App'}
    return render(request, 'index.html', context)

def signupuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass1']
        if pass1 == pass2:
            try:
                user = User.objects.create_user(username=username, email=email, password=pass1)
                user.save()
                login(request, user)
                return redirect('dashboard')
            except IntegrityError:
                context = {'title': 'Sign Up',
                            'error' : 'User already exists'}
                return render(request, 'signup.html', context)
    else:
        context = {'title': 'Sign Up'}
        return render(request, 'signup.html', context)

def signinuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Username or password is incorrect')
    return render(request, 'signin.html')

def signoutuser(request):
    logout(request)
    return redirect('signinuser')


def dashboard(request):
    todos = Todo.objects.filter(owner=request.user)
    context = {'title':'Dashboard', 'todos':todos}
    return render(request, 'dashboard.html', context)

def addtask(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        todo = Todo.objects.create(title=title, description=description, owner=request.user)
        todo.save()
        return redirect('dashboard')
    else:
        context = {'title':'Dashboard | Todo App'}
        return render(request, 'add.html', context)

