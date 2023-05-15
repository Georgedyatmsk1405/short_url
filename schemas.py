from pydantic import BaseModel, validator, Field 
import validators


class LongUrlIn(BaseModel):
    long_url: str

    @validator("long_url", check_fields=False)
    def validate_url(cls, v):
        if not validators.url(v):
            raise ValueError("Long URL is invalid.")
        return v


class ShortUrlIn(BaseModel):
    short_url: str
