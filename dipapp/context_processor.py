from dipapp.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, WishList, Address



def default(request):
    categories = Category.objects.all()
    address = None  # Initialize address with None  
    if request.user.is_authenticated:
        try:
            address = Address.objects.get(user=request.user) 
        except Address.DoesNotExist:
            pass
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price']) # getting the quantity of each products, multiplying each items. quantity multiply by it price 
    
    return {
        'categories': categories,
        'address': address,
        # "cart_data": request.session['cart_data_obj'],
        # 'totalcartitems': len(request.session['cart_data_obj']),
        # 'cart_total_amount' : cart_total_amount
    }

     