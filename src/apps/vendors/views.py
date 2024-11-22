from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from utils.pagination import CustomPagination
from .serializers import VendorSerializer
from .models import Vendor
from utils.response_formatter import custom_response

class VendorListCreateAPIView(ListCreateAPIView):
    """
    Handles listing and creating vendors with pagination.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
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
                message="Vendor created successfully",
                code=201,
                data=serializer.data
            )
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(custom_response(
            message="Vendor creation failed",
            code=400,
            errors=serializer.errors
        ), status=status.HTTP_400_BAD_REQUEST)

class VendorRetrieveUpdateDeleteAPIView(APIView):
    """
    Handles retrieving, updating, and deleting a vendor by ID.
    """

    @swagger_auto_schema(
        operation_summary="Retrieve Vendor",
        operation_description="Retrieve details of a specific vendor by ID.",
        responses={200: VendorSerializer, 404: "Vendor not found"},
    )
    def get(self, request, pk):
        try:
            vendor = Vendor.objects.get(pk=pk)
            serializer = VendorSerializer(vendor)
            response_data = custom_response(
                message="Vendor retrieved successfully",
                code=200,
                data=serializer.data,
            )
            return Response(response_data, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            response_data = custom_response(
                message="Vendor not found",
                code=404,
                errors={"detail": "Vendor does not exist"},
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Update Vendor",
        operation_description="Update details of a specific vendor by ID.",
        request_body=VendorSerializer,
        responses={200: VendorSerializer, 404: "Vendor not found"},
    )
    def put(self, request, pk):
        try:
            vendor = Vendor.objects.get(pk=pk)
            serializer = VendorSerializer(vendor, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_data = custom_response(
                    message="Vendor updated successfully",
                    code=200,
                    data=serializer.data,
                )
                return Response(response_data, status=status.HTTP_200_OK)
            response_data = custom_response(
                message="Vendor update failed",
                code=400,
                errors=serializer.errors,
            )
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Vendor.DoesNotExist:
            response_data = custom_response(
                message="Vendor not found",
                code=404,
                errors={"detail": "Vendor does not exist"},
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Delete Vendor",
        operation_description="Delete a specific vendor by ID.",
        responses={204: "No content", 404: "Vendor not found"},
    )
    def delete(self, request, pk):
        try:
            vendor = Vendor.objects.get(pk=pk)
            vendor.delete()
            response_data = custom_response(
                message="Vendor deleted successfully",
                code=204,
                data=None,
            )
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        except Vendor.DoesNotExist:
            response_data = custom_response(
                message="Vendor not found",
                code=404,
                errors={"detail": "Vendor does not exist"},
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
