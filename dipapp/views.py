from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from dipapp.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, WishList, Address
from .utils import get_user_country, get_currency_symbol
from django.views import View
from django.db.models import Count, Avg
from dipapp.forms import ProductReviewForm
from django.db.models import Q
# from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from django.contrib import messages
from django.template.loader import render_to_string

def home(request):
    products = Product.objects.filter(product_status ="published", featured = True)
    categories = Category.objects.all()[:4]
    # count_category_products = Category.objects.annotate(product_count=Count('product'))
    user_country = get_user_country(request)
    currency_symbol = get_currency_symbol(user_country)
    print(user_country)
    
    # Create the context dictionary
    context = {
        'products': products,
        'categories': categories,
        # 'count_category_products':count_category_products
        'user_country': user_country,
        'currency_symbol' : currency_symbol
    }

    # Render the template with the context data
    return render(request, 'dipapp/home.html', context)


def category_list_view(request):
    categories = Category.objects.all()

    context = {
        'categories': categories,
    }

    return render(request, 'dipapp/category-list.html', context)


def shop(request):
    products = Product.objects.filter(product_status ="published")
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
    }

    return render(request, 'dipapp/shop.html', context)


def category_product_list_view(request, cid):
#     products = Product.objects.filter(product_status ="published", category = category) retrieves a collection of product objects that meet two conditions:
# product_status ="published": Filters for products marked as "published."
# category = category: Filters for products belonging to the retrieved category.
    category = Category.objects.get(cid = cid)
    products = Product.objects.filter(product_status ="published", category = category)
    
    context = {
        
        'category': category,
        'products': products,
    }

    return render(request, 'dipapp/category-product-list.html', context)


def product_detail_view(request, pid):
    product = Product.objects.get(pid = pid)
    # product = get_object_or_404(Product, id = pid)
    products = Product.objects.filter(category = product.category).exclude(pid = pid) # filtering by the category in the Product model, if the category = the product that we are currently viewing, meaning that filtering by the category of that product. that is show all the products that have the same categories, and also exclude what so ever product that you are currently viewing or that you are on.
    
    # getting all reviews that is related to the product that we are currently viewing.
    reviews  = ProductReview.objects.filter(product = product).order_by("-date")
    
    # filter all the images that is related to the product that you are getting it details, it will get all it corresponding images.
    p_image = product.p_images.all()
    
    # Getting average review of the product, checking average on the rating field.
    average_rating = ProductReview.objects.filter(product = product).aggregate(rating = Avg('rating'))

# form the we are passing to the template.
    review_form = ProductReviewForm()
    
    make_review = True
    
    # if a user has make review before they shouldnt be able to make a review any longer.
    
    if request.user.is_authenticated:
        # filtering by the logged in user.
        user_review_count = ProductReview.objects.filter(user = request.user, product = product).count() # they should only be restrcted on the product that they have comment on, meaning that one product should have just one comment from just one user, a user can only make a review once on one product.. 

        if user_review_count > 0:
            make_review = False
    context = {
        'p': product,
        'p_image': p_image,
        'make_review' : make_review,
        'review_form': review_form,
        'average_rating': average_rating,
        'reviews' : reviews,
        'products': products
    }

    return render(request, 'dipapp/product_detail.html', context)


def tag_list(request, tag_slug = None):
    products = Product.objects.filter(product_status ="published").order_by("-id")
    tag = None # initially is should have nothing in it.
    if tag_slug:
        tag = get_object_or_404(Tag, slug =  tag_slug) # the second argument (slug) is in the Tag model that we installed from pip, and we are saying slug = whatsoever slug that we will be passing in.
        # when ever there is a slug we want to get all the products that is related to that slug.
        products = products.filter(tags__in=[tag]) # [tags__in] , take note that the product model has a field called tag, checking if we have this (tags__in) in what so ever product that we are filtering. 
    context = {
        "products":products,
        'tag': tag
    }
    return render(request, 'dipapp/tag.html', context)



def ajax_add_review(request, pid):
    product = Product.objects.get(pk  = pid)
    user = request.user
    # we want to create new review with whatsoever the user pass in the review form.
    # [user] field in the [ProductReview] model
    review   = ProductReview.objects.create(
        user = user,
        product = product,
        # getting the review that the user is passing in.
        review = request.POST['review'],
        rating = request.POST['rating']
    )
    
    context = {
        'user':user.username,
        'review': request.POST['review'],
        'rating' : request.POST['rating']
    }
    # getting the average reviews
    average_reviews = ProductReview.objects.filter(product = product).aggregate(rating = Avg("rating"))
    
    return JsonResponse(
        {
            'bool':True,
            'context': context,
            'average_reviews': average_reviews
        }
    )


def search_view(request):
    query = request.GET.get("q")
    if query:
        # Filter products based on the query
        products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(category__title__icontains=query) | Q(price__icontains=query) | Q(tags__name__icontains=query)).order_by("-date")
        product_count = products.count()
    else:
        # If no query is provided, return all products or handle as needed
        products = Product.objects.all().order_by("-date")
        product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
        "query": query
    }
    return render(request, 'dipapp/shop.html', context)


