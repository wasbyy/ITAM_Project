from fastapi import File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from io import BytesIO

from db.models import Event
from db.session import get_db


async def upload_image(file: UploadFile = File(...)):
    # Проверяем тип файла
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")
    # Читаем данные файла
    file_data = await file.read()
    return file_data

async def download_image(event_id: int, db: Session = Depends(get_db)):
    # Получаем изображение из базы данных
    image = db.query(Event).filter(Event.event_id == event_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    # Преобразуем бинарные данные в поток
    image_stream = BytesIO(image.data)
    return StreamingResponse(image_stream, media_type="image/jpeg")