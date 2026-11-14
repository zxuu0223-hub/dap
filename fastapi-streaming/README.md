# FastAPI streaming demo

An SSE endpoint that streams JSON events, stops when the client disconnects, disables proxy buffering, and validates all query parameters.

```bash
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Try it:

```bash
curl -N "http://127.0.0.1:8000/stream?message=hello&count=5&delay_ms=300"
```

Run tests with `pytest -q`.
