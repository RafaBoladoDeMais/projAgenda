from django.shortcuts import render, get_object_or_404, redirect
from contact.models import Contact, Category
from django.db.models import Q
from django.core.paginator import Paginator 
from contact.forms import ContactForm
from django.urls import reverse
from contact.models import Contact
from django.contrib.auth.decorators import login_required


@login_required(login_url='contact:login')
def create(req): 
    form_action = reverse('contact:create')


    if req.method == 'POST':
        form = ContactForm(req.POST, req.FILES)
        context = {
            'site_title': 'Create Contact -',
            'form': form,
            'form_action': form_action,
            'action': 'Create contact'
        }

        if form.is_valid():
            contact:ContactForm = form.save(commit=False)
            contact.owner = req.user
            contact.save()

            return redirect('contact:update', id=contact.id)

        return render(
            req,
            'contacts/create.html',
            context= context
        )

    context = {
        'site_title': 'Create Contact -',
        'form': ContactForm(),
        'form_action': form_action,
        'action': 'Create contact'
    }

    return render(
        req,
        'contacts/create.html',
        context= context
    )

@login_required(login_url='contact:login')
def update(req, id): 
    contact = get_object_or_404(Contact, id=id, show=True, owner=req.user)
    form_action = reverse('contact:update', args=(id,) )


    if req.method == 'POST':
        form = ContactForm(req.POST, req.FILES, instance=contact)
        context = {
            'site_title': 'Create Contact -',
            'form': form,
            'form_action': form_action,
            'action': 'Update contact'
        }

        if form.is_valid():
            contact = form.save()
            return redirect('contact:update', id=contact.id)

        return render(
            req,
            'contacts/create.html',
            context= context
        )

    context = {
        'site_title': 'Create Contact -',
        'form': ContactForm(instance=contact),
        'form_action': form_action,
        'action': 'Update contact'
    }

    return render(
        req,
        'contacts/create.html',
        context= context
    )
@login_required(login_url='contact:login')
def delete(req, id): 
    contact = get_object_or_404(Contact, id=id, show=True, owner=req.user)
    confirmation = req.POST.get('confirmation', 'no')
    is_confirming = req.POST.get('is_confirming', 'no')

    if confirmation == 'yes':
        contact.delete()
        return redirect('contact:index')
    
    return render(
        req,
        'contacts/contact.html',
        {
            'contact': contact,
            'confirmation': confirmation,
            'is_confirming': is_confirming
        }
    )