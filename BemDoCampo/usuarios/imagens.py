from django.conf import settings
from datetime import datetime
import os

class MediaRecords:
    def __init__(self) -> None:
        self.datename = datetime.now().strftime("%Y%m%d")
        pass
    
    
    def image_path(self, image, user_id, id_tenda=None):
        if not image:
            return None
        
        extension = image.name.split('.')[-1]
        
        if not id_tenda:
            file_name = f"{user_id}-{self.datename}.{extension}"
        else:
            file_name = f"{user_id}-{id_tenda}-{self.datename}.{extension}"

        image_path = os.path.join(settings.MEDIA_ROOT, "producers", str(user_id), file_name)

        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        return f"producers/{user_id}/{file_name}"
    
    
    def delete_image(self, path_image):
        try:
            if path_image:
                image_path = os.path.join(settings.MEDIA_ROOT, path_image)
                if os.path.exists(image_path):
                    os.remove(image_path)
        except Exception as e:
            print(f"Erro ao deletar a imagem: {e}")