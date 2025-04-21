from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from main.models import Avatar

def home(response):
    return render(response,'main/index.html',{})


@csrf_exempt
def upload_avatar(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name
        
        # Check if an Avatar with the same file name already exists
        existing_avatar = Avatar.objects.filter(image__endswith=file_name).first()  # Search for the file by name
        
        if existing_avatar:
            # If the file with the same name exists, delete its image file from the file system
            if existing_avatar.image:
                existing_avatar.image.delete()  # Delete the old image file
                existing_avatar.delete()  # Delete the Avatar record
        
        # Create a new Avatar instance with the uploaded file
        avatar = Avatar.objects.create(image=uploaded_file)

        # Get the URL of the uploaded image
        file_url = avatar.image.url
        print(file_url)
        return JsonResponse({'url': file_url}, status=200)

    return JsonResponse({'error': 'Invalid request or no file provided'}, status=400)

@csrf_exempt
def delete_avatar(request, filename):
    if request.method == 'POST':
        print(filename)
        # Check if an Avatar with the same file name already exists
        existing_avatar = Avatar.objects.filter(image__contains=filename).first()  # Search for the file by name
        
        if existing_avatar:
            # If the file with the same name exists, delete its image file from the file system
            if existing_avatar.image:
                existing_avatar.image.delete()  # Delete the old image file
        

            return JsonResponse({'message': f'Avatar with filename {filename} deleted successfully.'}, status=200)
        else:
            return JsonResponse({'error': f'Avatar with filename {filename} not found.'}, status=404)

    return JsonResponse({'error': 'Invalid request method, POST required.'}, status=405)

