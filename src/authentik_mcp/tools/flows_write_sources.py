from ..registry import _op
from .groups import authentik_flows_write
from .helpers import _get_client, _ok

# ── Sources — LDAP ───────────────────────────────────────────────────


@_op(authentik_flows_write)
def create_ldap_source(name: str, **kwargs):
    """Create an LDAP source. Required: name."""
    return _ok(_get_client().post("/sources/ldap/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_ldap_source(slug: str, **kwargs):
    """Update an LDAP source."""
    return _ok(_get_client().patch(f"/sources/ldap/{slug}/", json=kwargs))


# ── Sources — OAuth ──────────────────────────────────────────────────


@_op(authentik_flows_write)
def create_oauth_source(name: str, **kwargs):
    """Create an OAuth source. Required: name."""
    return _ok(_get_client().post("/sources/oauth/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_oauth_source(slug: str, **kwargs):
    """Update an OAuth source."""
    return _ok(_get_client().patch(f"/sources/oauth/{slug}/", json=kwargs))


# ── Sources — SAML ───────────────────────────────────────────────────


@_op(authentik_flows_write)
def create_saml_source(name: str, **kwargs):
    """Create a SAML source. Required: name."""
    return _ok(_get_client().post("/sources/saml/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_saml_source(slug: str, **kwargs):
    """Update a SAML source."""
    return _ok(_get_client().patch(f"/sources/saml/{slug}/", json=kwargs))


# ── Sources — SCIM ───────────────────────────────────────────────────


@_op(authentik_flows_write)
def create_scim_source(name: str, **kwargs):
    """Create a SCIM source. Required: name."""
    return _ok(_get_client().post("/sources/scim/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_scim_source(slug: str, **kwargs):
    """Update a SCIM source."""
    return _ok(_get_client().patch(f"/sources/scim/{slug}/", json=kwargs))


# ── Sources — Plex ───────────────────────────────────────────────────


@_op(authentik_flows_write)
def create_plex_source(name: str, **kwargs):
    """Create a Plex source. Required: name."""
    return _ok(_get_client().post("/sources/plex/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_plex_source(slug: str, **kwargs):
    """Update a Plex source."""
    return _ok(_get_client().patch(f"/sources/plex/{slug}/", json=kwargs))


@_op(authentik_flows_write)
def redeem_plex_token(slug: str):
    """Redeem a Plex token."""
    return _ok(_get_client().post(f"/sources/plex/{slug}/redeem_token/"))


@_op(authentik_flows_write)
def redeem_plex_token_authenticated(slug: str):
    """Redeem a Plex token (authenticated)."""
    return _ok(_get_client().post(f"/sources/plex/{slug}/redeem_token_authenticated/"))


# ── Sources — Kerberos ───────────────────────────────────────────────


@_op(authentik_flows_write)
def create_kerberos_source(name: str, **kwargs):
    """Create a Kerberos source. Required: name."""
    return _ok(_get_client().post("/sources/kerberos/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_kerberos_source(slug: str, **kwargs):
    """Update a Kerberos source."""
    return _ok(_get_client().patch(f"/sources/kerberos/{slug}/", json=kwargs))


# ── Sources — Telegram ───────────────────────────────────────────────


@_op(authentik_flows_write)
def create_telegram_source(name: str, **kwargs):
    """Create a Telegram source. Required: name."""
    return _ok(_get_client().post("/sources/telegram/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_telegram_source(slug: str, **kwargs):
    """Update a Telegram source."""
    return _ok(_get_client().patch(f"/sources/telegram/{slug}/", json=kwargs))


@_op(authentik_flows_write)
def connect_telegram_user(slug: str):
    """Connect a Telegram user."""
    return _ok(_get_client().post(f"/sources/telegram/{slug}/connect_user/"))


# ── Sources — Connections ────────────────────────────────────────────


@_op(authentik_flows_write)
def update_user_connection(id: int, **kwargs):
    """Update a user source connection."""
    return _ok(_get_client().patch(f"/sources/user_connections/all/{id}/", json=kwargs))


@_op(authentik_flows_write)
def update_group_connection(id: int, **kwargs):
    """Update a group source connection."""
    return _ok(_get_client().patch(f"/sources/group_connections/all/{id}/", json=kwargs))
