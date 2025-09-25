from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import StyleBoard
from poushia_products.models import Product

@login_required
def style_board_view(request):
    board, _ = StyleBoard.objects.get_or_create(user=request.user)
    return render(request, 'styleboard/style_board.html', {'board': board})

@login_required
def add_to_board(request, product_id):
    board, _ = StyleBoard.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    board.products.add(product)
    return redirect('styleboard:view')

@login_required
def remove_from_board(request, product_id):
    board = get_object_or_404(StyleBoard, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    board.products.remove(product)
    return redirect('styleboard:view')