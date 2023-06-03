from django.shortcuts import render
from django.template import loader
from .models import Produit
from django.shortcuts import redirect
from .forms import ProduitForm, LoginForm, SignUpForm, ProductForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as django_logout
from django.core.mail import send_mail

from django.contrib import messages

# Create your views here.


def logout(request):
    django_logout(request)
    return redirect('index')

def index(request):
    #add to panier
    if 'AjoutPanierBtn' in request.POST:
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            request.session['form_data'] = cleaned_data.form
        
    else:
        form = ProductForm()
        
    fournisseurs = Fournisseur.objects.all()
    produits = Produit.objects.all()
    context = {
        'fournisseurs' : fournisseurs,
        'produits' : produits
        }
    if 'contactbtn' in request.POST:
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        from_email = request.user.email # use the email of the authenticated user
        email_sent = False
        try:
            send_mail(
                subject,
                message,
                from_email,
                ['achrefhcini123@gmail.com'],
                fail_silently=False,
            ) 
            email_sent = True
           
        except:
            pass  
              
    return render(request,'magasin/accueil.html', context)

def panier(request):
    panier = request.session.get('panier', {})
    form = ProductForm(initial={
        'image': panier.get('image', ''),
        'libelle': panier.get('libelle', ''),
        'description': panier.get('description', ''),
        'categorie': panier.get('categorie', '')
    })
    context = {'form': form}
    return render(request, 'magasin/panier.html', context)

def produit_view(request):
    produits = Produit.objects.all()
    context = {}
    
    if request.method == "POST" : 
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            form = ProduitForm()  # create empty form
        context['form'] = form
    
    context['produits'] = produits
    return render(request, 'magasin/majProduits.html', context)

def LoginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # Set session value
                request.session['session_started'] = True
                request.session.set_expiry(1200) # 20 mins in seconds
                return redirect('index')  # Replace 'home' with the appropriate URL name for your home page
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
        
    return render(request, 'authentification/login.html', {'form': form})

from .models import *
def signupView (request):
    form = SignUpForm()  # Initialize an empty instance of SignUpForm
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            pwd1 = form.cleaned_data.get('password1')
            pwd2 = form.cleaned_data.get('password2')
            email = form.cleaned_data.get('email')
            name = form.cleaned_data.get('name')
            if pwd1 != pwd2:
                messages.error(request, 'Passwords do not match')
            else: 
                user = Fournisseur.objects.create_user(name=name ,email=email, password=pwd1)
                user.save()
                login(request, user)
                # Set session value
                request.session['session_started'] = True
                request.session.set_expiry(1200) # 20 mins in seconds
                # Additional logic if needed
                return redirect('index')
    return render(request, 'authentification/signup.html', {'form': form})

###### serializers views

from rest_framework import generics
from .serializers import FournisseurSerializer, ProduitSerializer, CategorieSerializer, ProduitNCSerializer, CommandeSerializer
from .models import Fournisseur, Produit, Categorie, ProduitNC, Commande
from rest_framework import viewsets

class FournisseurList(viewsets.ModelViewSet):
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer

class ProduitList(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

class CategorieList(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

class ProduitNCList(viewsets.ModelViewSet):
    queryset = ProduitNC.objects.all()
    serializer_class = ProduitNCSerializer

class CommandeList(viewsets.ModelViewSet):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'FournisseurList', FournisseurList)
router.register(r'ProduitList', ProduitList)
router.register(r'CategorieList', CategorieList)
router.register(r'ProduitNCList', ProduitNCList)
router.register(r'transaction', CategorieList)
router.register(r'CommandeList', CommandeList)

