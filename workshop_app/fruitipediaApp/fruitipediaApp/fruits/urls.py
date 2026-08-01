from django.urls import path, include
from .views import (
    index_view,
    dashboard_view,
    fruit_create_view,
    fruit_details_view,
    fruit_edit_view,
    fruit_delete_view,
    category_create_view,
)

urlpatterns = [
    path('', index_view, name='index'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('create-fruit/', fruit_create_view, name='create-fruit'),
    path('<int:pk>/', include([
        path('fruit-details/', fruit_details_view, name='fruit-details'),
        path('fruit-edit/', fruit_edit_view, name='fruit-edit'),
        path('delete-fruit/', fruit_delete_view, name='delete-fruit'),
    ])),
    path('create-category/', category_create_view, name='create-category')
]