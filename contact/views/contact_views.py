from django.shortcuts import render, get_object_or_404, redirect
from contact.models import Contact
from django.db.models import Q
from django.core.paginator import Paginator 


# Create your views here.

def index(req):
    contacts = Contact.objects.all().filter(show=True).order_by('-id')

    paginator = Paginator(contacts, 10)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)  


    context = {
        'page_obj': page_obj,
        'site_title': 'home -',
    }
    return render(
        req,
        'contacts/index.html',
        context= context
    )

def search(req):
    search_value = req.GET.get('q', '').strip()

    if search_value == '':
        return redirect('contact:index')

    contacts = Contact.objects.all()\
                .filter(show=True)\
                .filter(
                        Q(first_name__icontains=search_value) |
                        Q(first_name__icontains=search_value) |
                        Q(phone__icontains=search_value) |
                        Q(email__icontains=search_value) 
                    
                    )\
                .order_by('-id')
    
    paginator = Paginator(contacts, 10)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number) 

    context = {
        'page_obj': page_obj,
        'site_title': 'home -',
    }
    return render(
        req,
        'contacts/index.html',
        context= context
    )

def contact(req, id):
    contact = get_object_or_404(Contact, id=id, show=True)

    context = {
        'contact': contact,
        'site_title': 'contact -',
    }
    return render(
        req,
        'contacts/contact.html',
        context= context
    )


