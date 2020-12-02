import json

from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from .snippets.linux_user_mgnt import user_creation, UserCreationError
from .forms import AccountCreationForm, AccountAuthenticationFrom, AccountUpdateForm
from .models import AccountModel


# Create your views here.
@login_required
def home(request):
    obj = AccountModel.objects.all()
    context = {
        'users': obj
    }
    return render(request, 'home.html', context)


def registration_view(request):
    context = {
        'title': 'Registrate!',
        'register_active': 'active'
    }
    if request.POST:
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            raw_passwd = form.cleaned_data['password1']
            account = authenticate(username=username, password=raw_passwd)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = AccountCreationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    context = {
        'title': 'Login',
        'login_active': 'active'
    }

    form = AccountAuthenticationFrom(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = request.POST['username'].lower()
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid Credentials')

    context['login_form'] = form
    return render(request, 'account/login.html', context)


"""
 AJAX Views
"""


def save_user_form(request, form, template_name):
    data = {}

    if request.method == 'POST':
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                label = form.cleaned_data['label']
                user_creation(username, label)
            except UserCreationError:
                data['form_is_valid'] = False
            else:
                data['form_is_valid'] = True
                form.save()
        else:
            data['form_is_valid'] = False

    context = {'form': form}
    data['html_form'] = render_to_string(template_name=template_name, context=context, request=request)
    return JsonResponse(data)


def user_list(request):
    user_obj = []
    users = AccountModel.objects.all()
    if users.__len__() > 0:
        count = 1
        for user in users:
            obj = {
                'id': count,
                'username': user.username,
                'label': user.label,
                'pk': str(user.pk)
            }
            user_obj.append(obj)
            count += 1

        data = json.dumps({'data': user_obj})
        return HttpResponse(data, content_type='application/json')
    else:
        return JsonResponse({'show': False})


def user_create(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
    else:
        form = AccountCreationForm()
    return save_user_form(request, form, template_name='account/partial_user_create.html')


def user_update(request, pk):
    user = get_object_or_404(AccountModel, pk=pk)
    form = AccountUpdateForm(request.POST or None, instance=user)
    return save_user_form(request, form, template_name='account/partial_user_update.html')


def delete_view(request, pk):
    account = get_object_or_404(AccountModel, pk=pk)
    data = {}
    if request.method == 'POST':
        data['form_is_valid'] = True
        account.delete()
    else:
        context = {'account': account}
        data['html_form'] = render_to_string('account/partial_user_delete.html', context, request=request)
    return JsonResponse(data)
