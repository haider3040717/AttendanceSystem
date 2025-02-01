from django.shortcuts import render, redirect
from .models import CustomUser
from images.models import Image
from .forms import AccountCreationForm, AccountAuthenticationForm, EditProfileForm
from images.forms import ProfileImageForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            user.is_active = True
            user.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Account Created Successfully !')
                return redirect('home')
            else:
                print('invalid credentials')
                # messages.error(request, 'Invalid Username or Passowrd !')
        else:
            print(form.errors)
            messages.error(request, 'Invalid form details ! Try again')
            return redirect('user_register')
    else:
        form = AccountCreationForm()
        return render(request, 'frontend/register.html', {'form': form})



def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully Logged-in !')
                return redirect('home')
            else:
                print('Invalid credentials !')
                messages.error(request, 'Invalid Username or Passowrd !')
                return redirect('user_login')
        else:
            print(form.errors)
            messages.error(request, 'Invalid Username or Password !')
            return redirect(request.path)
    else:
        form = AccountAuthenticationForm()
        return render(request, 'frontend/login.html', {'form': form})



@login_required(login_url='user_login')
def user_logout(request):
    # Perform the logout
    logout(request)
    return redirect('user_login')



@login_required(login_url='user_login')
def edit_profile(request):
    user = request.user  # Get the logged-in user

    # Get or create the user's profile image object
    profile_image, created = Image.objects.get_or_create(user=user)

    # Initialize forms with user instance
    if request.method == "POST":
        profile_form = EditProfileForm(request.POST, instance=user)
        image_form = ProfileImageForm(request.POST, request.FILES, instance=profile_image)

        if profile_form.is_valid() and image_form.is_valid():
            profile_form.save()  # Save user details
            image_form.save()  # Save profile image
            return redirect('home')  # Redirect to profile page (update URL as needed)
    else:
        profile_form = EditProfileForm(instance=user)
        image_form = ProfileImageForm(instance=profile_image)

    context = {
        'profile_form': profile_form,
        'image_form': image_form,
        'user': user,
    }
    return render(request, 'frontend/edit_profile.html', context)