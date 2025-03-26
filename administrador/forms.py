from django import forms
from .models import Campaign, AdSet, Ad

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['nombre', 'red_social', 'hashtags', 'objective', 'formato']
    
    def __init__(self, *args, **kwargs):
        red_social = kwargs.pop('red_social', None)  # Extraer red_social
        super().__init__(*args, **kwargs)

        # Ocultar los campos adicionales por defecto
        self.fields['hashtags'].widget = forms.HiddenInput()
        self.fields['objective'].widget = forms.HiddenInput()
        self.fields['formato'].widget = forms.HiddenInput()

        # Mostrar los campos dependiendo de la red social seleccionada
        if red_social == 'tiktok':
            self.fields['hashtags'].widget = forms.TextInput(attrs={'placeholder': 'Ingresa hashtags'})
        elif red_social in ['facebook', 'instagram']:
            self.fields['formato'].widget = forms.TextInput()
            self.fields['objective'].widget = forms.Select(choices=Campaign.OBJECTIVES)

class AdSetForm(forms.ModelForm):
    class Meta:
        model = AdSet
        fields = ['nombre', 'campaign_id', 'daily_budget', 'billing_event', 'optimization_goal', 'status']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        '''
        # Ocultar los campos adicionales por defecto
        self.fields['hashtags'].widget = forms.HiddenInput()
        self.fields['objective'].widget = forms.HiddenInput()
        self.fields['formato'].widget = forms.HiddenInput()

        # Mostrar los campos dependiendo de la red social seleccionada
        if red_social == 'tiktok':
            self.fields['hashtags'].widget = forms.TextInput(attrs={'placeholder': 'Ingresa hashtags'})
        elif red_social in ['facebook', 'instagram']:
            self.fields['formato'].widget = forms.TextInput()
            self.fields['objective'].widget = forms.Select(choices=Campaign.OBJECTIVES)'
        '''

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['nombre', 'adset_id', 'status', 'creative', 'access_token']
    
    def __init__(self, *args, **kwargs):
        red_social = kwargs.pop('red_social', None)  # Extraer red_social
        super().__init__(*args, **kwargs)

        '''
        # Ocultar los campos adicionales por defecto
        self.fields['hashtags'].widget = forms.HiddenInput()
        self.fields['objective'].widget = forms.HiddenInput()
        self.fields['formato'].widget = forms.HiddenInput()

        # Mostrar los campos dependiendo de la red social seleccionada
        if red_social == 'tiktok':
            self.fields['hashtags'].widget = forms.TextInput(attrs={'placeholder': 'Ingresa hashtags'})
        elif red_social in ['facebook', 'instagram']:
            self.fields['formato'].widget = forms.TextInput()
            self.fields['objective'].widget = forms.Select(choices=Campaign.OBJECTIVES)
        '''