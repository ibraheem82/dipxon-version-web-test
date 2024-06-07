from django.urls import path, include
from . import views 


urlpatterns = [
    path('', views.home, name="home"),
    path('shop/products', views.shop, name="shop"),
    path('product/<pid>', views.product_detail_view, name="product_detail"),
    path('category/', views.category_list_view, name="category-list"),
    path('category/<cid>/', views.category_product_list_view, name="category-product-list"),
    # Tags
    path('products/tag/<slug:tag_slug>/', views.tag_list, name="tags"),
    # Review
    path('ajax-add-review/<int:pid>/', views.ajax_add_review, name="ajax-add-review"),
    # SEARCH
    path('search/', views.search_view, name="search"),
    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('cart/', views.cart_view, name="cart"),
    # Delete item from cart
    path('delete-from-cart/', views.delete_item_from_cart, name="delete-from-cart"),
    # Update item in cart
    path('update-cart/', views.update_cart, name="update-cart"),
     # checkout
    path('checkout/', views.checkout_view, name="checkout"),
    
    
    # Paypal Route
    path('paypal/', include('paypal.standard.ipn.urls'))
]