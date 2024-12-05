from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import *

class empSerial(ModelSerializer):
    id = ReadOnlyField()
    class Meta:
        model = Entity
        fields = "__all__"