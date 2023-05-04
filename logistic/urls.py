from django.urls import path, include
from rest_framework import routers
from .views import ProductViewSet, StockViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'stocks', StockViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
