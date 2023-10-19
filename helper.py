from sqlalchemy.future import select
from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession
import schemas
import models
import shortuuid
from constance import BASE_URL


async def check_and_create_short_link(
    long_url: schemas.LongUrlIn, session: AsyncSession
):

    if await get_obj_by_short_link(long_url.long_url, session):
        raise HTTPException(
            status_code=HTTPStatus.NOT_ACCEPTABLE,
            detail=f"url {long_url.long_url} is busy",
        )
    shortcode = shortuuid.ShortUUID().random(length=8)
    short_url = f"{BASE_URL}/{shortcode}"
    new_url = models.BaseUrl(short_url=short_url, **long_url.dict())
    session.add(new_url)
    await session.commit()
    return new_url


async def get_obj_by_short_link(long_url: str, session: AsyncSession) -> models.BaseUrl:
    urls = await session.execute(
        select(models.BaseUrl).where(models.BaseUrl.long_url == long_url)
    )
    url = urls.scalars().first()
    if url:
        return url
print("test")
print("test2")
