import time
import uvicorn
from sqlalchemy import delete
from sqlalchemy.future import select
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import  AsyncSession
from http import HTTPStatus
import models
import schemas
from database import engine,  get_async_session

from helper import check_and_create_short_link

app = FastAPI()


@app.on_event("startup")
async def shutdown():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown(session: AsyncSession = Depends(get_async_session)):
    await session.close()
    await engine.dispose()


@app.post('/url/', response_model=str)
async def create_url(long_url: schemas.LongUrlIn, session=Depends(get_async_session)) -> models.BaseUrl:
    async with session.begin():
        new_url = await check_and_create_short_link(long_url, session)
    return new_url.short_url


@app.post('/longurl/', response_model=str)
async def find_short_url(url: schemas.ShortUrlIn, session=Depends(get_async_session)):
    async with session.begin():
        res = await session.execute(select(models.BaseUrl).where(models.BaseUrl.short_url == url.short_url))
    if result := res.scalars().first():
        return result.long_url
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_ACCEPTABLE,
            detail=f"no such url",
        )


@app.post('/deletelongurl/', response_model=bool)
async def delete_short_url(url: schemas.ShortUrlIn, session=Depends(get_async_session)):
    async with session.begin():
        res = await session.execute(models.BaseUrl.__table__.delete().where(models.BaseUrl.short_url == url.short_url))
        is_deleted = res.rowcount > 0
        if is_deleted:
            await session.commit()

        return is_deleted


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")





