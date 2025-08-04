from django.shortcuts import render
from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import redirect, reverse

from account.forms import SigninForm, SignupForm

User = get_user_model()


def signin(request):
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()
            if user:
                login(request, user)
                return redirect(reverse('dashboard'))
            else:
                form.add_error('username', 'User does not exist')
        return render(request, 'account/signin.html', {'form': form})

    else:
        form = SigninForm()
        return render(request, 'account/signin.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()
            if user:
                form.add_error('username', 'User already exists')
            else:
                user = User(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    is_active=True,
                )
                user.set_password(form.cleaned_data['password'])
                user.save()
                return redirect(reverse('signup'))
        return render(request, 'account/signup.html', {'form': form})

    else:
        form = SignupForm()
        return render(request, 'account/signup.html', {'form': form})


# def logout_view(request):
#     logout(request)
#     return redirect(reverse('signin'))

def logout_confirm(request):
    if request.method == 'POST':
        logout(request)
        return redirect(reverse('signin'))
    return render(request, 'account/logout_confirm.html')
