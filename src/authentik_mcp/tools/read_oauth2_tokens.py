from ..registry import _op
from .groups import authentik_read
from .helpers import SLIM_OAUTH2_TOKEN, _get_client, _paginated


@_op(authentik_read)
def list_oauth2_access_tokens(limit: int = 20):
    """List OAuth2 access tokens."""
    return _paginated("/oauth2/access_tokens/", limit=limit, slim_fields=SLIM_OAUTH2_TOKEN)


@_op(authentik_read)
def show_oauth2_access_token(id: int):
    """Get OAuth2 access token details."""
    return _get_client().get(f"/oauth2/access_tokens/{id}/")


@_op(authentik_read)
def list_oauth2_authorization_codes(limit: int = 20):
    """List OAuth2 authorization codes."""
    return _paginated("/oauth2/authorization_codes/", limit=limit, slim_fields=SLIM_OAUTH2_TOKEN)


@_op(authentik_read)
def show_oauth2_authorization_code(id: int):
    """Get OAuth2 authorization code details."""
    return _get_client().get(f"/oauth2/authorization_codes/{id}/")


@_op(authentik_read)
def list_oauth2_refresh_tokens(limit: int = 20):
    """List OAuth2 refresh tokens."""
    return _paginated("/oauth2/refresh_tokens/", limit=limit, slim_fields=SLIM_OAUTH2_TOKEN)


@_op(authentik_read)
def show_oauth2_refresh_token(id: int):
    """Get OAuth2 refresh token details."""
    return _get_client().get(f"/oauth2/refresh_tokens/{id}/")
