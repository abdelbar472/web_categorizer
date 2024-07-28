from django.urls import path
from .api_views import SpaceList, SpaceDetail, CategoryList, SubcategoryList, UrlList

urlpatterns = [
    path('spaces/', SpaceList.as_view(), name='space-list'),
    path('spaces/<str:space_name>/', SpaceDetail.as_view(), name='space-detail'),
    path('spaces/<str:space_name>/categories/', CategoryList.as_view(), name='category-list'),
    path('spaces/<str:space_name>/categories/<str:category_name>/subcategories/', SubcategoryList.as_view(), name='subcategory-list'),
    path('spaces/<str:space_name>/categories/<str:category_name>/subcategories/<str:subcategory_name>/urls/', UrlList.as_view(), name='url-list'),
]
