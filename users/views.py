
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from users.models import Profile
from django.db.models import Q
from .filters import ProfileFilter
from django.views.generic import ListView
from datetime import date
from django.utils.timezone import now



def register(request): #register function
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) #form uses POST protocol
        if form.is_valid():
            user=form.save() #save instance of form
            user.refresh_from_db()
            username = form.cleaned_data.get('username') #retrives users inputs
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.gender= form.cleaned_data.get('gender')
            user.profile.hobbies= form.cleaned_data.get('hobbies') #form is cleared after submission
            user.save()
            messages.success(request, f'Account created for {username}! You are now able to log in') #displays success message to the user when registration is complete
            return redirect('login')#redirects to 'login' page
    else:
        form = UserRegisterForm()
    return render (request, 'users/register.html', {'form': form}) #sends data to be displayed on 'registration'page

@login_required #user must be logged in to use function
def profile(request): #profile function
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

def matches(request): #matches function
    matches = Profile.objects.filter(Q(hobbies__contains="swimming") | Q(hobbies__contains="tennis") | Q(hobbies__contains="swimming") | Q(hobbies__contains="piano") | Q(hobbies__contains="karate") | Q(hobbies__contains="baking") | Q(hobbies__contains="painting") | Q(hobbies__contains="dancing") | Q(hobbies__contains="reading") | Q(hobbies__contains="watching movies")) 

#this function uses the 'Q' class objects to query the 'user_profile' table in order to genereate a list containing all of the users and their selected hobbies and stores it into the array 'matches'. The list will be filtered/sorted using the html file that the data is output to.

    args = {'matches': matches}
    
    return render(request, 'users/matches.html', args)



def age_range(min_age, max_age):
    current = now().date()
    min_date = date(current.year - min_age, current.month, current.day)
    max_date = date(current.year - max_age, current.month, current.day)
    
    return Profile.filter(birthdate__gte=max_date,
                                birthdate__lte=min_date).order_by("birthdate")

#the array 'matches' is now available from the 'matches.html' file in the templates directory.

class UserListView(ListView):
    model = Profile
    template = 'users/matches.html'
    queryset = Profile.objects.filter(gender__icontains='male')

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['filter'] = 'This is just some data'
        return context
