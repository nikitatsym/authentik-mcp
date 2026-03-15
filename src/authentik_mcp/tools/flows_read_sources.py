from ..registry import _op
from .groups import authentik_flows_read
from .helpers import _get_client, _paginated

# ── Sources — All ────────────────────────────────────────────────────


@_op(authentik_flows_read)
def list_sources(limit: int = 20):
    """List all sources."""
    return _paginated("/sources/all/", limit=limit)


@_op(authentik_flows_read)
def show_source(slug: str):
    """Get source details."""
    return _get_client().get(f"/sources/all/{slug}/")


@_op(authentik_flows_read)
def list_source_types():
    """List source types."""
    return _get_client().get("/sources/all/types/")


# ── Sources — LDAP ───────────────────────────────────────────────────


@_op(authentik_flows_read)
def list_ldap_sources(limit: int = 20):
    """List LDAP sources."""
    return _paginated("/sources/ldap/", limit=limit)


@_op(authentik_flows_read)
def show_ldap_source(slug: str):
    """Get LDAP source details."""
    return _get_client().get(f"/sources/ldap/{slug}/")


@_op(authentik_flows_read)
def get_ldap_sync_status(slug: str):
    """Get LDAP source sync status."""
    return _get_client().get(f"/sources/ldap/{slug}/sync_status/")


# ── Sources — OAuth ──────────────────────────────────────────────────


@_op(authentik_flows_read)
def list_oauth_sources(limit: int = 20):
    """List OAuth sources."""
    return _paginated("/sources/oauth/", limit=limit)


@_op(authentik_flows_read)
def show_oauth_source(slug: str):
    """Get OAuth source details."""
    return _get_client().get(f"/sources/oauth/{slug}/")


@_op(authentik_flows_read)
def list_oauth_source_types():
    """List OAuth source types."""
    return _get_client().get("/sources/oauth/source_types/")


# ── Sources — SAML ───────────────────────────────────────────────────


@_op(authentik_flows_read)
def list_saml_sources(limit: int = 20):
    """List SAML sources."""
    return _paginated("/sources/saml/", limit=limit)


@_op(authentik_flows_read)
def show_saml_source(slug: str):
    """Get SAML source details."""
    return _get_client().get(f"/sources/saml/{slug}/")


@_op(authentik_flows_read)
def get_saml_source_metadata(slug: str):
    """Get SAML source metadata."""
    return _get_client().get(f"/sources/saml/{slug}/metadata/")


# ── Sources — SCIM ───────────────────────────────────────────────────


@_op(authentik_flows_read)
def list_scim_sources(limit: int = 20):
    """List SCIM sources."""
    return _paginated("/sources/scim/", limit=limit)


@_op(authentik_flows_read)
def show_scim_source(slug: str):
    """Get SCIM source details."""
    return _get_client().get(f"/sources/scim/{slug}/")


@_op(authentik_flows_read)
def get_scim_source_sync_status(slug: str):
    """Get SCIM source sync status."""
    return _get_client().get(f"/sources/scim/{slug}/sync_status/")


# ── Sources — Plex ───────────────────────────────────────────────────


@_op(authentik_flows_read)
def list_plex_sources(limit: int = 20):
    """List Plex sources."""
    return _paginated("/sources/plex/", limit=limit)


@_op(authentik_flows_read)
def show_plex_source(slug: str):
    """Get Plex source details."""
    return _get_client().get(f"/sources/plex/{slug}/")


# ── Sources — Kerberos ───────────────────────────────────────────────


@_op(authentik_flows_read)
def list_kerberos_sources(limit: int = 20):
    """List Kerberos sources."""
    return _paginated("/sources/kerberos/", limit=limit)


@_op(authentik_flows_read)
def show_kerberos_source(slug: str):
    """Get Kerberos source details."""
    return _get_client().get(f"/sources/kerberos/{slug}/")


@_op(authentik_flows_read)
def get_kerberos_sync_status(slug: str):
    """Get Kerberos source sync status."""
    return _get_client().get(f"/sources/kerberos/{slug}/sync_status/")


# ── Sources — Telegram ───────────────────────────────────────────────


@_op(authentik_flows_read)
def list_telegram_sources(limit: int = 20):
    """List Telegram sources."""
    return _paginated("/sources/telegram/", limit=limit)


@_op(authentik_flows_read)
def show_telegram_source(slug: str):
    """Get Telegram source details."""
    return _get_client().get(f"/sources/telegram/{slug}/")


# ── Sources — Connections ────────────────────────────────────────────


@_op(authentik_flows_read)
def list_user_connections(limit: int = 20):
    """List user source connections."""
    return _paginated("/sources/user_connections/all/", limit=limit)


@_op(authentik_flows_read)
def show_user_connection(id: int):
    """Get user source connection details."""
    return _get_client().get(f"/sources/user_connections/all/{id}/")


@_op(authentik_flows_read)
def list_group_connections(limit: int = 20):
    """List group source connections."""
    return _paginated("/sources/group_connections/all/", limit=limit)


@_op(authentik_flows_read)
def show_group_connection(id: int):
    """Get group source connection details."""
    return _get_client().get(f"/sources/group_connections/all/{id}/")
