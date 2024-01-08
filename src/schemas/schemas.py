from pydantic import BaseModel, Field


class LocationSchema(BaseModel):
    city: str = Field()
    regionName: str = Field()
    country: str = Field()


class WeatherSchema(BaseModel):
    temperature: str = Field()
    humidity: str = Field()
    description: str = Field()
