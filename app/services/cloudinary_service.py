import cloudinary
import cloudinary.uploader
from ..core.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

class CloudinaryService:
    @staticmethod
    async def upload_image(file, folder: str = "clothes") -> str:
        """
        Upload image to Cloudinary and return the secure URL
        """
        try:
            result = cloudinary.uploader.upload(
                file.file,
                folder=folder,
                resource_type="auto"
            )
            return result.get("secure_url")
        except Exception as e:
            raise Exception(f"Error uploading to Cloudinary: {str(e)}")
    
    @staticmethod
    async def delete_image(image_url: str) -> bool:
        """
        Delete image from Cloudinary by URL
        """
        try:
            parts = image_url.split('/')
            public_id_with_extension = parts[-1]
            public_id = f"clothes/{public_id_with_extension.split('.')[0]}"
            
            result = cloudinary.uploader.destroy(public_id)
            return result.get("result") == "ok"
        except Exception:
            return False