from fastapi import UploadFile
import asyncio

class LandmarkRecognitionService:
    """
    This service simulates a local AI model that takes an image
    and returns a landmark name. For now it's just a dummy.
    """

    def __init__(self):
        # later we'll load the real model here
        pass

    async def recognize(self, image: UploadFile) -> str:
        # Read the file (we don't use it yet, but this mimics real behavior)
        image_bytes = await image.read()

        # Simulate heavy work in a thread (like real model inference)
        # For now, it just returns a fixed value
        def _dummy_model():
            # Here we'll call the real local model later
            return "ithraa"

        landmark_name = await asyncio.to_thread(_dummy_model)
        return landmark_name