from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='homepage'),
    path('category/', views.category, name="category"),
    path('details/<slug:slug>/', views.product_details, name='product_details'),
    path('update_item/', views.updateItem, name="update_item"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('process_order/', views.processOrder, name="process_order"),
    path('search/', views.search, name="search"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('confirm/', views.confirmPage, name="confirm"),
    path('profile/', views.profilePage, name="profile"),
    #path('/category', views.CategoryView.as_view(), name='category'),
]
