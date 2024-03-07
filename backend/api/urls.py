from django.urls import path, include
from . import views
urlpatterns = [
    path("/register", views.register, name="register"),
    path("/login",views.login,name="login"),
    path("/delete_account",views.delete_account, name="delete_account"),
    path("/setting",views.setting, name="setting"),
    path("/find_user",views.find_user, name="find_user"),
]