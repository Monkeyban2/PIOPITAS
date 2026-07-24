from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import PerfilCliente, Producto


class RegistroClienteForm(forms.Form):
    tipo_doc = forms.ChoiceField(choices=PerfilCliente.TIPO_DOC_CHOICES)
    num_doc = forms.CharField(max_length=20)
    nombres = forms.CharField(max_length=100, min_length=3)
    apellidos = forms.CharField(max_length=100, min_length=3)
    email = forms.EmailField()
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        if User.objects.filter(username=email).exists():
            raise ValidationError('Ya existe una cuenta registrada con ese correo.')
        return email

    def clean_num_doc(self):
        num_doc = self.cleaned_data['num_doc'].strip()
        if PerfilCliente.objects.filter(numero_documento=num_doc).exists():
            raise ValidationError('Ya existe una cuenta registrada con ese número de documento.')
        return num_doc

    def clean_password(self):
        password = self.cleaned_data['password']
        validate_password(password)
        return password

    def guardar(self):
        datos = self.cleaned_data
        usuario = User.objects.create_user(
            username=datos['email'],
            email=datos['email'],
            first_name=datos['nombres'],
            last_name=datos['apellidos'],
            password=datos['password'],
        )
        PerfilCliente.objects.create(
            usuario=usuario,
            tipo_documento=datos['tipo_doc'],
            numero_documento=datos['num_doc'],
        )
        return usuario


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['categoria', 'nombre', 'descripcion', 'precio', 'imagen', 'stock', 'activo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 2}),
        }


class ActualizarStockForm(forms.Form):
    stock = forms.IntegerField(min_value=0)
