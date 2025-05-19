import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product


@csrf_exempt
def create_product(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        description = data.get("description", "")
        price = data.get("price")
        quantity = data.get("quantity")

        if not name or price is None or quantity is None:
            return JsonResponse({"error": "Name, price, and quantity are required."}, status=400)

        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            quantity=quantity
        )
        return JsonResponse({"message": "Product created", "product_id": product.id}, status=201)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def get_all_products(request):
    if request.method == "GET":
        products = list(Product.objects.values())
        return JsonResponse({"products": products}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def get_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        data = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": str(product.price),
            "quantity": product.quantity,
        }
        return JsonResponse(data, status=200)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)

@csrf_exempt
def add_product(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        quantity = data.get('quantity')

        if not name or not price or not description:
            return JsonResponse({"error": "All fields are required"}, status=400)

        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            quantity=quantity
        )
        return JsonResponse({"message": "Product added successfully", "id": product.id}, status=201)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def update_product(request, product_id):
    if request.method == "PUT":
        try:
            product = Product.objects.get(id=product_id)
            data = json.loads(request.body)

            product.name = data.get("name", product.name)
            product.description = data.get("description", product.description)
            product.price = data.get("price", product.price)
            product.quantity = data.get("quantity", product.quantity)
            product.save()

            return JsonResponse({"message": "Product updated successfully"}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def delete_product(request, product_id):
    if request.method == "DELETE":
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return JsonResponse({"message": "Product deleted successfully"}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)

