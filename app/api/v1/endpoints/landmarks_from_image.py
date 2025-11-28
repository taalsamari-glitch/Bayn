from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import StreamingResponse
from app.services.landmark_recognition import LandmarkRecognitionService
from app.services.landmark_description_service import get_landmark_description
from app.services.azure_tts import AzureTTSService

router = APIRouter()
@router.post("/describe-from-image", response_class=StreamingResponse)
async def describe_from_image(
    image: UploadFile = File(...),
    recognizer: LandmarkRecognitionService = Depends(LandmarkRecognitionService),
    tts_service: AzureTTSService = Depends(AzureTTSService),
):
    landmark_name = await recognizer.recognize(image)

    description = get_landmark_description(landmark_name)
    print(">>> Landmark name:", landmark_name)
    print(">>> Description length:", len(description))
    # optionally: print(">>> Description:", description)

    audio_bytes = tts_service.text_to_speech(description)
    print(">>> Audio bytes length:", len(audio_bytes))

    return StreamingResponse(
        iter([audio_bytes]),
        media_type="audio/wav",
        headers={"Content-Disposition": f'inline; filename="{landmark_name}.wav"'},
    )

