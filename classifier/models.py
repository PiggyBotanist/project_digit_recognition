import random
import string
from django.db import models

# Create unique ID function
def generate_unique_id():
    length = 12  # Define length of ID
    
    while True:
        # Generate a random string of uppercase letters with the specified length
        id = ''.join(random.choices(string.ascii_uppercase, k=length))
        
        # Ensure the ID is unique by checking if it already exists in the database
        if labelled_data.objects.filter(id=id).count() == 0:
            break  # If the ID is unique, break the loop

    return id

# Define your model
class labelled_data(models.Model):
    id = models.CharField(max_length=12, default=generate_unique_id, unique=True, primary_key=True)     # Set max_length to 12 to match the unique ID length
    created_at = models.DateTimeField(auto_now_add=True)                                                # Automatically set the date when the record is created
    label = models.IntegerField(null=False)                                                             # The label is an integer, cannot be null
    image = models.CharField(max_length=10000)                                                          # Store the image as a string (base64 or other format)
