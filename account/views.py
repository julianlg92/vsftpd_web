import json

from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from .snippets.linux_user_mgnt import (user_modify_or_create, UserCreationError, UserEditionError,
                                       user_delete, UserDeleteError)
from .forms import AccountCreationForm, AccountAuthenticationFrom, AccountUpdateForm
from .models import AccountModel


# Create your views here.
@login_required
def home(request):
    return render(request, 'home.html')


def registration_view(request):
    context = {
        'title': 'Registrate!',
        'register_active': 'active'
    }
    if request.POST:
        form = AccountCreationForm(request.POST, group_edit=request.user.is_anonymous)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            context['registration_form'] = form
    else:
        form = AccountCreationForm(group_edit=request.user.is_anonymous)
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
                if user.is_moderator:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.warning(request, f'User {username} is not staff')
            else:
                messages.error(request, 'Invalid Credentials')

    context['login_form'] = form
    return render(request, 'account/login.html', context)


@login_required
def requests(request):
    return render(request, 'account/enable.html')


"""
 AJAX Views
"""


def user_list(request, **kwars):
    user_obj = []
    exclude_enable = kwars['exclude_enable']
    users = AccountModel.objects.all().exclude(is_enabled=exclude_enable) if request.user.is_superuser else AccountModel.objects.filter(
        group=request.user.group).exclude(pk=request.user.pk).exclude(is_enabled=exclude_enable)
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
        return JsonResponse({'data': None})


def save_user_form(request, form, template_name):
    data = {}

    modify = True if (form.instance.username != '') else False

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            label = form.cleaned_data['label']
            password = form.cleaned_data['password'] if modify else form.cleaned_data['password1']
            try:
                user_modify_or_create(username, password, label, modify)
            except (UserCreationError, UserEditionError):
                data['user_error'] = True
                data['form_is_valid'] = False
            else:
                data['form_is_valid'] = True
                user = form.save(commit=False)
                if request.user.is_moderator:
                    user.is_enabled = True
                user = form.save()

        else:
            data['form_is_valid'] = False

    context = {'form': form}
    data['html_form'] = render_to_string(
        template_name=template_name, context=context, request=request)
    return JsonResponse(data)


def user_create(request):
    form = AccountCreationForm(
        request.POST or None, group_edit=request.user.is_superuser)
    return save_user_form(request, form, template_name='account/partial_user_create.html')


def user_update(request, pk):
    user = get_object_or_404(AccountModel, pk=pk)
    form = AccountUpdateForm(request.POST or None, instance=user, group_edit=request.user.is_superuser)
    return save_user_form(request, form, template_name='account/partial_user_update.html')


@login_required
def user_enable(request, pk):
    data = {}

    if request.method == 'PUT':
        user = get_object_or_404(AccountModel, pk=pk)
        user.is_enabled = True
        user.save()
        data['username'] = user.username
        data['success'] = True

    return JsonResponse(data)


@login_required
def delete_view(request, pk):
    account = get_object_or_404(AccountModel, pk=pk)
    data = {}
    if request.method == 'POST':
        try:
            user_delete(account.username)
        except UserDeleteError:
            data['form_is_valid'] = False
            data['user_error'] = True
        else:
            data['form_is_valid'] = True
            account.delete()
    else:
        context = {'account': account}
        data['html_form'] = render_to_string(
            'account/partial_user_delete.html', context, request=request)
    return JsonResponse(data)
