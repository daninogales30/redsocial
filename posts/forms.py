from django import forms


class PostForm(forms.Form):
    imagen = forms.ImageField(required=False, label="Foto de perfil")
    texto = forms.CharField(widget=forms.Textarea())