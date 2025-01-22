from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm
from .models import User
from .models import Login
from django.http import HttpResponse
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


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')  # Replace 'home' with your home page view name
#         else:
#             messages.error(request, 'Invalid username or password')
#     return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        mail_id = request.POST.get('mail_id')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Basic validation
        if not all([username, mail_id, password, confirm_password]):
            messages.error(request, 'All fields are required')
            return redirect('register')

        # Check if username or email already exists
        if Login.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        if Login.objects.filter(mail_id=mail_id).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')

        # Password validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
            return redirect('register')

        try:
            # Create new user with hashed password
            hashed_password = make_password(password)
            Login.objects.create(
                username=username,
                mail_id=mail_id,
                password=hashed_password,
                confirm_password=hashed_password
            )
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')

        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return redirect('register')

    return render(request, 'registration.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Try to get user with the provided username
            user = Login.objects.get(username=username)
            # Check if password matches
            if check_password(password, user.password):
                # Set basic session data and redirect to show page
                request.session['user_id'] = user.id
                return redirect('show')
            else:
                messages.error(request, 'Invalid credentials')
                return redirect('login')
        except Login.DoesNotExist:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'login.html')


def logout_user(request):  # Added logout functionality
    request.session.flush()
    messages.success(request, 'Logged out successfully')
    return redirect('login')