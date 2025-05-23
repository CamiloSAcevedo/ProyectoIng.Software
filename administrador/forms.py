from django import forms
from .models import Campaign, AdSet, Ad, Creative, Vacante
from .models import AdvertiserTikTok, CampaignTikTok, AdGroupTikTok, AdTikTok

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['nombre', 'objective']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class AdSetForm(forms.ModelForm):
    class Meta:
        model = AdSet
        fields = ['nombre', 'campaign_id', 'daily_budget', 'billing_event', 'optimization_goal', 'status']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['nombre', 'adset_id', 'status', 'creative_id']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CreativeForm(forms.ModelForm):
    class Meta:
        model = Creative
        fields = ['nombre', 'name', 'message', 'body', 'image_url', 'link', 'call_to_action']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            
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



class AdvertiserTikTokForm(forms.ModelForm):
    class Meta:
        model = AdvertiserTikTok
        fields = ['nombre', 'descripcion']

class CampaignTikTokForm(forms.ModelForm):
    class Meta:
        model = CampaignTikTok
        fields = ['advertiser', 'nombre', 'objetivo', 'presupuesto']

class AdGroupTikTokForm(forms.ModelForm):
    class Meta:
        model = AdGroupTikTok
        fields = ['campaign', 'nombre', 'segmentacion']

class AdTikTokForm(forms.ModelForm):
    class Meta:
        model = AdTikTok
        fields = ['adgroup', 'nombre', 'contenido', 'url', 'imagen']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
# ---------------------- MIS VACANTES ----------------------#