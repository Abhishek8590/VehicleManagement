from django.urls import path

from . import views

urlpatterns = [
   path('register/',views.RegistrationView.as_view(),name='register'),
   path('login/',views.LoginView.as_view(),name='login'),
   path('logout/',views.log_out_view,name='logout'),
   path("password/change/",views.PassResetView.as_view(),name="pass-res"),
   path('vehicle/create/',views.VehicleCreateView.as_view(),name='create-vehicle'),
   path('',views.VehicleListView.as_view(),name='all-vehicles'),
   path('vehicle/<int:pk>/',views.VehicleDetailView.as_view(),name='vehicle-detail'),
   path('vehicle/<int:pk>/update/',views.VehicleUpdateView.as_view(),name='update-vehicle'),
   path('vehicle/<int:pk>/delete/',views.VehicleDeleteView.as_view(),name='veh-delete'),
]
