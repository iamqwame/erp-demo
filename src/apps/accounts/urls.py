from django.urls import path
from .views import AccountListCreateAPIView, AccountRetrieveUpdateDeleteAPIView

urlpatterns = [
    path('', AccountListCreateAPIView.as_view(), name='account-list-create'),
    path('<int:pk>/', AccountRetrieveUpdateDeleteAPIView.as_view(), name='account-retrieve-update-delete'),
]
