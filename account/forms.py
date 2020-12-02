from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password

from .models import AccountModel

from string import punctuation


class AccountCreationForm(UserCreationForm):
    username = forms.CharField(max_length=15, )
    label = forms.CharField(max_length=30, )

    # def __init__(self, *args, **kwargs):
    #     super(AccountCreationForm, self).__init__(*args, **kwargs)
    #
    #     for field in ['username', 'label', 'password1', 'password2']:
    #         self.fields[field].help_text = None
    #         self.fields[field].label = ''
    #         self.fields[field].widget.attrs['class'] = 'form-control mb-4 text-center'
    #         self.fields[field].widget.attrs['placeholder'] = field.upper()

    class Meta:
        model = AccountModel
        fields = ['username', 'label', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        special_chars = punctuation
        if not (username.islower() or username.isspace()):
            raise forms.ValidationError('Username can not contain uppercase or whitespaces')
        elif any(char in special_chars for char in username):
            raise forms.ValidationError('Username can not contain special characters')
        return username


class AccountAuthenticationFrom(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control mb-4 text-center',
        'placeholder': 'user',
    }))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-4 text-center',
        'placeholder': 'password'
    }))

    # def clean_username(self):
    #     username = self.data['username'].lower()


class AccountUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=15,
                               widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = AccountModel
        fields = ['username', 'label', 'password']

        widgets = {
            'label': forms.TextInput(attrs={'class': 'form-control'})
        }

    def save(self, commit=True):
        user_instance = super(AccountUpdateForm, self).save(commit=False)

        if 'password' in self.changed_data:
            user_instance.password = make_password(self.data['password'])

        user_instance.save()
        return user_instance