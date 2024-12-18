from django.urls import path
from main.views import show_main, create_product, show_json, show_xml, show_json_by_id, show_xml_by_id, register_user, login_user, logout_user, edit_Product, delete_Product, add_Product_ajax, create_product_flutter

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-product/', create_product, name='create_product'), 
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('edit-Product/<uuid:id>', edit_Product, name='edit_Product'),
    path('delete-Product/<uuid:id>', delete_Product, name='delete_Product'),
    path('add-Product-ajax/', add_Product_ajax, name='add_Product_ajax'),
    path('create-product-flutter/', create_product_flutter, name='create_product_flutter'),



]