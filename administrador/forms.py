from django import forms
from .models import Campaign, AdSet, Ad, Creative, Vacante

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['nombre', 'red_social', 'objective']
    
    def __init__(self, *args, **kwargs):
        red_social = kwargs.pop('red_social', None)  # Extraer red_social
        super().__init__(*args, **kwargs)

        self.fields['objective'].widget = forms.HiddenInput()

        # Mostrar los campos dependiendo de la red social seleccionada
        if red_social in ['facebook', 'instagram']: 
            self.fields['objective'].widget = forms.Select(choices=Campaign.OBJECTIVES)
        # elif red_social == 'X':   (Por definir)

class AdSetForm(forms.ModelForm):
    class Meta:
        model = AdSet
        fields = ['nombre', 'campaign_id', 'daily_budget', 'billing_event', 'optimization_goal', 'status']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['nombre', 'adset_id', 'status', 'creative_id', 'red_social']
    
    def __init__(self, *args, **kwargs):
        red_social = kwargs.pop('red_social', None)  # Extraer red_social
        super().__init__(*args, **kwargs)

        if red_social:
            self.fields['red_social'].initial = red_social


class CreativeForm(forms.ModelForm):
    class Meta:
        model = Creative
        fields = ['nombre', 'name', 'message', 'body', 'image_url', 'link', 'call_to_action']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# ---------------------- MIS VACANTES ----------------------#
class VacanteForm(forms.ModelForm):
    class Meta:
        model = Vacante
        fields = ['vacante', 'empresa', 'ubicacion', 'contrato', 'salario', 'descripcion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
#Cargar excel

class UploadFileForm(forms.Form):
    archivo = forms.FileField(label='Seleccionar archivo Excel')
# ---------------------- MIS VACANTES ----------------------#