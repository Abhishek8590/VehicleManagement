from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import View, DetailView, UpdateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.forms import formset_factory
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, FormView, TemplateView, UpdateView, ListView, DetailView

from .models import Vehicle, VehicleImage
from .forms import RegisterForm, LoginForm, VehicleForm, VehicleImageForm, PassResetForm
from .decorators import signin_required, admin_required, superadmin_required
# Create your views here.

sadecks = [superadmin_required, signin_required, never_cache]
adecks = [admin_required, signin_required, never_cache]

decks = [signin_required, never_cache]

# registration view


class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, 'register.html', {"form": form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'registration successfully')
            return redirect('login')
        messages.error(request, 'registration faild')
        return render(request, 'register.html', {"form": form})

# login view


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'login.html', {"form": form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')
            usr = authenticate(request, username=uname, password=pwd)
            if usr:
                login(request, user=usr)
                messages.success(request, 'login successfully')
                return redirect('all-vehicles')
        messages.error(request, 'invalid credential')
        return render(request, 'login.html', {"form": form})


# logout view

class PassResetView(View):
    model=User
    template_name="pass-res.html"
    form_class=PassResetForm

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)

        if form.is_valid():
            username=form.cleaned_data.get("username")
            email=form.cleaned_data.get("email")
            pwd1=form.cleaned_data.get("password1")
            pwd2=form.cleaned_data.get("password2")

            if pwd1==pwd2:
                try:
                    usr=User.objects.get(username=username,email=email)
                    usr.set_password(pwd1)
                    usr.save()
                    messages.success(request,"password changed")
                    return redirect("signin")

                except Exception as e:
                    messages.error("invalid credentials")
                    return render (request,self.template_name,{"form":form})
            else:
                messages.error("password mismatch")
                return render(request,self.template_name,{"form":form})

@signin_required
def log_out_view(request, *args, **kwargs):
    logout(request)
    messages.success(request, 'logout successfully')
    return redirect('login')

# create vehicles


@method_decorator(sadecks, name='dispatch')
class VehicleCreateView(View):
    def get(self, request):
        form = VehicleForm()
        ImageFormSet = formset_factory(VehicleImageForm, extra=1)
        formset = ImageFormSet()
        return render(request, 'vehicle-create.html', {'form': form, 'formset': formset})

    def post(self, request):
        form = VehicleForm(request.POST)
        ImageFormSet = formset_factory(VehicleImageForm, extra=1)
        formset = ImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            vehicle = form.save(commit=False)
            vehicle.save()  # Save the vehicle

            # saving vehicle image
            for image_form in formset:
                if image_form.is_valid():
                    image = image_form.cleaned_data.get('image')
                    img = VehicleImage.objects.create(
                        vehicle=vehicle, image=image)
                    img.save()
            messages.success(request, 'vehicle created successfully')
            return redirect('all-vehicles')
        messages.error(request, 'invalid details')
        return render(request, 'vehicle-create.html', {'form': form, 'formset': formset})


# list all vehicles
@method_decorator(decks, name='dispatch')
class VehicleListView(View):
    def get(self, request, *args, **kwargs):
        vehicle = Vehicle.objects.all().order_by('-created_date')
        return render(request, 'vehicle-all.html', {"vehicles": vehicle})


# one vehicle detail
@method_decorator(decks, name='dispatch')
class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = 'vehicle-detail.html'
    context_object_name = 'vehicle'


@method_decorator(adecks, name='dispatch')
class VehicleUpdateView(UpdateView):
    form_class = VehicleForm
    model = Vehicle
    template_name = 'vehicle-update.html'
    success_url = reverse_lazy('all-vehicles')

@method_decorator(sadecks, name='dispatch')
class VehicleDeleteView(View):
    def get(self,request,*args, **kwargs):
        id=kwargs.get('pk')
        Vehicle.objects.get(id=id).delete()
        return redirect('all-vehicles')

