from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(name=name, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, name, email, password):
        user = self.create_user(name, email, password=password)
        user.is_superuser  = True
        user.save(using=self._db)
        return user


class Fournisseur(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50, unique=True)
    adress = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=8)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True) 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = UserManager()  # Add this line

    def __str__(self):
        return self.name + " " + self.address + " " + self.email + " " + self.telephone

   
# Create your models here.
class Produit(models.Model):
    product_id = models.AutoField(primary_key=True)
    type_choices=[("em","emballé"),("fr","Frais"),("cs","Conserve")]
    libelle=models.CharField(max_length=50)
    description=models.TextField(default="Non définie")
    prix=models.DecimalField(max_digits=10, decimal_places=3)
    type=models.CharField(max_length=2,choices=type_choices,default="em")
    img=models.ImageField(blank=True, upload_to='produits')
    catégorie=models.ForeignKey('Categorie',on_delete=models.CASCADE,null=True)
    def __str__(self):
        return "Libellé : "+self.libelle +"\nDescription : "+self.description+"\nPrix : "+str(self.prix)
    
class Categorie(models.Model):
   TYPES_CHOICES=[('Al','Alimentaire'), ('Mb','Meuble'),('Sn','Sanitaire'), ('Vs','Vaisselle'),('Vt','Vêtement'),('Jx','Jouets'),('Lg','Linge de Maison'),('Bj','Bijoux'),('Dc','Décor')]
   name=models.CharField(default='alimentaire', choices=TYPES_CHOICES,max_length=50,)
   def __str__(self) :
       return self.name+""
   
class ProduitNC(Produit):
 duree_garantie = models.CharField(max_length=100)
 def __str__(self):
        return super().__str__() + f" ({self.duree_garantie})" 
    
class Commande(models.Model):
    dateCde = models.DateField(null=True, default=date.today)
    totalCde = models.DecimalField(max_digits=10, decimal_places=3)
    produits = models.ManyToManyField('Produit', related_name='commandes')

    def __str__(self):
        return f"Commande du {self.dateCde} d'un total de {self.totalCde}"