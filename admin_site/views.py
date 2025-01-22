from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm
from .models import User
from django.contrib.auth import authenticate, login



# Existing views for managing users

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
    # Get all users
    users = User.objects.all()
    return render(request, "show.html", {'users': users})


def edit(request, id):
    user = User.objects.get(id=id)
    form = UserForm(instance=user)

    # Get the current roles assigned to the user
    selected_roles = user.roles.split(',') if user.roles else []

    return render(request, 'edit.html', {'user': user, 'form': form, 'selected_roles': selected_roles})


def update(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            # Save the form data
            updated_user = form.save(commit=False)
            roles = request.POST.getlist('roles')  # Get the selected roles from the checkboxes

            # Save roles as a comma-separated string
            updated_user.roles = ','.join(roles)
            updated_user.save()

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


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Replace 'home' with your home page view name
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')
