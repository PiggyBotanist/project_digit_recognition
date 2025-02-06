from rest_framework import serializers
from .models import labelled_data


# Define the serializer class that will convert 'labelled_data' model instances into JSON and validate incoming data
class DataSerializer(serializers.ModelSerializer):
    
    # The 'Meta' class is used to configure the serializer’s behavior
    class Meta:
        # Define which model this serializer is for
        model = labelled_data
        
        # Specify the fields from the model that should be included in the serialization
        fields = ('label', 'image')
