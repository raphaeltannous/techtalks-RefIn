import uuid
from io import BytesIO

from config import settings
from exceptions import (
    InvalidImageError,
)
from PIL import Image, ImageOps


def delete_profile_picture(filename: str | None):
    if filename is None:
        return

    file_path = settings.USER_PROFILE_PICTURES_DIRECTORY.joinpath(filename).absolute()

    if file_path.exists():
        file_path.unlink()


def process_profile_picture(image_bytes: bytes) -> str:
    try:
        original = Image.open(BytesIO(image_bytes))
    except Exception:
        raise InvalidImageError()

    original = ImageOps.exif_transpose(original)

    # Resize and crop to 300x300
    image = original.copy()
    image.thumbnail((300, 300), Image.Resampling.LANCZOS)
    image = ImageOps.fit(
        image,
        (300, 300),
        Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )

    if image.mode != "RGB":
        image = image.convert("RGB")

    filename = f"{uuid.uuid4()}.jpg"
    filepath = settings.USER_PROFILE_PICTURES_DIRECTORY.joinpath(filename).absolute()

    image.save(
        filepath,
        "JPEG",
        quality=85,
        optimize=True,
    )

    return filename


def delete_banner(filename: str | None):
    if filename is None:
        return

    file_path = settings.USER_PROFILE_BANNERS_DIRECTORY.joinpath(filename).absolute()

    if file_path.exists():
        file_path.unlink()


def process_banner(image_bytes: bytes) -> str:
    try:
        original = Image.open(BytesIO(image_bytes))
    except Exception:
        raise InvalidImageError()

    original = ImageOps.exif_transpose(original)

    # Resize and crop to 700x300
    image = original.copy()
    image.thumbnail((700, 300), Image.Resampling.LANCZOS)
    image = ImageOps.fit(
        image,
        (700, 300),
        Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )

    if image.mode != "RGB":
        image = image.convert("RGB")

    filename = f"{uuid.uuid4()}.jpg"
    filepath = settings.USER_PROFILE_BANNERS_DIRECTORY.joinpath(
        filename,
    ).absolute()

    image.save(
        filepath,
        "JPEG",
        quality=85,
        optimize=True,
    )

    return filename
