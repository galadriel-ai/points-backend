import asyncio
from typing import Optional

import settings
from points import api_logger
from points.repository import utils as db_utils
import aiohttp
from google.cloud import storage

from points.domain.dashboard.entities import UserProfileImage
from points.repository.user_repository import UserRepositoryPsql

logger = api_logger.get()

STORAGE_CLIENT = storage.Client.from_service_account_json(
    settings.GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_PATH)
BUCKET = STORAGE_CLIENT.bucket(settings.GOOGLE_BUCKET_NAME)

SLEEP_TIME = 1


async def execute(
    user_repository: UserRepositoryPsql,
) -> None:
    users = user_repository.get_users_without_cached_images()
    for user in users:
        await _handle_user_image_download(user, user_repository)
        await asyncio.sleep(SLEEP_TIME)


async def _handle_user_image_download(
    user: UserProfileImage,
    user_repository: UserRepositoryPsql,
) -> None:
    url = await _handle_image_upload(user.profile_image_url)
    if url:
        user_repository.save_cached_profile_image_url(user.user_id, url)
        logger.debug(f"Saved image for user={user.user_id}, url={url}")


async def _handle_image_upload(url: str) -> Optional[str]:
    try:
        async with aiohttp.ClientSession() as session:
            res = await session.get(url)
            content = await res.content.read()

        filename = f"{db_utils.generate_uuid()}.jpg"
        blob = BUCKET.blob(filename)
        blob.upload_from_string(content, content_type=res.headers["Content-Type"])
        return f"https://storage.googleapis.com/{settings.GOOGLE_BUCKET_NAME}/{filename}"
    except Exception as e:
        logger.error("Failed to upload profile image", exc_info=True)
        return None
