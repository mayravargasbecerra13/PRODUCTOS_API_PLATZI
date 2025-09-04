from django import forms

class ProductoForm(forms.Form):
    title = forms.CharField(
        label="Título", 
        max_length=255, 
        widget=forms.TextInput(attrs={"placeholder": "Nombre del producto"}))
    
    price = forms.DecimalField(
        label="Precio", max_digits=10, 
        decimal_places=2, 
        widget=forms.NumberInput(attrs={"placeholder": "100.00", "step": "0.01"}))
    
    description = forms.CharField(
        label="Descripción", 
        widget=forms.Textarea(attrs={"placeholder": "Descripción del producto", "rows": 4}))
    
    categoryId = forms.IntegerField(
        label="ID de categoría", 
        widget=forms.NumberInput(attrs={"placeholder": "1"}))
    
    images = forms.URLField(label="URL de la imagen", required=False)