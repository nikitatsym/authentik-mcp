from ..registry import _op
from .groups import authentik_write
from .helpers import _get_client, _ok

# ── Providers — OAuth2 ───────────────────────────────────────────────


@_op(authentik_write)
def create_oauth2_provider(name: str, **kwargs):
    """Create an OAuth2 provider. Required: name."""
    return _ok(_get_client().post("/providers/oauth2/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_oauth2_provider(id: int, **kwargs):
    """Update an OAuth2 provider."""
    return _ok(_get_client().patch(f"/providers/oauth2/{id}/", json=kwargs))


# ── Providers — LDAP ─────────────────────────────────────────────────


@_op(authentik_write)
def create_ldap_provider(name: str, **kwargs):
    """Create an LDAP provider. Required: name."""
    return _ok(_get_client().post("/providers/ldap/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_ldap_provider(id: int, **kwargs):
    """Update an LDAP provider."""
    return _ok(_get_client().patch(f"/providers/ldap/{id}/", json=kwargs))


# ── Providers — SAML ─────────────────────────────────────────────────


@_op(authentik_write)
def create_saml_provider(name: str, **kwargs):
    """Create a SAML provider. Required: name."""
    return _ok(_get_client().post("/providers/saml/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_saml_provider(id: int, **kwargs):
    """Update a SAML provider."""
    return _ok(_get_client().patch(f"/providers/saml/{id}/", json=kwargs))


@_op(authentik_write)
def import_saml_metadata(**kwargs):
    """Import SAML metadata."""
    return _ok(_get_client().post("/providers/saml/import_metadata/", json=kwargs))


# ── Providers — Proxy ────────────────────────────────────────────────


@_op(authentik_write)
def create_proxy_provider(name: str, **kwargs):
    """Create a proxy provider. Required: name."""
    return _ok(_get_client().post("/providers/proxy/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_proxy_provider(id: int, **kwargs):
    """Update a proxy provider."""
    return _ok(_get_client().patch(f"/providers/proxy/{id}/", json=kwargs))


# ── Providers — SCIM ─────────────────────────────────────────────────


@_op(authentik_write)
def create_scim_provider(name: str, **kwargs):
    """Create a SCIM provider. Required: name."""
    return _ok(_get_client().post("/providers/scim/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_scim_provider(id: int, **kwargs):
    """Update a SCIM provider."""
    return _ok(_get_client().patch(f"/providers/scim/{id}/", json=kwargs))


@_op(authentik_write)
def sync_scim_object(id: int, **kwargs):
    """Trigger SCIM object sync."""
    return _ok(_get_client().post(f"/providers/scim/{id}/sync_object/", json=kwargs))


# ── Providers — Radius ───────────────────────────────────────────────


@_op(authentik_write)
def create_radius_provider(name: str, **kwargs):
    """Create a Radius provider. Required: name."""
    return _ok(_get_client().post("/providers/radius/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_radius_provider(id: int, **kwargs):
    """Update a Radius provider."""
    return _ok(_get_client().patch(f"/providers/radius/{id}/", json=kwargs))


# ── Providers — RAC ──────────────────────────────────────────────────


@_op(authentik_write)
def create_rac_provider(name: str, **kwargs):
    """Create a RAC provider. Required: name."""
    return _ok(_get_client().post("/providers/rac/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_rac_provider(id: int, **kwargs):
    """Update a RAC provider."""
    return _ok(_get_client().patch(f"/providers/rac/{id}/", json=kwargs))


# ── Providers — Google Workspace ─────────────────────────────────────


@_op(authentik_write)
def create_google_workspace_provider(name: str, **kwargs):
    """Create a Google Workspace provider. Required: name."""
    return _ok(_get_client().post("/providers/google_workspace/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_google_workspace_provider(id: int, **kwargs):
    """Update a Google Workspace provider."""
    return _ok(_get_client().patch(f"/providers/google_workspace/{id}/", json=kwargs))


@_op(authentik_write)
def sync_google_workspace_object(id: int, **kwargs):
    """Trigger Google Workspace object sync."""
    return _ok(_get_client().post(f"/providers/google_workspace/{id}/sync_object/", json=kwargs))


# ── Providers — Microsoft Entra ──────────────────────────────────────


@_op(authentik_write)
def create_microsoft_entra_provider(name: str, **kwargs):
    """Create a Microsoft Entra provider. Required: name."""
    return _ok(_get_client().post("/providers/microsoft_entra/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_microsoft_entra_provider(id: int, **kwargs):
    """Update a Microsoft Entra provider."""
    return _ok(_get_client().patch(f"/providers/microsoft_entra/{id}/", json=kwargs))


@_op(authentik_write)
def sync_microsoft_entra_object(id: int, **kwargs):
    """Trigger Microsoft Entra object sync."""
    return _ok(_get_client().post(f"/providers/microsoft_entra/{id}/sync_object/", json=kwargs))


# ── Providers — WS-Fed ───────────────────────────────────────────────


@_op(authentik_write)
def create_wsfed_provider(name: str, **kwargs):
    """Create a WS-Fed provider. Required: name."""
    return _ok(_get_client().post("/providers/wsfed/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_wsfed_provider(id: int, **kwargs):
    """Update a WS-Fed provider."""
    return _ok(_get_client().patch(f"/providers/wsfed/{id}/", json=kwargs))


# ── Providers — SSF ──────────────────────────────────────────────────


@_op(authentik_write)
def create_ssf_provider(name: str, **kwargs):
    """Create an SSF provider. Required: name."""
    return _ok(_get_client().post("/providers/ssf/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_ssf_provider(id: int, **kwargs):
    """Update an SSF provider."""
    return _ok(_get_client().patch(f"/providers/ssf/{id}/", json=kwargs))
