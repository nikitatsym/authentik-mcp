from ..registry import _op
from .groups import authentik_read
from .helpers import SLIM_PROPERTY_MAPPING, _get_client, _paginated

# ── Property Mappings — All ──────────────────────────────────────────


@_op(authentik_read)
def list_property_mappings(limit: int = 20):
    """List all property mappings."""
    return _paginated("/propertymappings/all/", limit=limit, slim_fields=SLIM_PROPERTY_MAPPING)


@_op(authentik_read)
def show_property_mapping(id: str):
    """Get property mapping details."""
    return _get_client().get(f"/propertymappings/all/{id}/")


@_op(authentik_read)
def list_property_mapping_types():
    """List property mapping types."""
    return _get_client().get("/propertymappings/all/types/")


# ── Provider Mappings ────────────────────────────────────────────────


@_op(authentik_read)
def list_scope_mappings(limit: int = 20):
    """List OAuth2 scope mappings."""
    return _paginated("/propertymappings/provider/scope/", limit=limit, slim_fields=SLIM_PROPERTY_MAPPING)


@_op(authentik_read)
def show_scope_mapping(id: str):
    """Get scope mapping details."""
    return _get_client().get(f"/propertymappings/provider/scope/{id}/")


@_op(authentik_read)
def list_saml_property_mappings(limit: int = 20):
    """List SAML property mappings."""
    return _paginated("/propertymappings/provider/saml/", limit=limit, slim_fields=SLIM_PROPERTY_MAPPING)


@_op(authentik_read)
def show_saml_property_mapping(id: str):
    """Get SAML property mapping details."""
    return _get_client().get(f"/propertymappings/provider/saml/{id}/")


@_op(authentik_read)
def list_scim_property_mappings(limit: int = 20):
    """List SCIM property mappings."""
    return _paginated("/propertymappings/provider/scim/", limit=limit, slim_fields=SLIM_PROPERTY_MAPPING)


@_op(authentik_read)
def show_scim_property_mapping(id: str):
    """Get SCIM property mapping details."""
    return _get_client().get(f"/propertymappings/provider/scim/{id}/")


@_op(authentik_read)
def list_radius_property_mappings(limit: int = 20):
    """List Radius property mappings."""
    return _paginated("/propertymappings/provider/radius/", limit=limit, slim_fields=SLIM_PROPERTY_MAPPING)


@_op(authentik_read)
def show_radius_property_mapping(id: str):
    """Get Radius property mapping details."""
    return _get_client().get(f"/propertymappings/provider/radius/{id}/")


@_op(authentik_read)
def list_rac_property_mappings(limit: int = 20):
    """List RAC property mappings."""
    return _paginated("/propertymappings/provider/rac/", limit=limit, slim_fields=SLIM_PROPERTY_MAPPING)


@_op(authentik_read)
def show_rac_property_mapping(id: str):
    """Get RAC property mapping details."""
    return _get_client().get(f"/propertymappings/provider/rac/{id}/")


@_op(authentik_read)
def list_google_workspace_property_mappings(limit: int = 20):
    """List Google Workspace property mappings."""
    return _paginated("/propertymappings/provider/google_workspace/", limit=limit, slim_fields=SLIM_PROPERTY_MAPPING)


@_op(authentik_read)
def show_google_workspace_property_mapping(id: str):
    """Get Google Workspace property mapping details."""
    return _get_client().get(f"/propertymappings/provider/google_workspace/{id}/")


@_op(authentik_read)
def list_microsoft_entra_property_mappings(limit: int = 20):
    """List Microsoft Entra property mappings."""
    return _paginated("/propertymappings/provider/microsoft_entra/", limit=limit, slim_fields=SLIM_PROPERTY_MAPPING)


@_op(authentik_read)
def show_microsoft_entra_property_mapping(id: str):
    """Get Microsoft Entra property mapping details."""
    return _get_client().get(f"/propertymappings/provider/microsoft_entra/{id}/")


# ── Notification Mappings ────────────────────────────────────────────


@_op(authentik_read)
def list_notification_mappings(limit: int = 20):
    """List notification property mappings."""
    return _paginated("/propertymappings/notification/", limit=limit, slim_fields=SLIM_PROPERTY_MAPPING)


@_op(authentik_read)
def show_notification_mapping(id: str):
    """Get notification property mapping details."""
    return _get_client().get(f"/propertymappings/notification/{id}/")


# ── Source Mappings ──────────────────────────────────────────────────


@_op(authentik_read)
def list_ldap_source_mappings(limit: int = 20):
    """List LDAP source property mappings."""
    return _paginated("/propertymappings/source/ldap/", limit=limit, slim_fields=SLIM_PROPERTY_MAPPING)


@_op(authentik_read)
def show_ldap_source_mapping(id: str):
    """Get LDAP source property mapping details."""
    return _get_client().get(f"/propertymappings/source/ldap/{id}/")


@_op(authentik_read)
def list_oauth_source_mappings(limit: int = 20):
    """List OAuth source property mappings."""
    return _paginated("/propertymappings/source/oauth/", limit=limit, slim_fields=SLIM_PROPERTY_MAPPING)


@_op(authentik_read)
def show_oauth_source_mapping(id: str):
    """Get OAuth source property mapping details."""
    return _get_client().get(f"/propertymappings/source/oauth/{id}/")


@_op(authentik_read)
def list_saml_source_mappings(limit: int = 20):
    """List SAML source property mappings."""
    return _paginated("/propertymappings/source/saml/", limit=limit, slim_fields=SLIM_PROPERTY_MAPPING)


@_op(authentik_read)
def show_saml_source_mapping(id: str):
    """Get SAML source property mapping details."""
    return _get_client().get(f"/propertymappings/source/saml/{id}/")


@_op(authentik_read)
def list_scim_source_mappings(limit: int = 20):
    """List SCIM source property mappings."""
    return _paginated("/propertymappings/source/scim/", limit=limit, slim_fields=SLIM_PROPERTY_MAPPING)


@_op(authentik_read)
def show_scim_source_mapping(id: str):
    """Get SCIM source property mapping details."""
    return _get_client().get(f"/propertymappings/source/scim/{id}/")


@_op(authentik_read)
def list_kerberos_source_mappings(limit: int = 20):
    """List Kerberos source property mappings."""
    return _paginated("/propertymappings/source/kerberos/", limit=limit, slim_fields=SLIM_PROPERTY_MAPPING)


@_op(authentik_read)
def show_kerberos_source_mapping(id: str):
    """Get Kerberos source property mapping details."""
    return _get_client().get(f"/propertymappings/source/kerberos/{id}/")


@_op(authentik_read)
def list_plex_source_mappings(limit: int = 20):
    """List Plex source property mappings."""
    return _paginated("/propertymappings/source/plex/", limit=limit, slim_fields=SLIM_PROPERTY_MAPPING)


@_op(authentik_read)
def show_plex_source_mapping(id: str):
    """Get Plex source property mapping details."""
    return _get_client().get(f"/propertymappings/source/plex/{id}/")


@_op(authentik_read)
def list_telegram_source_mappings(limit: int = 20):
    """List Telegram source property mappings."""
    return _paginated("/propertymappings/source/telegram/", limit=limit, slim_fields=SLIM_PROPERTY_MAPPING)


@_op(authentik_read)
def show_telegram_source_mapping(id: str):
    """Get Telegram source property mapping details."""
    return _get_client().get(f"/propertymappings/source/telegram/{id}/")
