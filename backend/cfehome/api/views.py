import json
from django.forms.models import model_to_dict

from rest_framework.decorators import api_view
from rest_framework.response import Response


from product.models import Products
from product.serializers import ProductSerializers

@api_view(["POST"])
def api_home(request, *args, **kwargs):
    serializer = ProductSerializers(data=request.data)
    if serializer.is_valid(raise_exception=True):
        #instance = serializer.save()
        print(serializer.data)
        return Response(serializer.data)
    return Response({"invalid": "not good data"}, status=400) 
    