from django.urls import path
from . import views

app_name = "userauths"

urlpatterns = [
    path("signup/", views.register_view, name="signup"),
    path("signin/", views.login_view, name="signin"),
    path("signout/", views.logout_view, name="signout"),
]