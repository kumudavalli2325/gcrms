from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
# def user(request):
#     if request.method == "POST":
#         try:
#             if request.POST['password'] != request.POST['confirm_password']:
#                 messages.error(request, 'Passwords do not match!')
#                 return render(request, 'index.html')
#
#             roles = request.POST.getlist('roles')
#
#             user = User(
#                 username=request.POST['username'],
#                 password=make_password(request.POST['password']),
#                 confirm_password=make_password(request.POST['confirm_password']),
#                 mail_id=request.POST['mail_id'],
#                 first_name=request.POST['first_name'],
#                 last_name=request.POST['last_name'],
#                 phone_number=request.POST['phone_number'],
#                 roles=','.join(roles)
#             )
#             user.save()
#             messages.success(request, 'User added successfully!')
#             return redirect('/show')
#         except Exception as e:
#             messages.error(request, f'Error: {str(e)}')
#     return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                messages.success(request, 'Login successful!')
                return redirect('/show')  # Redirect to the "show" page
            else:
                messages.error(request, 'Invalid username or password!')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist!')

    return render(request, 'login.html')


def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    messages.success(request, 'Logged out successfully!')
    return redirect('/login')

def logout_view(request):
    logout(request)  # This will log the user out
    return redirect('login')

def show(request):
    users = User.objects.all()
    return render(request, "show.html", {'users': users})


def edit(request, id):
    if 'user_id' not in request.session:
        messages.error(request, 'Please log in first!')
        return redirect('/login')

    user = User.objects.get(id=id)
    return render(request, 'edit.html', {'user': user})

#
# def update(request, id):
#     if 'user_id' not in request.session:
#         messages.error(request, 'Please log in first!')
#         return redirect('/login')
#
#     user = User.objects.get(id=id)
#     if request.method == 'POST':
#         try:
#             user.username = request.POST['username']
#             if request.POST.get('password'):
#                 user.password = make_password(request.POST['password'])
#                 user.confirm_password = make_password(request.POST['password'])
#             user.mail_id = request.POST['mail_id']
#             user.first_name = request.POST['first_name']
#             user.last_name = request.POST['last_name']
#             user.phone_number = request.POST['phone_number']
#             user.save()
#             messages.success(request, 'User updated successfully!')
#             return redirect("/show")
#         except Exception as e:
#             messages.error(request, f'Error: {str(e)}')
#     return render(request, 'edit.html', {'user': user})


def destroy(request, id):
    if 'user_id' not in request.session:
        messages.error(request, 'Please log in first!')
        return redirect('/login')

    user = User.objects.get(id=id)
    user.delete()
    messages.success(request, 'User deleted successfully!')
    return redirect("/show")


def user(request):
    if request.method == "POST":
        try:
            if request.POST['password'] != request.POST['confirm_password']:
                messages.error(request, 'Passwords do not match!')
                return render(request, 'index.html')

            roles = request.POST.getlist('roles')
            user = User(
                username=request.POST['username'],
                password=make_password(request.POST['password']),
                confirm_password=make_password(request.POST['confirm_password']),
                mail_id=request.POST['mail_id'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                phone_number=request.POST['phone_number'],
                roles=','.join(roles)
            )
            user.save()
            messages.success(request, 'User added successfully!')
            return redirect('/show')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return render(request, 'index.html')


def update(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        try:
            # Update all fields
            user.username = request.POST['username']
            user.mail_id = request.POST['mail_id']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.phone_number = request.POST['phone_number']

            # Update roles
            roles = request.POST.getlist('roles')
            user.roles = ','.join(roles)

            # Optional: Update password if provided
            if request.POST.get('password'):
                user.password = make_password(request.POST['password'])
                user.confirm_password = make_password(request.POST['password'])

            user.save()
            messages.success(request, 'User updated successfully!')
            return redirect("/show")
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return render(request, 'edit.html', {'user': user})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keeps the user logged in after changing the password
            return render(request, 'change_password.html', {'password_changed': True})
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form, 'password_changed': False})

