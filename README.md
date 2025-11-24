# Password Checker API

A small production-ready password strength checker and API built with FastAPI.

Features
- Entropy-based scoring
- Common pattern detection
- Repetition/sequence detection
- Configurable policy
- CLI and HTTP API with simple hardening (rate-limit, request-size limit, optional API key)

Quick start (local)

1. Create and activate a virtualenv, install deps:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the CLI (interactive):

```bash
python3 cli.py
```

3. Run the API (dev):

```bash
# Run with uvicorn (do NOT run `python app.py`)
uvicorn app:app --reload
```

Important: Python version
------------------------

FastAPI and Pydantic have compatibility requirements. If you see import errors involving
`pydantic` or `ForwardRef._evaluate()` (example below), it's usually because your virtualenv
is using Python 3.13 where the installed package versions are incompatible.

Typical error message:

```
TypeError: ForwardRef._evaluate() missing 1 required keyword-only argument: 'recursive_guard'
```

Resolution options (pick one):

- Preferred: Use Python 3.11 (matches the provided `Dockerfile` and CI).

  On Debian/Ubuntu (example):

  ```bash
  # install python3.11 if not available
  sudo apt-get update && sudo apt-get install -y python3.11 python3.11-venv

  # remove old virtualenv if you created one with a different python
  rm -rf .venv

  # create venv using python3.11
  python3.11 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

- Alternative: use `pyenv` to install and select Python 3.11, then create the venv.

  ```bash
  # install pyenv (see https://github.com/pyenv/pyenv for install instructions)
  pyenv install 3.11.4
  pyenv local 3.11.4
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

- Or: use the included Dockerfile (recommended for parity). Docker runs Python 3.11 in the container so you won't hit this issue.

  ```bash
  docker build -t password-checker:latest .
  docker run -p 8000:8000 password-checker:latest
  ```

Don't run `python app.py`
------------------------

The FastAPI app should be launched with an ASGI server such as `uvicorn` (as shown above). Running
`python app.py` will import FastAPI and its dependencies directly — if your environment uses an
incompatible Python/runtime, you'll encounter import-time errors. Use `uvicorn app:app` or Docker instead.

API usage

- POST `/check` with JSON body `{ "password": "..." }` returns a JSON report.
- Example:

```bash
curl -X POST "http://127.0.0.1:8000/check" \
  -H "Content-Type: application/json" \
  -d '{"password":"MyPass123!"}'
```

Environment variables (optional)

- `PASSWORD_API_KEY` — if set, clients must provide header `x-api-key: <value>` for `/check`.
- `RATE_LIMIT_CALLS` — number of calls per `RATE_LIMIT_WINDOW` allowed (default 30).
- `RATE_LIMIT_WINDOW` — sliding window in seconds for rate limiting (default 60).
- `MAX_REQUEST_SIZE` — maximum request payload size in bytes (default 4096).
- `PORT` — port to bind the server (default 8000).

Docker

Build and run with the included `Dockerfile` (uses Python 3.11):

```bash
# build
docker build -t password-checker:latest .

# run (example)
docker run -p 8000:8000 \
  -e PASSWORD_API_KEY=changeme \
  -e RATE_LIMIT_CALLS=30 \
  -e RATE_LIMIT_WINDOW=60 \
  password-checker:latest
```

Continuous integration

A minimal GitHub Actions workflow is included at `.github/workflows/ci.yml` to run `pytest` on push and pull requests (Python 3.11).

Deploying to Render

1. Push to GitHub.
2. Create a Web Service on Render and connect the repo.
3. Render will run `pip install -r requirements.txt` and use the `Procfile` start command `web: uvicorn app:app --host 0.0.0.0 --port $PORT`.

Security notes

- Do not store plain-text passwords. This service is for checking strength only.
- If deploying publicly, set `PASSWORD_API_KEY` and enable HTTPS, add persistent rate-limiting (Redis), and monitor logs.

License / Disclaimer

This project is intended for educational and internal use. Use responsibly.
