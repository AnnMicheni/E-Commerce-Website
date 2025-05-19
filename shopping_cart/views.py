from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import CartItem
from product_management.models import Product
from django.contrib.auth import get_user_model
import json

User = get_user_model()

@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get("user_id")
        product_id = data.get("product_id")
        quantity = data.get("quantity", 1)

        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)

        item, created = CartItem.objects.get_or_create(user=user, product=product)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()

        return JsonResponse({"message": "Item added to cart"}, status=200)

@csrf_exempt
def update_cart_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get("user_id")
        product_id = data.get("product_id")
        quantity = data.get("quantity")

        item = CartItem.objects.get(user_id=user_id, product_id=product_id)
        item.quantity = quantity
        item.save()

        return JsonResponse({"message": "Cart updated"}, status=200)

@csrf_exempt
def remove_from_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get("user_id")
        product_id = data.get("product_id")

        CartItem.objects.filter(user_id=user_id, product_id=product_id).delete()
        return JsonResponse({"message": "Item removed from cart"}, status=200)
