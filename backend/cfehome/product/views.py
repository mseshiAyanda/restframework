from rest_framework import generics, mixins

from .models import Products
from .serializers import ProductSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


from api.mixins import StaffEditorPermissionMixin

class ProductListCreateAPIView(StaffEditorPermissionMixin, generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializers

    def perform_create(self, serializer):

        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') 
             
        if content is None:
            content = title
        serializer.save(content=content)
    

class ProductDetailAPIView(StaffEditorPermissionMixin, generics.RetrieveAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializers

pruduct_detail_view = ProductDetailAPIView.as_view()        

class ProductUpdateAPIView(StaffEditorPermissionMixin, generics.UpdateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializers 
    lookup_field = 'pk' 

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title
     
class ProductDestroyAPIView(StaffEditorPermissionMixin, generics.DestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializers 
    lookup_field = 'pk' 

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
    

class ProductListAPIView(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializers

pruduct_list_view = ProductListAPIView.as_view()

class ProductMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
    ):
    queryset = Products.objects.all()
    serializer_class = ProductSerializers
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args,**kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
            return self.create(request, *args, **kwargs)

product_mixin_view = ProductMixinView.as_view()      

# @api_view(["POST", "GET"])
# def product_alt_view(request, pk=None, *args, **kwargs):
#     method = request.method

#     if method == "GET":
#         if pk is not None:
#             obj = get_object_or_404(Products, pk=pk)
#             data = ProductSerializers(obj, many=False).data
#             return Response(data)
    
#         qs = Products.objects.all()
#         data = ProductSerializers(qs, many=True).data
#         return Response(data)
    
      
#     if method == "POST":
#         serializer = ProductSerializers(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             title = serializer.validated_data.get('title')
#             content = serializer.validated_data.get('content') or None
#             if content is None:
#                 content = title
#                 serializer.save(content=content)
#                 return Response(serializer.data)
#             return Response({"invalid": "not good data"}, status=400) 
    

         