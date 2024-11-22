from django.urls import path
from .views import VendorListCreateAPIView, VendorRetrieveUpdateDeleteAPIView

urlpatterns = [
    path('', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('<int:pk>/', VendorRetrieveUpdateDeleteAPIView.as_view(), name='vendor-retrieve-update-delete'),
]
