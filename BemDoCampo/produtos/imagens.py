from django.conf import settings
import os

class MediaRecords:
    def __init__(self) -> None:
        pass
    
    
    def image_path(self, image, product_id, user_id):
        if not image:
            return "NoPhotoProduct.jpg"
        
        extension = image.name.split('.')[-1]
        file_name = f"{product_id}.{extension}"

        image_path = os.path.join(settings.MEDIA_ROOT, "producers", str(user_id), "prod_img", file_name)

        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        return f"producers/{user_id}/prod_img/{file_name}"
    
    
    def delete_image(self, product):
        try:
            if product:
                image_path = os.path.join(settings.MEDIA_ROOT, product)
                if os.path.exists(image_path):
                    os.remove(image_path)
        except Exception as e:
            print(f"Erro ao deletar a imagem: {e}")