def add_to_cart(request):
    cart_product = {} # This will temporarily store information about the product being added
    cart_product[str(request.GET['id'])] = { # Creates a key-value pair in cart_product.
        'title':request.GET['title'],
        'qty':request.GET['qty'],
        'price':request.GET['price'],
        'image':request.GET['image'],
        'pid':request.GET['pid']
        } # get the current product id.

    # check if there is cart data inside the session the user is using, :  checks if there's already a key named 'cart_data_obj' in the user's session. The session is a temporary storage area for data associated with the user's web browsing session.
    # * If the key exists, the code proceeds to update the existing cart data.
# If the key doesn't exist, the code creates a new cart in the session.
    if 'cart_data_obj' in request.session: # Get the current session.
        if str(request.GET['id']) in request.session['cart_data_obj']: # checks if the product being added (identified by its ID) already exists in the existing cart data (request.session['cart_data_obj'])
            # * If the product is already in the cart ✅.: 
                    # ?  updates the quantity of the existing product in the cart. It retrieves the quantity from the cart_product dictionary and converts it to an integer using int()
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data) # ensures the changes are reflected in the cart_data dictionary.
            request.session['cart_data_obj'] = cart_data #  updates the cart data stored in the user's session with the modified cart_data dictionary.
            
        else:
                        # ! If the product is not already in the cart:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product) # The entire cart_product dictionary (containing the new product's information) is merged into the existing cart_data using cart_data.update(cart_product).

            request.session['cart_data_obj'] = cart_data
            
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({
        "data":request.session['cart_data_obj'],
        'totalcartitems': len(request.session['cart_data_obj'])
    })
    
def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price']) # getting the quantity of each products, multiplying each items. quantity multiply by it price
            
            
        return render(request, 'dipapp/cart.html', {
            "cart_data": request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount' : cart_total_amount
        })
    else:
        messages.warning(request, "Your cart is empty")
        return redirect('home')


def delete_item_from_cart(request):
    product_id = str(request.GET['id']) #  Retrieves the ID of the product to be deleted from the HTTP GET request parameters and converts it into a string.
    if 'cart_data_obj' in request.session: # Checks if the user's session contains a dictionary called 'cart_data_obj', which presumably stores shopping cart items.
        if product_id in request.session['cart_data_obj']: # Checks if the product ID exists as a key within the cart dictionary.
            
            cart_data = request.session['cart_data_obj'] # Stores the current cart data in a variable.
            del request.session['cart_data_obj'][product_id] # Deletes the dictionary entry for the product being removed
            request.session['cart_data_obj'] = cart_data # Saves the modified cart data back into the session.

    cart_total_amount = 0 # Initializes a variable to store the new cart total.
    if 'cart_data_obj' in request.session: # Checks if the cart is not empty.
        for p_id, item in request.session['cart_data_obj'].items(): # Iterates through each item in the cart data.
            cart_total_amount += int(item['qty']) * float(item['price']) # Multiplies the quantity of each item by its price and adds it to the running total.
    
    context = render_to_string("dipapp/async/cart-list.html", {"cart_data": request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount' : cart_total_amount}) # This rendering includes the updated cart data, total items, and total amount.
    return JsonResponse({
        "data": context,
        'totalcartitems': len(request.session['cart_data_obj']) # The total number of items remaining in the cart.
    })
    
    
def update_cart(request):
    product_id = str(request.GET['id']) 
    product_qty = request.GET['qty']

    if 'cart_data_obj' in request.session: 
        if product_id in request.session['cart_data_obj']: 
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            
            request.session['cart_data_obj'] = cart_data 

    cart_total_amount = 0
    if 'cart_data_obj' in request.session: 
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price']) 
    
    context = render_to_string("dipapp/async/cart-list.html", {"cart_data": request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount' : cart_total_amount}) 
    return JsonResponse({
        "data": context,
        'totalcartitems': len(request.session['cart_data_obj']) 
    })
        
def checkout_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session: 
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price']) 
        
        
        return render(request, 'dipapp/checkout.html', {
            "cart_data": request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount' : cart_total_amount
        })




# def cart_view(request):
#     cart_total_amount = 0
#     if 'cart_data_obj' in request.session:
        
#         for p_id, item in request.session['cart_data_obj'].items():
#             print(item)
#             try:
#                 qty = int(item.get('qty', 0))
#                 price = float(item.get('price', 0))
#                 cart_total_amount += qty * price
#             except (ValueError, TypeError):
#                 # Handle conversion errors
#                 messages.warning(request, f"Invalid quantity or price for item with ID {p_id}")
               
            
#         return render(request, 'dipapp/cart.html', {
#             "cart_data": request.session['cart_data_obj'],
            
#             'totalcartitems': len(request.session['cart_data_obj']),
#             'cart_total_amount' : cart_total_amount
#         })
        
#     else:
#         messages.warning(request, "Your cart is empty")
#         return redirect('home')
        
    