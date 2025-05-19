from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
from shopping_cart.models import CartItem
from .models import Order, OrderItem
from django.conf import settings
from django.contrib.auth import get_user_model
import jwt
import json

User = get_user_model()

@csrf_exempt
def checkout(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    # ✅ Extract token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JsonResponse({"error": "Authorization header missing or invalid"}, status=401)

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = User.objects.get(id=payload["user_id"])
    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Token has expired"}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({"error": "Invalid token"}, status=401)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    # ✅ Now you're using a valid authenticated user
    try:
        cart_items = CartItem.objects.filter(user=user)
        if not cart_items.exists():
            return JsonResponse({"error": "Cart is empty"}, status=400)

        total = sum(item.product.price * item.quantity for item in cart_items)
        order = Order.objects.create(user=user, total_price=total)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            item.delete()

        send_mail(
            'Order Confirmation',
            f'Your order #{order.id} has been placed.',
            'annemicheni5@gmail.com',
            [user.email],
            fail_silently=False,
        )

        return JsonResponse({"message": "Order placed successfully", "order": str(order.id)})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

