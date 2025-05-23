from django.db import models


#------------- MODELOS PARA CLUSTERING ------------------#
class ModeloEntrenado(models.Model):
    nombre = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    columnas_usadas = models.JSONField()  # 👈 importante cambio
    pesos_columnas = models.TextField()   # JSON en string: {"col1": 1.0, "col2": 0.5}
    archivo_modelo = models.FileField(upload_to='media/modelos/')
    descripcion = models.TextField()
    
    def __str__(self):
        return f" {self.nombre} {self.fecha.strftime('%Y-%m-%d')}"


class ClusterTargeting(models.Model):
    cluster = models.IntegerField()
    modelo_clustering = models.ForeignKey(ModeloEntrenado, null=True, blank=True, on_delete=models.SET_NULL)
    meta_location = models.CharField(max_length=100,blank=True,null=True)
    interests = models.JSONField(default=list,blank=True,null=True)
    education_level = models.CharField(max_length=50,blank=True,null=True)
    age_min = models.IntegerField(blank=True,null=True)
    age_max = models.IntegerField(blank=True,null=True)

    def get_meta_targeting(self):
        return {
            "geo_locations": {"cities": [self.meta_location]},
            "interests": self.interests,
            "education_statuses": [self.education_level],
            "age_min": self.age_min,
            "age_max": self.age_max
        }
    
    def __str__(self):
        return f" Targeting cluster {self.cluster} - {self.modelo_clustering}"
