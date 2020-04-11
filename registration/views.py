from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


class UserCreationForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username"]


def register(request):
    if request.method == 'POST':
        # print(request.POST)
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('landing')
    else:
        form = UserCreationForm()
    context = dict(form=form)

    return render(request, 'registration/register.html', context)
