from django.contrib import admin
from .models import Produit
from .models import Categorie
from .models import Fournisseur

admin.site.register(Produit)
admin.site.register(Categorie)
admin.site.register(Fournisseur)

# Register your models here.
