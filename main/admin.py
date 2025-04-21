from django.contrib import admin
from main.models import  Depot,HistoriqueDepot,DepotLivre,HistoriqueDepotLivre
from django.utils.html import mark_safe

class DepotAdmin(admin.ModelAdmin):
    
    search_fields=["reference","designation","type"]
     
    list_filter=["reference","designation","quantite_entree","quantite_sortie","location","responsable","centre","date_entree","date_sortie","type"]
    def depot_statut(self,obj):
        try:
            stock= obj.quantite_entree-obj.quantite_sortie
            if stock==0:
                return mark_safe('<div style="width:100%%;height:100%%; background-color:red;text-align:center;color:white">%s</div>' % "Produit Vide")
            return mark_safe('<div style="width:100%%;height:100%%; background-color:green;text-align:center;color:white">%s</div>' % "Produit ne pas Vide")
        except:
            return mark_safe('<div style="width:100%%;height:100%%; background-color:green;text-align:center;color:white">%s</div>' % "Produit ne pas Vide")
        
    list_display=("reference","Image","designation","quantite_entree","quantite_sortie","stock","location","responsable","centre","date_entree","date_sortie","depot_statut")

class HistoriqueDepotAdmin(admin.ModelAdmin):
    list_display=["reference","date","action","qantite","motif","nom"]
    search_fields=["reference"]
    list_filter=["reference__reference","reference__designation","reference__responsable","reference__centre","date","action","nom"]



class DepotLivreAdmin(admin.ModelAdmin):
    
    search_fields=["reference","designation"]
     
    list_filter=["reference","designation","language","quantite_entree","quantite_sortie","location","category","centre","date_entree","date_sortie"]
    def depot_statut(self,obj):
        try:
            stock= obj.quantite_entree-obj.quantite_sortie
            if stock==0:
                return mark_safe('<div style="width:100%%;height:100%%; background-color:red;text-align:center;color:white">%s</div>' % "Livre Vide")
            return mark_safe('<div style="width:100%%;height:100%%; background-color:green;text-align:center;color:white">%s</div>' % "Livre ne pas Vide")
        except:
            return mark_safe('<div style="width:100%%;height:100%%; background-color:green;text-align:center;color:white">%s</div>' % "Livre ne pas Vide")
        
    list_display=("reference","designation","quantite_entree","quantite_sortie","stock","location","language","category","centre","date_entree","date_sortie","depot_statut")


class HistoriqueDepotLivreAdmin(admin.ModelAdmin):
    list_display=["reference","date","language","category","designation","action","qantite","motif","nom"]
    search_fields=("reference__reference","reference__designation")
    list_filter=["reference__reference","reference__designation","reference__centre","date","action","nom"]



admin.site.register(Depot,DepotAdmin)
admin.site.register(DepotLivre,DepotLivreAdmin)
admin.site.register(HistoriqueDepot,HistoriqueDepotAdmin)
admin.site.register(HistoriqueDepotLivre,HistoriqueDepotLivreAdmin)
# Register your models here.
