from fastapi import FastAPI, HTTPException

from src import calculator
from src.models import (
    CalculateRequest,
    CalculateResponse,
    ConvertRequest,
    ConvertResponse,
)
from src.services.exchange_rate import ExchangeRateError, ExchangeRateService

app = FastAPI(title="Calculator API", version="0.1.0")

# One shared instance is fine here - httpx.AsyncClient is created per-request
# inside the service anyway. In a bigger app you'd wire this via Depends().
exchange_rate_service = ExchangeRateService()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/calculate", response_model=CalculateResponse)
async def calculate(payload: CalculateRequest) -> CalculateResponse:
    func = calculator.OPERATIONS[payload.operation]
    try:
        result = func(payload.a, payload.b)
    except ZeroDivisionError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except TypeError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return CalculateResponse(
        operation=payload.operation, a=payload.a, b=payload.b, result=result
    )


@app.post("/convert", response_model=ConvertResponse)
async def convert(payload: ConvertRequest) -> ConvertResponse:
    try:
        rate = await exchange_rate_service.get_rate(
            payload.from_currency, payload.to_currency
        )
        converted = calculator.multiply(payload.amount, rate)
    except ExchangeRateError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return ConvertResponse(
        amount=payload.amount,
        from_currency=payload.from_currency.upper(),
        to_currency=payload.to_currency.upper(),
        rate=rate,
        converted_amount=converted,
    )
