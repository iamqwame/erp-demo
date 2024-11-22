from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from utils.pagination import CustomPagination
from .serializers import CustomerSerializer
from .models import Customer
from utils.response_formatter import custom_response

class CustomerListCreateAPIView(ListCreateAPIView):
    """
    Handles listing and creating customers with pagination.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
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
                message="Customer created successfully",
                code=201,
                data=serializer.data
            )
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(custom_response(
            message="Customer creation failed",
            code=400,
            errors=serializer.errors
        ), status=status.HTTP_400_BAD_REQUEST)


class CustomerRetrieveUpdateDeleteAPIView(APIView):
    """
    Handles retrieving, updating, and deleting a customer by ID.
    """

    @swagger_auto_schema(
        operation_summary="Retrieve Customer",
        operation_description="Retrieve details of a specific customer by ID.",
        responses={200: CustomerSerializer, 404: "Customer not found"},
    )
    def get(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer)
            response_data = custom_response(
                message="Customer retrieved successfully",
                code=200,
                data=serializer.data,
            )
            return Response(response_data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            response_data = custom_response(
                message="Customer not found",
                code=404,
                errors={"detail": "Customer does not exist"},
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Update Customer",
        operation_description="Update details of a specific customer by ID.",
        request_body=CustomerSerializer,
        responses={200: CustomerSerializer, 404: "Customer not found"},
    )
    def put(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_data = custom_response(
                    message="Customer updated successfully",
                    code=200,
                    data=serializer.data,
                )
                return Response(response_data, status=status.HTTP_200_OK)
            response_data = custom_response(
                message="Customer update failed",
                code=400,
                errors=serializer.errors,
            )
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            response_data = custom_response(
                message="Customer not found",
                code=404,
                errors={"detail": "Customer does not exist"},
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Delete Customer",
        operation_description="Delete a specific customer by ID.",
        responses={204: "No content", 404: "Customer not found"},
    )
    def delete(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
            customer.delete()
            response_data = custom_response(
                message="Customer deleted successfully",
                code=204,
                data=None,
            )
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        except Customer.DoesNotExist:
            response_data = custom_response(
                message="Customer not found",
                code=404,
                errors={"detail": "Customer does not exist"},
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
