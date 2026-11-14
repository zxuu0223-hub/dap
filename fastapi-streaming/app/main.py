import asyncio
import json
from collections.abc import AsyncIterator

from fastapi import FastAPI, Query, Request
from fastapi.responses import StreamingResponse

app = FastAPI(title="Streaming API Demo", version="1.0.0")


async def event_stream(request: Request, message: str, count: int, delay_ms: int) -> AsyncIterator[str]:
    for index in range(1, count + 1):
        if await request.is_disconnected():
            break
        payload = {"index": index, "message": message, "done": index == count}
        yield f"id: {index}\nevent: chunk\ndata: {json.dumps(payload, ensure_ascii=False)}\n\n"
        await asyncio.sleep(delay_ms / 1000)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/stream", response_class=StreamingResponse)
async def stream(
    request: Request,
    message: str = Query("Hello from FastAPI", min_length=1, max_length=200),
    count: int = Query(5, ge=1, le=100),
    delay_ms: int = Query(300, ge=0, le=5000),
) -> StreamingResponse:
    return StreamingResponse(
        event_stream(request, message, count, delay_ms),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
