from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from project.lib import mail
from datetime import datetime
from .forms import TicketForm, UserCreateForm
from .models import Ticket
from project.apps.lotto.utils import tickets as tickets_util


def index(request):
    return render(request, 'lotto/index.html', {})


def register(request):
    # if already logged in just redirect to the main page
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('lotto:index'))
    
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save() # creates new records in the DB
            # authenticating user
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.add_message(request, messages.SUCCESS,
                'Successful regisration.')
            if user.email:
                # can be some error that we don't what to handle
                # (like email is not an email)
                try: 
                    mail.send(user.email, 'Registrierung bei Lottochecker.',
                        'Sie wurden bei Lottochecker registriert..')
                except:
                    pass
            return HttpResponseRedirect(reverse('lotto:index'))
    else:
        form = UserCreateForm()
            
    return render(request, 'form-page.html', {
        'form': form,
        'form_title': 'Register',
    })


def user_login(request):
    # if already logged in just redirect to the main page
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('lotto:index'))
    
    if request.method == 'POST':
        form = AuthenticationForm(None, request.POST)
        # if login and password are correct
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            login(request, user)
            
            if user.email:
                # can be some error that we don't what to handle
                # (like email is not an email)
                try: 
                    mail.send(user.email, 'Anmeldung bei Lottochecker.',
                        'Ein Login wurde bei Lottochecker mit Ihrem'
                                'Konto durchgefuehrt.')
                except:
                    pass
            
            messages.add_message(request, messages.SUCCESS, 'Angemeldet')
            return HttpResponseRedirect(reverse('lotto:ticket_list_upcoming'))
        else:
            pass
            #messages.add_message(request, messages.ERROR,
            #    'Authentication failure.')
    else:
        form = AuthenticationForm()
    
    
    return render(request, 'form-page.html', {
        'form': form,
        'form_title': 'Anmeldung',
    })


def user_logout(request):
    # if not logged in just redirect to the main page
    if request.user.is_authenticated():
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Abgemeldet')
    return HttpResponseRedirect(reverse('lotto:index'))


@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.instance
            ticket.user = request.user
            ticket.save()
            messages.add_message(request, messages.SUCCESS,
                'Neuer Schein erstellt')
            return HttpResponseRedirect(reverse('lotto:ticket_list'))
        else:
            pass
            #messages.add_message(request, messages.ERROR,
            #    'Authentication failure.')
    else:
        form = TicketForm()
        
    return render(request, 'form-page.html', {
        'form_title': 'Neuen Schein erstellen',
        'form': form,
        'form_text': 'Bitte geben Sie Ziehungsdatum und Tippzahlen ein:'
    })


@login_required
def ticket_edit(request, ticket_id):
    ticket = get_object_or_404(Ticket, user=request.user, id=ticket_id,
        date__gte=datetime.now().date())
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        #raise Exception(form.instance)
        if form.is_valid():
            ticket = form.instance
            ticket.user = request.user
            ticket.save()
            messages.add_message(request, messages.SUCCESS,
                'Changes saved.')
            return HttpResponseRedirect(reverse('lotto:ticket_list'))
    else:
        form = TicketForm(instance=ticket)
    
    return render(request, 'form-page.html', {
        'form_title': 'Ticket Edit ',
        'form': form,
        'submit_text': 'Save changes',
    })
    
@login_required
def ticket_delete(request, ticket_id):
    ticket = get_object_or_404(Ticket, user=request.user, id=ticket_id)
    ticket_id = ticket.id # will be set to None after delete
    ticket.delete()
    messages.add_message(request, messages.SUCCESS,
        'Ticket #%s (for date: %s) deleted.' % (ticket_id, ticket.date))
    # redirect to previous page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

@login_required
def ticket_list(request, upcoming=False):
    tickets = Ticket.objects.filter(user=request.user)
    if upcoming:
        tickets = tickets.filter(date__gte=datetime.now().date())
    
    return render(request, 'lotto/ticket/list-page.html', {
        'tickets': tickets,
        'upcoming': upcoming,
    })
    
@login_required    
def ticket_list_upcoming(request):
    return ticket_list(request, upcoming=True)


@login_required
def ticket_check(request):
    ''' Just calls ticket_check function, used for for debugging purposes. '''
    tickets_util.check_tickets()
    messages.add_message(request, messages.INFO, 'Tickets checked.')
    return ticket_list(request)


@login_required
def ticket_ajax_check(request):
    ''' Checking tickets with ajax '''
    win_tickets = tickets_util.check_tickets()
    user_wins = [t for t in win_tickets if t.user.id == request.user.id]
    
    upcoming = request.GET.get('upcoming', 'false') != 'false'
    
    tickets = Ticket.objects.filter(user=request.user)
    if upcoming:
        tickets = tickets.filter(date__gte=datetime.now().date())
        
    return render(request, 'lotto/ticket/list-snippet.html', {
        'tickets': tickets,
        'upcoming': upcoming,
        'ajax': True,
        'win_tickets': len(win_tickets),
        'user_wins': len(user_wins),
    });
    






