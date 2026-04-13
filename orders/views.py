from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from restaurants.models import FoodItem
from .models import Cart, CartItem, Order, OrderItem

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'orders/cart.html', {'cart': cart})

@login_required
def add_to_cart(request, food_item_id):
    food_item = get_object_or_404(FoodItem, id=food_item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, food_item=food_item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'{food_item.name} added to cart!')
    return redirect('restaurant_detail', pk=food_item.restaurant.pk)

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def place_order(request):
    if request.method == 'POST':
        cart = get_object_or_404(Cart, user=request.user)
        delivery_address = request.POST.get('delivery_address')
        if not cart.cart_items.exists():
            messages.error(request, 'Your cart is empty!')
            return redirect('cart')
        order = Order.objects.create(
            user=request.user,
            total_price=cart.get_total(),
            delivery_address=delivery_address,
        )
        for cart_item in cart.cart_items.all():
            OrderItem.objects.create(
                order=order,
                food_item=cart_item.food_item,
                quantity=cart_item.quantity,
                price=cart_item.food_item.price,
            )
        cart.cart_items.all().delete()
        return redirect('order_confirmation', order_id=order.id)
    return redirect('cart')

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_confirmation.html', {'order': order})


@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')