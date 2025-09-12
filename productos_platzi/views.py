import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from requests.exceptions import RequestException
from .forms import ProductoForm

BASE_URL = "https://api.escuelajs.co/api/v1/products"

def home(request):
    return render(request, "home.html")

@csrf_exempt

def lista_productos(request):
    response = requests.get(BASE_URL)
    productos = response.json() if response.status_code == 200 else []
    return render(request, "lista_productos.html", {"productos": productos})

def detalle_producto(request, producto_id):
    response = requests.get(f"{BASE_URL}/{producto_id}")
    if response.status_code == 200:
        productos = response.json()
    else:
        messages.success(request, "No se pudo cargar el producto")
        return redirect("lista_productos")
    return render(request, "detalle_producto.html", {"producto": productos})

@login_required(login_url='accounts:login')
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

@login_required(login_url='accounts:login')   
def update_producto(request, producto_id):
    response = requests.get(f"{BASE_URL}/{producto_id}")
    if response.status_code != 200:
        messages.error(request, "No se puede cargar el producto para editar.")
        return redirect("lista_productos")
    
    producto = response.json()
    
    form = ProductoForm(initial={
        "title": producto["title"],
        "price": producto["price"],
        "description": producto["description"],
        "categoryId": producto["category"]["id"],
        "image": producto["images"][0] if producto.get("images") else ""
    })
    
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            update_data = {
                "title": data["title"],
                "price": float(data["price"]),
                "description": data["description"],
                "categoryId": data["categoryId"],
            }
            if data.get("image"):  
                update_data["images"] = [data["image"]]

            put_response = requests.put(f"{BASE_URL}/{producto_id}", json=update_data)
            
            if put_response.status_code == 200:
                messages.success(request, f"Producto actualizado: {data['title']}")
                return redirect("detalle_producto", producto_id=producto_id)
            else:
                messages.error(request, f"Error al actualizar el producto: {put_response.text}")
    
    return render(request, "update_producto.html", {"form": form, "producto": producto})

csrf_exempt

@login_required(login_url='accounts:login')
def delete_producto(request, producto_id):
    if request.method == "POST":
        response = requests.delete(f"{BASE_URL}/{producto_id}")
        if response.status_code == 200:
            messages.success(request, "🚮 Producto eliminado exitosamente.")
        else:
            messages.error(request, "Error al emliminar el producto")
        return redirect("lista_productos") 
    
    return render(request, "productos/detalle_confirm.html", {"producto_id": producto_id})   