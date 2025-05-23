from django import forms
from .models import Campaign, AdSet, Ad, Creative, Vacante

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['nombre', 'objective', 'plataforma']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['plataforma'].widget = forms.HiddenInput(attrs={'id': 'plataforma-input'})

class AdSetForm(forms.ModelForm):
    class Meta:
        model = AdSet
        fields = ['nombre', 'campaign_id', 'daily_budget', 'billing_event', 'optimization_goal', 'status', 'plataforma']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['plataforma'].widget = forms.HiddenInput(attrs={'id': 'plataforma-input'})


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['nombre', 'adset_id', 'status', 'creative_id', 'plataforma']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['plataforma'].widget = forms.HiddenInput(attrs={'id': 'plataforma-input'})



class CreativeForm(forms.ModelForm):
    class Meta:
        model = Creative
        fields = ['nombre', 'name', 'message', 'body', 'image_url', 'link', 'call_to_action', 'plataforma']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['plataforma'].widget = forms.HiddenInput(attrs={'id': 'plataforma-input'})

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