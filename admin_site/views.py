# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm
from .models import User

def user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                # Create user object but don't save yet
                user = form.save(commit=False)
                # Remove confirm_password as it's not in the model
                user.save()
                messages.success(request, 'User registered successfully!')
                return redirect('/show')
            except Exception as e:
                messages.error(request, f'Error registering user: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserForm()
    return render(request, 'index.html', {'form': form})

def show(request):
    users = User.objects.all()
    return render(request, "show.html", {'users': users})

def edit(request, id):
    user = User.objects.get(id=id)
    form = UserForm(instance=user)
    return render(request, 'edit.html', {'user': user, 'form': form})

def update(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully!')
            return redirect("/show")
        messages.error(request, 'Please correct the errors below.')
    form = UserForm(instance=user)
    return render(request, 'edit.html', {'user': user, 'form': form})

def destroy(request, id):
    user = User.objects.get(id=id)
    user.delete()
    messages.success(request, 'User deleted successfully!')
    return redirect("/show")