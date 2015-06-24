from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('landing')
    else:
        form = UserCreationForm()
    context = dict(form=form)
    return render(request, 'registration/register.html', context)
