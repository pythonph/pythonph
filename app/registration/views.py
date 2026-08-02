from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from .forms import LoginForm, UserCreationForm


def register(request):
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("landing:landing")
    else:
        form = UserCreationForm()

    context = {"form": form}

    return render(request, "registration/register.html", context)


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    form_class = LoginForm
