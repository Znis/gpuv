from django.urls import path

from . import views

urlpatterns = [
    path("", views.loginPage, name="login"),
    path("logout/", views.userlogout, name="logout"),
    path("checksession/", views.sessionCheck, name="session-check"),

    path("sessionend/", views.sessionEnd, name="sessionend"),
    path("login/", views.login_handler, name="loginhandler"),
    path("workspace/", views.index, name="index"),
    path('backend/', views.backend, name='backend'),

    
]
