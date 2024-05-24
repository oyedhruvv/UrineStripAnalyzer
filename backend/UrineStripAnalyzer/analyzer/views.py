import cv2
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render


def home(request):
    return render(request, 'analyzer/home.html')

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image_file = request.FILES['image']
        path = default_storage.save('tmp/' + image_file.name, ContentFile(image_file.read()))
        img_path = 'media/' + path

        # Process the image to extract colors
        colors = extract_colors(img_path)

        # Remove the saved image file
        default_storage.delete(path)

        return JsonResponse({'colors': colors})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def extract_colors(img_path):
    # Read the image
    image = cv2.imread(img_path)

    # Assuming the strip has 10 distinct color regions
    # Placeholder logic: Just sample 10 points for simplicity
    height, width, _ = image.shape
    step = height // 10
    colors = []

    for i in range(10):
        y = step * i + step // 2
        x = width // 2
        color = image[y, x].tolist()  # Get color at the center of each segment
        colors.append(color)

    return colors
