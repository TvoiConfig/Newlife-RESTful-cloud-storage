from django.urls import path
from users.views import RegistrationView, AuthorizationView, LogoutView


urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('authorization/', AuthorizationView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]