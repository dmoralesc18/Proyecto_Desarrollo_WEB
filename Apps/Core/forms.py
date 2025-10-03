from django import forms

class SoporteForm(forms.Form):
    nombre = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your full name'
        }),
        label='Full Name'
    )
    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        }),
        label='Email Address'
    )
    asunto = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Brief description of your issue'
        }),
        label='Subject'
    )
    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Please describe your issue in detail...'
        }),
        label='Message'
    )