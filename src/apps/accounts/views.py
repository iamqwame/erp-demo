from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from utils.pagination import CustomPagination
from .serializers import AccountSerializer
from .models import Account
from utils.response_formatter import custom_response

class AccountListCreateAPIView(ListCreateAPIView):
    """
    Handles listing and creating accounts with pagination.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    pagination_class = CustomPagination

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = custom_response(
                message="Account created successfully",
                code=201,
                data=serializer.data
            )
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(custom_response(
            message="Account creation failed",
            code=400,
            errors=serializer.errors
        ), status=status.HTTP_400_BAD_REQUEST)


class AccountRetrieveUpdateDeleteAPIView(APIView):
    """
    Handles retrieving, updating, and deleting an account by ID.
    """

    @swagger_auto_schema(
        operation_summary="Retrieve Account",
        operation_description="Retrieve details of a specific account by ID.",
        responses={200: AccountSerializer, 404: "Account not found"},
    )
    def get(self, request, pk):
        try:
            account = Account.objects.get(pk=pk)
            serializer = AccountSerializer(account)
            response_data = custom_response(
                message="Account retrieved successfully",
                code=200,
                data=serializer.data,
            )
            return Response(response_data, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            response_data = custom_response(
                message="Account not found",
                code=404,
                errors={"detail": "Account does not exist"},
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Update Account",
        operation_description="Update details of a specific account by ID.",
        request_body=AccountSerializer,
        responses={200: AccountSerializer, 404: "Account not found"},
    )
    def put(self, request, pk):
        try:
            account = Account.objects.get(pk=pk)
            serializer = AccountSerializer(account, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_data = custom_response(
                    message="Account updated successfully",
                    code=200,
                    data=serializer.data,
                )
                return Response(response_data, status=status.HTTP_200_OK)
            response_data = custom_response(
                message="Account update failed",
                code=400,
                errors=serializer.errors,
            )
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Account.DoesNotExist:
            response_data = custom_response(
                message="Account not found",
                code=404,
                errors={"detail": "Account does not exist"},
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Delete Account",
        operation_description="Delete a specific account by ID.",
        responses={204: "No content", 404: "Account not found"},
    )
    def delete(self, request, pk):
        try:
            account = Account.objects.get(pk=pk)
            account.delete()
            response_data = custom_response(
                message="Account deleted successfully",
                code=204,
                data=None,
            )
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        except Account.DoesNotExist:
            response_data = custom_response(
                message="Account not found",
                code=404,
                errors={"detail": "Account does not exist"},
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
