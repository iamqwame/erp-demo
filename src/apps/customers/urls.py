from django.urls import path
from .views import CustomerListCreateAPIView, CustomerRetrieveUpdateDeleteAPIView

urlpatterns = [
    path('', CustomerListCreateAPIView.as_view(), name='customer-list-create'),
    path('<int:pk>/', CustomerRetrieveUpdateDeleteAPIView.as_view(), name='customer-retrieve-update-delete'),
]