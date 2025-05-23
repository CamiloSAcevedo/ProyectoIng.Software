# ---------------------- CLUSTERING ----------------------#
from django import forms    
from .models import ClusterTargeting

class EntrenamientoForm(forms.Form):
    archivo_excel = forms.FileField(
        label="Archivo Excel con vacantes",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    columnas = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox'}),
        label="Selecciona las columnas clave",
        required=False
    )

    nombre = forms.CharField(
        label="Ingresa un nombre para identificar tu modelo",
        max_length=100,
        widget=forms.TextInput(attrs={
            'size': 40,
            'class': 'form-control',
            'placeholder': 'Escribe un nombre descriptivo'
        })
    )

    def __init__(self, *args, **kwargs):
        columnas_disponibles = kwargs.pop('columnas_disponibles', [])
        super().__init__(*args, **kwargs)
        self.fields['columnas'].choices = [(col, col) for col in columnas_disponibles]

        for col in columnas_disponibles:
            self.fields[f"peso_{col}"] = forms.FloatField(
            initial=1.0,
            label=f"Peso para '{col}'",
            required=False,
            widget=forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'style': 'width: 80px; display: inline-block;'
            })
        )
        

META_INTEREST_CHOICES = [
    ("technology", "Technology"),
    ("software_development", "Software Development"),
    ("data_science", "Data Science & Analytics"),
    ("digital_marketing", "Digital Marketing"),
    ("finance", "Finance & Accounting"),
    ("healthcare", "Healthcare"),
    ("human_resources", "Human Resources"),
    ("education_training", "Education & Training"),
    ("customer_service", "Customer Service"),
    ("sales", "Sales"),
    ("logistics", "Logistics & Supply Chain"),
]

META_EDUCATION_CHOICES = [
    ("high_school", "High School"),
    ("college", "College"),
    ("associate_degree", "Associate Degree"),
    ("in_graduate_school", "In Graduate School"),
    ("doctorate_degree", "Doctorate Degree"),
]

META_LOCATION_CHOICES = [
    ("Medellin", "Medellin"),
    ("Bogotá", "Bogotá"),
    ("Itagui", "Itagui"),
    ("Sabaneta", "Sabaneta"),
    ("Cali", "Cali"),
]

class ClusterTargetingForm(forms.ModelForm):
    meta_location = forms.ChoiceField(choices=META_LOCATION_CHOICES, label="Ubicación (Ciudad)")
    interests = forms.MultipleChoiceField(
        choices=META_INTEREST_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Intereses"
    )
    education_level = forms.ChoiceField(
        choices=META_EDUCATION_CHOICES,
        label="Nivel Educativo"
    )
    age_min = forms.IntegerField(min_value=13, max_value=65, label="Edad mínima")
    age_max = forms.IntegerField(min_value=13, max_value=65, label="Edad máxima")

    class Meta:
        model = ClusterTargeting
        exclude = ['cluster']



