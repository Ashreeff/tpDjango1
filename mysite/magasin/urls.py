from django.urls import path
from . import views
from .views import LoginView, signupView, logout, produit_view, panier
from django.contrib.auth import views as auth_views 


urlpatterns = [ 
    path('home/', views.index, name='index'),
    path('login/', views.LoginView, name='login'),
    path('signup/', views.signupView, name='signup'),
    path('logout/', views.logout, name='logout'), 
    path('produits/', views.produit_view, name='produit'), 
    path('panier/', views.panier, name='panier'),    
    path('fournisseur/', views.SupplierListView.as_view(), name='fournisseur'),



    #reset password ursls
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]