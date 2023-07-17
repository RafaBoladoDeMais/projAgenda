from django.shortcuts import render, redirect
from contact.forms import RegisterForm, RegisterUpdateForm
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def register(req):
    form = RegisterForm()

    if req.method == 'POST':
        form = RegisterForm(req.POST)

        if form.is_valid():
            form.save()
            messages.success(req, 'Contato adicionado com sucesso')
            return redirect('contact:index')


    context = {
        'action': 'Create User',
        'form': form
    }
    return render(
        req, 
        'contacts/register.html',
        context
    )


def login_view(req):
    form = AuthenticationForm(req)

    if req.method == 'POST':
        form = AuthenticationForm(req, data=req.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(req, user)
            messages.success(req, 'Logado com sucesso')
            return redirect('contact:index')
        else:
            messages.error(req, 'login invalido')


    context = {
        'action': 'Login',
        'form': form
    }
    return render(
        req, 
        'contacts/login.html',
        context
    )

@login_required(login_url='contact:login')
def logout_view(req):
    auth.logout(req)

    return redirect('contact:login')


@login_required(login_url='contact:login')
def user_update(req):
    form = RegisterUpdateForm(instance=req.user)

    if req.method == 'POST':
        form = RegisterUpdateForm(data=req.POST, instance=req.user)

        context = {
            'action': 'Update User',
            'form': form
        }
        if form.is_valid():
            form.save()
            messages.success(req, 'Usuario atualizado com sucesso')
            return redirect('contact:index')


    context = {
        'action': 'Update User',
        'form': form
    }
    return render(
        req, 
        'contacts/register.html',
        context
    )