from django import forms
from datetime import date,timedelta


class ImageUploadForm(forms.Form):
    # image = forms.ImageField(label = 'Upload an Image', required=True)
    description = forms.CharField(
        label = 'Description of Incident',
        required=False, 
        widget=forms.Textarea(attrs={
        'placeholder': 'Describe the image briefly...',
        'rows': 6
        })
    )

    today = date.today()
    min_date = today - timedelta(days=10)

    date = forms.DateField(
        label="Date of Incident",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
                "max" : today.isoformat(),
                "min" : min_date.isoformat(),
            }))

class ACVForm(forms.Form):
    original_cost = forms.DecimalField(
        label='Original Cost of Product',
        min_value=1, max_digits=10, 
        decimal_places=2,
        widget= forms.NumberInput(
            attrs={
                'placeholder': 'Enter the original cost in INR'
                }))
    
    age = forms.DecimalField(
        label='Age of Product (in years)', 
        min_value=0,
        max_digits=3,
        widget= forms.NumberInput(
            attrs={
                'placeholder': 'Enter age of product in years'
                }))
    
    useful_life = forms.IntegerField(
        label='Useful Life of Product (in years)',
        min_value=1,
        widget= forms.NumberInput(
            attrs={
                'placeholder': 'Enter useful life of product in years'
                }))
    