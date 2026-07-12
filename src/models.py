from typing import Literal

from pydantic import BaseModel, Field


class CalculateRequest(BaseModel):
    operation: Literal["add", "subtract", "multiply", "divide"]
    a: float
    b: float


class CalculateResponse(BaseModel):
    operation: str
    a: float
    b: float
    result: float


class ConvertRequest(BaseModel):
    amount: float = Field(gt=0)
    from_currency: str = Field(min_length=3, max_length=3)
    to_currency: str = Field(min_length=3, max_length=3)


class ConvertResponse(BaseModel):
    amount: float
    from_currency: str
    to_currency: str
    rate: float
    converted_amount: float
