from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.html import mark_safe


class Depot(models.Model):
    reference=models.CharField(max_length=100,primary_key=True)
    designation=models.CharField(max_length=100,blank=True)
    quantite_entree = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)

    quantite_sortie=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    location=models.CharField(max_length=100,null=True,blank=True)
    type=models.CharField(max_length=100,choices=(("Electique","Electique"),("Plomberie","Plomberie"),("Construction","Construction"),("Jeux","Jeux"),("Vetement","Vetement"),("Accessoir","Accessoir")),default="Electique")
    responsable=models.CharField(max_length=100,choices=(("Abas","Abas"),("Zakir","Zakir"),("Roger","Roger"),("Azmat","Azmat"),("Sheck Salman","Sheck Salman")),default="Abas")
    centre=models.CharField(max_length=100,choices=(("Antaniavo","Antaniavo"),("Andakana","Andakana"),("Manakara","Manakara")),default="Antaniavo")
    date_entree=models.DateField(null=True,blank=True)
    date_sortie=models.DateField(null=True,blank=True)
    image=models.ImageField(upload_to="image/",null=True,blank=True)
    def stock(self):
        try:
            stock=self.quantite_entree - self.quantite_sortie
            return stock    
        
        except:
            return 0
         
    def __str__(self):
        return self.reference
    def Image(self):
        if self.image and hasattr(self.image, 'url'):
            return mark_safe(f'<img src="{self.image.url}" width="50" height="50"/>')
        return "Pas d'Image "
    
class HistoriqueDepot(models.Model):
    reference=models.ForeignKey(Depot,on_delete=models.SET_NULL,null=True,)
    date=models.DateField(null=True)
    action=models.CharField(max_length=100,choices=(('entree','entree'),('sortie','sortie'),('retour','retour')))
    qantite= models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    motif=models.CharField(max_length=1000,null=True,blank=True)
    nom=models.CharField(max_length=100,null=True,blank=True)
    def responsable(self):
        return self.reference.responsable if self.reference else None
    def designation(self):
        return self.reference.designation if self.reference else None
    def location(self):
        return self.reference.location if self.reference else None
    def centre(self):
        return self.reference.centre if self.reference else None
    def stock(self):
        return self.reference.stock() if self.reference else 0

@receiver(post_save, sender=HistoriqueDepot)
def update_depot(sender,instance,created,**kwargs):
    if created:
        depot = Depot.objects.filter(reference=instance.reference).first()
        if depot:
            if instance.action == "entree":
                depot.quantite_entree += instance.qantite  # Increase stock
            elif instance.action == "sortie":
                depot.quantite_sortie += instance.qantite  # Reduce stock
            elif instance.action == "retour":
                depot.quantite_sortie -= instance.qantite  # Add back stock

            depot.save()  # Save the updated values
             

class DepotLivre(models.Model):
    reference=models.CharField(max_length=100,primary_key=True)
    designation=models.CharField(max_length=100,blank=True)
    category=models.CharField(max_length=100,choices=(("Quran","Quran"),("Fiqh","Fiqh"),("Anqaeed","Anqaeed"),("Douan","Douan"),("Sirat","Sirat"),("Akhlaq","Akhlaq")),default="Quran")
    language=models.CharField(max_length=100,choices=(("Mg","Mg"),("Ar","Ar"),("Fr","Fr"),("Ar-Mg","Ar-Mg"),("Mg-Fr","Mg-Fr"),("Ar-Fr","Ar-Fr")),default="Mg")
    quantite_entree=models.IntegerField(null=True,blank=True,default=0)
    quantite_sortie=models.IntegerField(null=True,blank=True,default=0)
    location=models.CharField(max_length=100,null=True,blank=True)
    centre=models.CharField(max_length=100,choices=(("Antaniavo","Antaniavo"),("Andakana","Andakana"),("Manakara","Manakara")),default="Antaniavo")
    date_entree=models.DateField(null=True,blank=True)
    date_sortie=models.DateField(null=True,blank=True)
    def stock(self):
        try:
            stock=self.quantite_entree - self.quantite_sortie
            return stock
        
        except:
            return 0
         
    def __str__(self):
        return self.reference

class HistoriqueDepotLivre(models.Model):
    reference=models.ForeignKey(DepotLivre,on_delete=models.CASCADE,null=True)
    date=models.DateField(null=True)
    action=models.CharField(max_length=100,choices=(('entree','entree'),('sortie','sortie')))
    qantite=models.IntegerField(default=0)
    motif=models.CharField(max_length=1000,null=True,blank=True)
    nom=models.CharField(max_length=100,null=True,blank=True)
    def language(self):
        try:
            return self.reference.language
        except:
            return "Pas de lang"

    def category(self):
        try:
            return self.reference.category
        except:
            return "No category"
    def designation(self):
        try:
            return self.reference.designation
        except:
            return "No designation"
    def location(self):
        try:
            return self.reference.location
        except:
            return "No location"
    def centre(self):
        try: 
            return self.reference.centre
        except:
            return "No centre"
        
    def stock(self):
        try:
            return self.reference.stock
        except:
            return "No stock"

@receiver(post_save, sender=HistoriqueDepotLivre)
def update_depotlivre(sender,instance,created,**kwargs):
    if created:
        if instance.action =="entree":
            quantite_entree=DepotLivre.objects.get(reference=instance.reference).quantite_entree
            DepotLivre.objects.filter(reference=instance.reference).update(
               quantite_entree=quantite_entree+instance.qantite
            )
        if instance.action =="sortie":
             quantite_sortie=DepotLivre.objects.get(reference=instance.reference).quantite_sortie
             DepotLivre.objects.filter(reference=instance.reference).update(
               quantite_sortie=quantite_sortie+instance.qantite
            )




class Avatar(models.Model):
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)  # Store the image in media/avatars/
    
    def __str__(self):
        return f"Avatar {self.id}"