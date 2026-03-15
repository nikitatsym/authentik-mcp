import httpx

from .config import get_settings


class APIError(Exception):
    def __init__(self, status: int, method: str, path: str, body):
        self.status = status
        self.method = method
        self.path = path
        self.body = body
        super().__init__(f"{method} {path} -> {status}: {body}")


class AuthentikClient:
    def __init__(
        self,
        base_url: str | None = None,
        token: str | None = None,
    ):
        s = get_settings()
        self._root = (base_url or s.authentik_url).rstrip("/")
        self._http = httpx.Client(
            base_url=self._root + "/api/v3/",
            headers={"Authorization": f"Bearer {token or s.authentik_token}"},
            timeout=30.0,
        )

    def _handle(self, r: httpx.Response):
        if r.status_code >= 400:
            try:
                body = r.json()
            except Exception:
                body = r.text
            raise APIError(r.status_code, r.request.method, str(r.url), body)
        if r.status_code == 204 or not r.content:
            return None
        return r.json()

    def get(self, path: str, **kwargs):
        return self._handle(self._http.get(path, **kwargs))

    def post(self, path: str, **kwargs):
        return self._handle(self._http.post(path, **kwargs))

    def put(self, path: str, **kwargs):
        return self._handle(self._http.put(path, **kwargs))

    def patch(self, path: str, **kwargs):
        return self._handle(self._http.patch(path, **kwargs))

    def delete(self, path: str, **kwargs):
        return self._handle(self._http.delete(path, **kwargs))

    def health(self):
        """Check service health (/-/health/live/, outside /api/v3/)."""
        r = httpx.get(
            self._root + "/-/health/live/",
            headers=self._http.headers,
            timeout=10.0,
        )
        if r.status_code == 200:
            return {"status": "ok"}
        return {"status": "error", "code": r.status_code}
