from ..registry import _op
from .groups import authentik_write
from .helpers import _get_client, _ok

# ── Test ─────────────────────────────────────────────────────────────


@_op(authentik_write)
def test_property_mapping(id: str, **kwargs):
    """Test a property mapping."""
    return _ok(_get_client().post(f"/propertymappings/all/{id}/test/", json=kwargs))


# ── Provider Mappings ────────────────────────────────────────────────


@_op(authentik_write)
def create_scope_mapping(name: str, **kwargs):
    """Create an OAuth2 scope mapping. Required: name."""
    return _ok(_get_client().post("/propertymappings/provider/scope/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_scope_mapping(id: str, **kwargs):
    """Update an OAuth2 scope mapping."""
    return _ok(_get_client().patch(f"/propertymappings/provider/scope/{id}/", json=kwargs))


@_op(authentik_write)
def create_saml_property_mapping(name: str, **kwargs):
    """Create a SAML property mapping. Required: name."""
    return _ok(_get_client().post("/propertymappings/provider/saml/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_saml_property_mapping(id: str, **kwargs):
    """Update a SAML property mapping."""
    return _ok(_get_client().patch(f"/propertymappings/provider/saml/{id}/", json=kwargs))


@_op(authentik_write)
def create_scim_property_mapping(name: str, **kwargs):
    """Create a SCIM property mapping. Required: name."""
    return _ok(_get_client().post("/propertymappings/provider/scim/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_scim_property_mapping(id: str, **kwargs):
    """Update a SCIM property mapping."""
    return _ok(_get_client().patch(f"/propertymappings/provider/scim/{id}/", json=kwargs))


@_op(authentik_write)
def create_radius_property_mapping(name: str, **kwargs):
    """Create a Radius property mapping. Required: name."""
    return _ok(_get_client().post("/propertymappings/provider/radius/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_radius_property_mapping(id: str, **kwargs):
    """Update a Radius property mapping."""
    return _ok(_get_client().patch(f"/propertymappings/provider/radius/{id}/", json=kwargs))


@_op(authentik_write)
def create_rac_property_mapping(name: str, **kwargs):
    """Create a RAC property mapping. Required: name."""
    return _ok(_get_client().post("/propertymappings/provider/rac/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_rac_property_mapping(id: str, **kwargs):
    """Update a RAC property mapping."""
    return _ok(_get_client().patch(f"/propertymappings/provider/rac/{id}/", json=kwargs))


@_op(authentik_write)
def create_google_workspace_property_mapping(name: str, **kwargs):
    """Create a Google Workspace property mapping. Required: name."""
    return _ok(_get_client().post("/propertymappings/provider/google_workspace/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_google_workspace_property_mapping(id: str, **kwargs):
    """Update a Google Workspace property mapping."""
    return _ok(_get_client().patch(f"/propertymappings/provider/google_workspace/{id}/", json=kwargs))


@_op(authentik_write)
def create_microsoft_entra_property_mapping(name: str, **kwargs):
    """Create a Microsoft Entra property mapping. Required: name."""
    return _ok(_get_client().post("/propertymappings/provider/microsoft_entra/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_microsoft_entra_property_mapping(id: str, **kwargs):
    """Update a Microsoft Entra property mapping."""
    return _ok(_get_client().patch(f"/propertymappings/provider/microsoft_entra/{id}/", json=kwargs))


# ── Notification Mappings ────────────────────────────────────────────


@_op(authentik_write)
def create_notification_mapping(name: str, **kwargs):
    """Create a notification property mapping. Required: name."""
    return _ok(_get_client().post("/propertymappings/notification/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_notification_mapping(id: str, **kwargs):
    """Update a notification property mapping."""
    return _ok(_get_client().patch(f"/propertymappings/notification/{id}/", json=kwargs))


# ── Source Mappings ──────────────────────────────────────────────────


@_op(authentik_write)
def create_ldap_source_mapping(name: str, **kwargs):
    """Create an LDAP source mapping. Required: name."""
    return _ok(_get_client().post("/propertymappings/source/ldap/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_ldap_source_mapping(id: str, **kwargs):
    """Update an LDAP source mapping."""
    return _ok(_get_client().patch(f"/propertymappings/source/ldap/{id}/", json=kwargs))


@_op(authentik_write)
def create_oauth_source_mapping(name: str, **kwargs):
    """Create an OAuth source mapping. Required: name."""
    return _ok(_get_client().post("/propertymappings/source/oauth/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_oauth_source_mapping(id: str, **kwargs):
    """Update an OAuth source mapping."""
    return _ok(_get_client().patch(f"/propertymappings/source/oauth/{id}/", json=kwargs))


@_op(authentik_write)
def create_saml_source_mapping(name: str, **kwargs):
    """Create a SAML source mapping. Required: name."""
    return _ok(_get_client().post("/propertymappings/source/saml/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_saml_source_mapping(id: str, **kwargs):
    """Update a SAML source mapping."""
    return _ok(_get_client().patch(f"/propertymappings/source/saml/{id}/", json=kwargs))


@_op(authentik_write)
def create_scim_source_mapping(name: str, **kwargs):
    """Create a SCIM source mapping. Required: name."""
    return _ok(_get_client().post("/propertymappings/source/scim/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_scim_source_mapping(id: str, **kwargs):
    """Update a SCIM source mapping."""
    return _ok(_get_client().patch(f"/propertymappings/source/scim/{id}/", json=kwargs))


@_op(authentik_write)
def create_kerberos_source_mapping(name: str, **kwargs):
    """Create a Kerberos source mapping. Required: name."""
    return _ok(_get_client().post("/propertymappings/source/kerberos/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_kerberos_source_mapping(id: str, **kwargs):
    """Update a Kerberos source mapping."""
    return _ok(_get_client().patch(f"/propertymappings/source/kerberos/{id}/", json=kwargs))


@_op(authentik_write)
def create_plex_source_mapping(name: str, **kwargs):
    """Create a Plex source mapping. Required: name."""
    return _ok(_get_client().post("/propertymappings/source/plex/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_plex_source_mapping(id: str, **kwargs):
    """Update a Plex source mapping."""
    return _ok(_get_client().patch(f"/propertymappings/source/plex/{id}/", json=kwargs))


@_op(authentik_write)
def create_telegram_source_mapping(name: str, **kwargs):
    """Create a Telegram source mapping. Required: name."""
    return _ok(_get_client().post("/propertymappings/source/telegram/", json={"name": name, **kwargs}))


@_op(authentik_write)
def update_telegram_source_mapping(id: str, **kwargs):
    """Update a Telegram source mapping."""
    return _ok(_get_client().patch(f"/propertymappings/source/telegram/{id}/", json=kwargs))
