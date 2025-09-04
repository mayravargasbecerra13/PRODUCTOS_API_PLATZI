import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import ProductoForm

BASE_URL = "https://api.escuelajs.co/api/v1/products"

def home(request):
    return render(request, "home.html")

@csrf_exempt

def lista_productos(request):
    response = requests.get(BASE_URL)
    productos = response.json() if response.status_code == 200 else []
    return render(request, "lista_productos.html", {"productos": productos})

def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            payload = {
                "title": form.cleaned_data["title"],
                "price": float(form.cleaned_data["price"]),
                "description": form.cleaned_data["description"],
                "categoryId": int(form.cleaned_data["categoryId"]),
                "images": [form.cleaned_data["image"]],
            }

            try:
                resp = requests.post(BASE_URL, json=payload, timeout=10)
                resp.raise_for_status()
            except requests.exceptions.RequestException as e:
                messages.error(request, f"❌ Error al crear producto: {e}")
                return render(request, "crear_producto.html", {"form": form})

            if resp.status_code == 201:
                productos = resp.json()
                messages.success(
                request, f"✅Producto creado exitosamente: ID {productos['id']} - {productos['title']}"
                )
                return redirect("lista_productos")
            else:
                messages.error(request, f"❌ Error API: {resp.status_code} - {resp.text}")
    else:
        form = ProductoForm()
        
    return render(request, "crear_producto.html", {"form": form})
    

