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


class LoginForm(forms.Form):
    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tu@correo.com'}),
        label='Correo'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        label='Contraseña'
    )


class ProfileForm(forms.Form):
    nombre = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Nombre'
    )
    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Correo'
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Dejar en blanco para no cambiar'}),
        label='Contraseña'
    )


class UserForm(forms.Form):
    nombre = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Nombre'
    )


class FirstUserSetupForm(forms.Form):
    nombre = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
        label='Nombre'
    )
    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'admin@tu-dominio.com'}),
        label='Correo'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Contraseña'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirmar contraseña'
    )

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        return cleaned
    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Correo'
    )
    rol = forms.ChoiceField(
        choices=(('Administrador','Administrador'), ('Supervisor','Supervisor'), ('Cliente','Cliente')),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Rol'
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Contraseña'
    )
