from django.urls import path

from account import views

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_confirm, name='logout_confirm'),
]