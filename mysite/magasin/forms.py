from django import forms  # Add this import statement
from django.forms import ModelForm
from .models import Produit, Fournisseur
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class SignUpForm(UserCreationForm):
    class Meta:
        model = Fournisseur
        fields = ('name', 'email', 'password1', 'password2')
        widgets = {
            'name': forms.TextInput(attrs={'type': 'text'}),
        }
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'placeholder': 'Enter email'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder':'Enter password'}))

class ProduitForm(ModelForm): 
    class Meta : 
        model = Produit 
        fields = "__all__" #pour tous les champs de la table
        #fields=['libelle','description'] #pour qulques champs
        
class ProductForm(forms.Form):
    image = forms.ImageField()
    libelle = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    categorie = forms.CharField(max_length=255)
    product_id = forms.IntegerField(widget=forms.HiddenInput())