from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages  
from django.contrib.auth.decorators import login_required
from .models import UserProfile 

# Registrasi
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registrasi berhasil! Anda sudah login.")
            return redirect("book_list")
        else:
            messages.error(request, "Registrasi gagal. Silakan cek kembali data Anda.")
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

# Logout
def logout_view(request):
    logout(request)  
    messages.info(request, "Anda telah logout.")  
    return redirect("login") 

# Profil
@login_required
def profile_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    context = {
        'user': user,
        'profile': profile
    }
    return render(request, 'accounts/profile.html', context)

# Edit Profil
@login_required
def edit_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
            profile.save()

        messages.success(request, 'Profil berhasil diperbarui')
        return redirect('edit_profile')

    context = {'user': user}
    return render(request, 'accounts/edit_profile.html', context)

# Ubah Password
@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # agar tidak logout setelah ganti password
            messages.success(request, "Password berhasil diubah.")
            return redirect("profile")
        else:
            messages.error(request, "Terjadi kesalahan. Silakan cek kembali form.")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "accounts/change_password.html", {"form": form})
