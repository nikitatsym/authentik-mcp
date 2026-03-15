from ..registry import _op
from .groups import authentik_read
from .helpers import _get_client, _paginated

# ── Providers — All ──────────────────────────────────────────────────


@_op(authentik_read)
def list_providers(limit: int = 20):
    """List all providers."""
    return _paginated("/providers/all/", limit=limit)


@_op(authentik_read)
def show_provider(id: int):
    """Get full provider details."""
    return _get_client().get(f"/providers/all/{id}/")


@_op(authentik_read)
def list_provider_types():
    """List provider types."""
    return _get_client().get("/providers/all/types/")


# ── Providers — OAuth2 ───────────────────────────────────────────────


@_op(authentik_read)
def list_oauth2_providers(limit: int = 20):
    """List OAuth2 providers."""
    return _paginated("/providers/oauth2/", limit=limit)


@_op(authentik_read)
def show_oauth2_provider(id: int):
    """Get OAuth2 provider details."""
    return _get_client().get(f"/providers/oauth2/{id}/")


@_op(authentik_read)
def get_oauth2_setup_urls(id: int):
    """Get OAuth2 provider setup URLs."""
    return _get_client().get(f"/providers/oauth2/{id}/setup_urls/")


@_op(authentik_read)
def preview_oauth2_user(id: int):
    """Preview OAuth2 user data for a provider."""
    return _get_client().get(f"/providers/oauth2/{id}/preview_user/")


# ── Providers — LDAP ─────────────────────────────────────────────────


@_op(authentik_read)
def list_ldap_providers(limit: int = 20):
    """List LDAP providers."""
    return _paginated("/providers/ldap/", limit=limit)


@_op(authentik_read)
def show_ldap_provider(id: int):
    """Get LDAP provider details."""
    return _get_client().get(f"/providers/ldap/{id}/")


# ── Providers — SAML ─────────────────────────────────────────────────


@_op(authentik_read)
def list_saml_providers(limit: int = 20):
    """List SAML providers."""
    return _paginated("/providers/saml/", limit=limit)


@_op(authentik_read)
def show_saml_provider(id: int):
    """Get SAML provider details."""
    return _get_client().get(f"/providers/saml/{id}/")


@_op(authentik_read)
def get_saml_metadata(id: int):
    """Get SAML provider metadata."""
    return _get_client().get(f"/providers/saml/{id}/metadata/")


@_op(authentik_read)
def preview_saml_user(id: int):
    """Preview SAML user data for a provider."""
    return _get_client().get(f"/providers/saml/{id}/preview_user/")


# ── Providers — Proxy ────────────────────────────────────────────────


@_op(authentik_read)
def list_proxy_providers(limit: int = 20):
    """List proxy providers."""
    return _paginated("/providers/proxy/", limit=limit)


@_op(authentik_read)
def show_proxy_provider(id: int):
    """Get proxy provider details."""
    return _get_client().get(f"/providers/proxy/{id}/")


# ── Providers — SCIM ─────────────────────────────────────────────────


@_op(authentik_read)
def list_scim_providers(limit: int = 20):
    """List SCIM providers."""
    return _paginated("/providers/scim/", limit=limit)


@_op(authentik_read)
def show_scim_provider(id: int):
    """Get SCIM provider details."""
    return _get_client().get(f"/providers/scim/{id}/")


@_op(authentik_read)
def get_scim_sync_status(id: int):
    """Get SCIM provider sync status."""
    return _get_client().get(f"/providers/scim/{id}/sync_status/")


@_op(authentik_read)
def list_scim_users(provider: int):
    """List SCIM provider users."""
    return _get_client().get(f"/providers/scim/{provider}/users/")


@_op(authentik_read)
def list_scim_groups(provider: int):
    """List SCIM provider groups."""
    return _get_client().get(f"/providers/scim/{provider}/groups/")


# ── Providers — Radius ───────────────────────────────────────────────


@_op(authentik_read)
def list_radius_providers(limit: int = 20):
    """List Radius providers."""
    return _paginated("/providers/radius/", limit=limit)


@_op(authentik_read)
def show_radius_provider(id: int):
    """Get Radius provider details."""
    return _get_client().get(f"/providers/radius/{id}/")


# ── Providers — RAC ──────────────────────────────────────────────────


@_op(authentik_read)
def list_rac_providers(limit: int = 20):
    """List RAC providers."""
    return _paginated("/providers/rac/", limit=limit)


@_op(authentik_read)
def show_rac_provider(id: int):
    """Get RAC provider details."""
    return _get_client().get(f"/providers/rac/{id}/")


# ── Providers — Google Workspace ─────────────────────────────────────


@_op(authentik_read)
def list_google_workspace_providers(limit: int = 20):
    """List Google Workspace providers."""
    return _paginated("/providers/google_workspace/", limit=limit)


@_op(authentik_read)
def show_google_workspace_provider(id: int):
    """Get Google Workspace provider details."""
    return _get_client().get(f"/providers/google_workspace/{id}/")


@_op(authentik_read)
def get_google_workspace_sync_status(id: int):
    """Get Google Workspace provider sync status."""
    return _get_client().get(f"/providers/google_workspace/{id}/sync_status/")


# ── Providers — Microsoft Entra ──────────────────────────────────────


@_op(authentik_read)
def list_microsoft_entra_providers(limit: int = 20):
    """List Microsoft Entra providers."""
    return _paginated("/providers/microsoft_entra/", limit=limit)


@_op(authentik_read)
def show_microsoft_entra_provider(id: int):
    """Get Microsoft Entra provider details."""
    return _get_client().get(f"/providers/microsoft_entra/{id}/")


@_op(authentik_read)
def get_microsoft_entra_sync_status(id: int):
    """Get Microsoft Entra provider sync status."""
    return _get_client().get(f"/providers/microsoft_entra/{id}/sync_status/")


# ── Providers — WS-Fed ───────────────────────────────────────────────


@_op(authentik_read)
def list_wsfed_providers(limit: int = 20):
    """List WS-Fed providers."""
    return _paginated("/providers/wsfed/", limit=limit)


@_op(authentik_read)
def show_wsfed_provider(id: int):
    """Get WS-Fed provider details."""
    return _get_client().get(f"/providers/wsfed/{id}/")


@_op(authentik_read)
def get_wsfed_metadata(id: int):
    """Get WS-Fed provider metadata."""
    return _get_client().get(f"/providers/wsfed/{id}/metadata/")


# ── Providers — SSF ──────────────────────────────────────────────────


@_op(authentik_read)
def list_ssf_providers(limit: int = 20):
    """List SSF providers."""
    return _paginated("/providers/ssf/", limit=limit)


@_op(authentik_read)
def show_ssf_provider(id: int):
    """Get SSF provider details."""
    return _get_client().get(f"/providers/ssf/{id}/")
