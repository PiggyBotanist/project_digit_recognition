from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import DataSerializer
from rest_framework import status
from .models import labelled_data
import torch.nn.functional as F
from django.apps import apps
from PIL import Image
import numpy as np
import base64
import torch
import json
import io

# Define a view that will handle requests to make prediction
class PredictView(APIView):
    def post(self, request, format=None):
        try:
            # Retrieve the raw binary image data from the request body
            image_data = request.body.decode('utf-8')
            json_data = json.loads(image_data)
            
            # Extract the base64 image data and decode it
            image = json_data['image']
            image = image.replace("data:image/png;base64,", "")  # Remove the data URI prefix
            image = base64.b64decode(image)
            
            # Open the image with PIL
            image = Image.open(io.BytesIO(image))
            
            # Convert to grayscale and resize (for example, MNIST 28x28 image size)
            image = image.convert("L").resize((28, 28))  # Convert to grayscale and resize

            # Convert the image to a NumPy array
            image_array = np.array(image)
            
            # Normalize the image data (scale to [0, 1] range)
            normalized_image = image_array / 255.0
            
            # Flatten the image to create a 1D array
            flatten_image = normalized_image.flatten()
            
            # Convert to a PyTorch tensor
            image_tensor = torch.tensor(flatten_image)
            
            # Retrieve the model from the app config
            classifier_config = apps.get_app_config('classifier')
            model = classifier_config.model
            
            # Perform prediction (model expects a tensor)
            output = model(image_tensor.float())  # Ensure the tensor type is float
            
            # Apply softmax to get probabilities for each class
            probabilities = F.softmax(output, dim=0)
            
            # Get the predicted class by finding the index with the highest probability
            predicted_class = torch.argmax(probabilities)
            
            # Prepare response data
            response_data = {
                "prediction": predicted_class.item(),
                "probabilities": probabilities.detach().numpy().tolist()
            }
            
            # Return the prediction and probabilities as a response
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any exceptions and return a meaningful error response
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Define a view that will handle requests to save data
class SaveView(APIView):
    # Specify the serializer class to be used for data validation and transformation
    serializer_class = DataSerializer
    
    # Define the POST method that will be triggered when data is sent to this endpoint
    def post(self, request, format=None):
        # Create an instance of the serializer with the incoming data
        serializer = self.serializer_class(data=request.data)
        
        # Check if the data is valid according to the serializer's validation rules
        if serializer.is_valid():
            
            # Retrieve the 'label' and 'image' values from the serializer's validated data
            label = serializer.data.get('label')
            image = serializer.data.get('image')
            
            # Check if the label is a valid integer between 0 and 9
            if (label > -1 and label < 10):
                # Create a new instance of the 'labelled_data' model with the valid data
                data = labelled_data(label=label, image=image)
                
                # Save the new data object to the database
                data.save()
                
                # Return a successful response with the serialized data of the saved object
                return Response(DataSerializer(data).data, status=status.HTTP_201_CREATED)
        
        # If the serializer data is invalid or the label is not between 0 and 9, return an error response
        return Response({"error": "failed to save data..."}, status=status.HTTP_400_BAD_REQUEST)
