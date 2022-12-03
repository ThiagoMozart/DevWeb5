from django.template.context_processors import static
from django.urls import path
from app import views
from warhammer import settings

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('history/', views.history, name="history"),
    path('chapter/', views.chapter, name="chapter"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('shop/', views.shop, name="shop"),
    path('selling/', views.selling, name="selling"),
    path('show_product/<int:id>', views.show_product, name="show_product"),
    path('edit_product/<int:id>', views.edit_product, name="edit_product"),
    path('remove_product', views.remove_product, name="remove_product"),
]
