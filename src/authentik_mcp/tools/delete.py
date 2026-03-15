from ..registry import _op
from .groups import authentik_delete
from .helpers import _get_client, _ok

# ── Core ─────────────────────────────────────────────────────────────


@_op(authentik_delete)
def delete_user(id: int):
    """Delete a user. Irreversible."""
    return _ok(_get_client().delete(f"/core/users/{id}/"))


@_op(authentik_delete)
def delete_group(id: str):
    """Delete a group. Irreversible."""
    return _ok(_get_client().delete(f"/core/groups/{id}/"))


@_op(authentik_delete)
def delete_application(slug: str):
    """Delete an application. Irreversible."""
    return _ok(_get_client().delete(f"/core/applications/{slug}/"))


@_op(authentik_delete)
def delete_app_entitlement(id: str):
    """Delete an application entitlement. Irreversible."""
    return _ok(_get_client().delete(f"/core/application_entitlements/{id}/"))


@_op(authentik_delete)
def delete_token(identifier: str):
    """Delete a token. Irreversible."""
    return _ok(_get_client().delete(f"/core/tokens/{identifier}/"))


@_op(authentik_delete)
def delete_brand(id: str):
    """Delete a brand. Irreversible."""
    return _ok(_get_client().delete(f"/core/brands/{id}/"))


@_op(authentik_delete)
def delete_session(id: str):
    """Delete a session. Irreversible."""
    return _ok(_get_client().delete(f"/core/authenticated_sessions/{id}/"))


@_op(authentik_delete)
def bulk_delete_sessions():
    """Bulk delete all sessions. Irreversible."""
    return _ok(_get_client().delete("/core/authenticated_sessions/bulk_delete/"))


@_op(authentik_delete)
def delete_user_consent(id: int):
    """Delete a user consent entry. Irreversible."""
    return _ok(_get_client().delete(f"/core/user_consent/{id}/"))


# ── Providers ────────────────────────────────────────────────────────


@_op(authentik_delete)
def delete_provider(id: int):
    """Delete a provider. Irreversible."""
    return _ok(_get_client().delete(f"/providers/all/{id}/"))


@_op(authentik_delete)
def delete_oauth2_provider(id: int):
    """Delete an OAuth2 provider. Irreversible."""
    return _ok(_get_client().delete(f"/providers/oauth2/{id}/"))


@_op(authentik_delete)
def delete_ldap_provider(id: int):
    """Delete an LDAP provider. Irreversible."""
    return _ok(_get_client().delete(f"/providers/ldap/{id}/"))


@_op(authentik_delete)
def delete_saml_provider(id: int):
    """Delete a SAML provider. Irreversible."""
    return _ok(_get_client().delete(f"/providers/saml/{id}/"))


@_op(authentik_delete)
def delete_proxy_provider(id: int):
    """Delete a proxy provider. Irreversible."""
    return _ok(_get_client().delete(f"/providers/proxy/{id}/"))


@_op(authentik_delete)
def delete_scim_provider(id: int):
    """Delete a SCIM provider. Irreversible."""
    return _ok(_get_client().delete(f"/providers/scim/{id}/"))


@_op(authentik_delete)
def delete_radius_provider(id: int):
    """Delete a Radius provider. Irreversible."""
    return _ok(_get_client().delete(f"/providers/radius/{id}/"))


@_op(authentik_delete)
def delete_rac_provider(id: int):
    """Delete a RAC provider. Irreversible."""
    return _ok(_get_client().delete(f"/providers/rac/{id}/"))


@_op(authentik_delete)
def delete_google_workspace_provider(id: int):
    """Delete a Google Workspace provider. Irreversible."""
    return _ok(_get_client().delete(f"/providers/google_workspace/{id}/"))


@_op(authentik_delete)
def delete_microsoft_entra_provider(id: int):
    """Delete a Microsoft Entra provider. Irreversible."""
    return _ok(_get_client().delete(f"/providers/microsoft_entra/{id}/"))


@_op(authentik_delete)
def delete_wsfed_provider(id: int):
    """Delete a WS-Fed provider. Irreversible."""
    return _ok(_get_client().delete(f"/providers/wsfed/{id}/"))


@_op(authentik_delete)
def delete_ssf_provider(id: int):
    """Delete an SSF provider. Irreversible."""
    return _ok(_get_client().delete(f"/providers/ssf/{id}/"))


# ── Flows ────────────────────────────────────────────────────────────


@_op(authentik_delete)
def delete_flow(slug: str):
    """Delete a flow. Irreversible."""
    return _ok(_get_client().delete(f"/flows/instances/{slug}/"))


@_op(authentik_delete)
def delete_flow_binding(id: str):
    """Delete a flow stage binding. Irreversible."""
    return _ok(_get_client().delete(f"/flows/bindings/{id}/"))


# ── Outposts ─────────────────────────────────────────────────────────


@_op(authentik_delete)
def delete_outpost(id: str):
    """Delete an outpost. Irreversible."""
    return _ok(_get_client().delete(f"/outposts/instances/{id}/"))


@_op(authentik_delete)
def delete_service_connection(id: str):
    """Delete a service connection. Irreversible."""
    return _ok(_get_client().delete(f"/outposts/service_connections/all/{id}/"))


@_op(authentik_delete)
def delete_docker_service_connection(id: str):
    """Delete a Docker service connection. Irreversible."""
    return _ok(_get_client().delete(f"/outposts/service_connections/docker/{id}/"))


@_op(authentik_delete)
def delete_kubernetes_service_connection(id: str):
    """Delete a Kubernetes service connection. Irreversible."""
    return _ok(_get_client().delete(f"/outposts/service_connections/kubernetes/{id}/"))


# ── Policies ─────────────────────────────────────────────────────────


@_op(authentik_delete)
def delete_policy(id: str):
    """Delete a policy. Irreversible."""
    return _ok(_get_client().delete(f"/policies/all/{id}/"))


@_op(authentik_delete)
def delete_policy_binding(id: str):
    """Delete a policy binding. Irreversible."""
    return _ok(_get_client().delete(f"/policies/bindings/{id}/"))


@_op(authentik_delete)
def delete_expression_policy(id: str):
    """Delete an expression policy. Irreversible."""
    return _ok(_get_client().delete(f"/policies/expression/{id}/"))


@_op(authentik_delete)
def delete_password_policy(id: str):
    """Delete a password policy. Irreversible."""
    return _ok(_get_client().delete(f"/policies/password/{id}/"))


@_op(authentik_delete)
def delete_password_expiry_policy(id: str):
    """Delete a password expiry policy. Irreversible."""
    return _ok(_get_client().delete(f"/policies/password_expiry/{id}/"))


@_op(authentik_delete)
def delete_reputation_policy(id: str):
    """Delete a reputation policy. Irreversible."""
    return _ok(_get_client().delete(f"/policies/reputation/{id}/"))


@_op(authentik_delete)
def delete_reputation_score(id: int):
    """Delete a reputation score. Irreversible."""
    return _ok(_get_client().delete(f"/policies/reputation/scores/{id}/"))


@_op(authentik_delete)
def delete_event_matcher_policy(id: str):
    """Delete an event matcher policy. Irreversible."""
    return _ok(_get_client().delete(f"/policies/event_matcher/{id}/"))


@_op(authentik_delete)
def delete_geoip_policy(id: str):
    """Delete a GeoIP policy. Irreversible."""
    return _ok(_get_client().delete(f"/policies/geoip/{id}/"))


@_op(authentik_delete)
def delete_dummy_policy(id: str):
    """Delete a dummy policy. Irreversible."""
    return _ok(_get_client().delete(f"/policies/dummy/{id}/"))


@_op(authentik_delete)
def delete_unique_password_policy(id: str):
    """Delete a unique password policy. Irreversible."""
    return _ok(_get_client().delete(f"/policies/unique_password/{id}/"))


# ── Events ───────────────────────────────────────────────────────────


@_op(authentik_delete)
def delete_event(id: str):
    """Delete an event. Irreversible."""
    return _ok(_get_client().delete(f"/events/events/{id}/"))


@_op(authentik_delete)
def delete_notification(id: str):
    """Delete a notification. Irreversible."""
    return _ok(_get_client().delete(f"/events/notifications/{id}/"))


@_op(authentik_delete)
def delete_notification_rule(id: str):
    """Delete a notification rule. Irreversible."""
    return _ok(_get_client().delete(f"/events/rules/{id}/"))


@_op(authentik_delete)
def delete_notification_transport(id: str):
    """Delete a notification transport. Irreversible."""
    return _ok(_get_client().delete(f"/events/transports/{id}/"))


# ── Stages ───────────────────────────────────────────────────────────


@_op(authentik_delete)
def delete_stage(id: str):
    """Delete a stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/all/{id}/"))


@_op(authentik_delete)
def delete_identification_stage(id: str):
    """Delete an identification stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/identification/{id}/"))


@_op(authentik_delete)
def delete_password_stage(id: str):
    """Delete a password stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/password/{id}/"))


@_op(authentik_delete)
def delete_authenticator_totp_stage(id: str):
    """Delete a TOTP authenticator stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/authenticator/totp/{id}/"))


@_op(authentik_delete)
def delete_authenticator_webauthn_stage(id: str):
    """Delete a WebAuthn authenticator stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/authenticator/webauthn/{id}/"))


@_op(authentik_delete)
def delete_authenticator_duo_stage(id: str):
    """Delete a Duo authenticator stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/authenticator/duo/{id}/"))


@_op(authentik_delete)
def delete_authenticator_sms_stage(id: str):
    """Delete an SMS authenticator stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/authenticator/sms/{id}/"))


@_op(authentik_delete)
def delete_authenticator_email_stage(id: str):
    """Delete an email authenticator stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/authenticator/email/{id}/"))


@_op(authentik_delete)
def delete_authenticator_static_stage(id: str):
    """Delete a static authenticator stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/authenticator/static/{id}/"))


@_op(authentik_delete)
def delete_authenticator_validate_stage(id: str):
    """Delete an authenticator validate stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/authenticator/validate/{id}/"))


@_op(authentik_delete)
def delete_authenticator_endpoint_gdtc_stage(id: str):
    """Delete an endpoint GDTC authenticator stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/authenticator/endpoint_gdtc/{id}/"))


@_op(authentik_delete)
def delete_user_login_stage(id: str):
    """Delete a user login stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/user_login/{id}/"))


@_op(authentik_delete)
def delete_user_logout_stage(id: str):
    """Delete a user logout stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/user_logout/{id}/"))


@_op(authentik_delete)
def delete_user_write_stage(id: str):
    """Delete a user write stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/user_write/{id}/"))


@_op(authentik_delete)
def delete_user_delete_stage(id: str):
    """Delete a user delete stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/user_delete/{id}/"))


@_op(authentik_delete)
def delete_consent_stage(id: str):
    """Delete a consent stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/consent/{id}/"))


@_op(authentik_delete)
def delete_captcha_stage(id: str):
    """Delete a captcha stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/captcha/{id}/"))


@_op(authentik_delete)
def delete_deny_stage(id: str):
    """Delete a deny stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/deny/{id}/"))


@_op(authentik_delete)
def delete_dummy_stage(id: str):
    """Delete a dummy stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/dummy/{id}/"))


@_op(authentik_delete)
def delete_email_stage(id: str):
    """Delete an email stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/email/{id}/"))


@_op(authentik_delete)
def delete_redirect_stage(id: str):
    """Delete a redirect stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/redirect/{id}/"))


@_op(authentik_delete)
def delete_source_stage(id: str):
    """Delete a source stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/source/{id}/"))


@_op(authentik_delete)
def delete_mtls_stage(id: str):
    """Delete an mTLS stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/mtls/{id}/"))


@_op(authentik_delete)
def delete_endpoint_stage(id: str):
    """Delete an endpoint stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/endpoints/{id}/"))


@_op(authentik_delete)
def delete_invitation_stage(id: str):
    """Delete an invitation stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/invitation/stages/{id}/"))


@_op(authentik_delete)
def delete_invitation(id: str):
    """Delete an invitation. Irreversible."""
    return _ok(_get_client().delete(f"/stages/invitation/invitations/{id}/"))


@_op(authentik_delete)
def delete_prompt_stage(id: str):
    """Delete a prompt stage. Irreversible."""
    return _ok(_get_client().delete(f"/stages/prompt/stages/{id}/"))


@_op(authentik_delete)
def delete_prompt(id: str):
    """Delete a prompt. Irreversible."""
    return _ok(_get_client().delete(f"/stages/prompt/prompts/{id}/"))


# ── Sources ──────────────────────────────────────────────────────────


@_op(authentik_delete)
def delete_source(slug: str):
    """Delete a source. Irreversible."""
    return _ok(_get_client().delete(f"/sources/all/{slug}/"))


@_op(authentik_delete)
def delete_ldap_source(slug: str):
    """Delete an LDAP source. Irreversible."""
    return _ok(_get_client().delete(f"/sources/ldap/{slug}/"))


@_op(authentik_delete)
def delete_oauth_source(slug: str):
    """Delete an OAuth source. Irreversible."""
    return _ok(_get_client().delete(f"/sources/oauth/{slug}/"))


@_op(authentik_delete)
def delete_saml_source(slug: str):
    """Delete a SAML source. Irreversible."""
    return _ok(_get_client().delete(f"/sources/saml/{slug}/"))


@_op(authentik_delete)
def delete_scim_source(slug: str):
    """Delete a SCIM source. Irreversible."""
    return _ok(_get_client().delete(f"/sources/scim/{slug}/"))


@_op(authentik_delete)
def delete_plex_source(slug: str):
    """Delete a Plex source. Irreversible."""
    return _ok(_get_client().delete(f"/sources/plex/{slug}/"))


@_op(authentik_delete)
def delete_kerberos_source(slug: str):
    """Delete a Kerberos source. Irreversible."""
    return _ok(_get_client().delete(f"/sources/kerberos/{slug}/"))


@_op(authentik_delete)
def delete_telegram_source(slug: str):
    """Delete a Telegram source. Irreversible."""
    return _ok(_get_client().delete(f"/sources/telegram/{slug}/"))


@_op(authentik_delete)
def delete_user_connection(id: int):
    """Delete a user source connection. Irreversible."""
    return _ok(_get_client().delete(f"/sources/user_connections/all/{id}/"))


@_op(authentik_delete)
def delete_group_connection(id: int):
    """Delete a group source connection. Irreversible."""
    return _ok(_get_client().delete(f"/sources/group_connections/all/{id}/"))


# ── Crypto ───────────────────────────────────────────────────────────


@_op(authentik_delete)
def delete_certificate(id: str):
    """Delete a certificate-key pair. Irreversible."""
    return _ok(_get_client().delete(f"/crypto/certificatekeypairs/{id}/"))


# ── RBAC ─────────────────────────────────────────────────────────────


@_op(authentik_delete)
def delete_role(id: str):
    """Delete an RBAC role. Irreversible."""
    return _ok(_get_client().delete(f"/rbac/roles/{id}/"))


@_op(authentik_delete)
def delete_initial_permission(id: int):
    """Delete an initial permission. Irreversible."""
    return _ok(_get_client().delete(f"/rbac/initial_permissions/{id}/"))


# ── Property Mappings ────────────────────────────────────────────────


@_op(authentik_delete)
def delete_property_mapping(id: str):
    """Delete a property mapping. Irreversible."""
    return _ok(_get_client().delete(f"/propertymappings/all/{id}/"))


@_op(authentik_delete)
def delete_scope_mapping(id: str):
    """Delete a scope mapping. Irreversible."""
    return _ok(_get_client().delete(f"/propertymappings/provider/scope/{id}/"))


@_op(authentik_delete)
def delete_saml_property_mapping(id: str):
    """Delete a SAML property mapping. Irreversible."""
    return _ok(_get_client().delete(f"/propertymappings/provider/saml/{id}/"))


@_op(authentik_delete)
def delete_scim_property_mapping(id: str):
    """Delete a SCIM property mapping. Irreversible."""
    return _ok(_get_client().delete(f"/propertymappings/provider/scim/{id}/"))


@_op(authentik_delete)
def delete_radius_property_mapping(id: str):
    """Delete a Radius property mapping. Irreversible."""
    return _ok(_get_client().delete(f"/propertymappings/provider/radius/{id}/"))


@_op(authentik_delete)
def delete_rac_property_mapping(id: str):
    """Delete a RAC property mapping. Irreversible."""
    return _ok(_get_client().delete(f"/propertymappings/provider/rac/{id}/"))


@_op(authentik_delete)
def delete_google_workspace_property_mapping(id: str):
    """Delete a Google Workspace property mapping. Irreversible."""
    return _ok(_get_client().delete(f"/propertymappings/provider/google_workspace/{id}/"))


@_op(authentik_delete)
def delete_microsoft_entra_property_mapping(id: str):
    """Delete a Microsoft Entra property mapping. Irreversible."""
    return _ok(_get_client().delete(f"/propertymappings/provider/microsoft_entra/{id}/"))


@_op(authentik_delete)
def delete_notification_mapping(id: str):
    """Delete a notification property mapping. Irreversible."""
    return _ok(_get_client().delete(f"/propertymappings/notification/{id}/"))


@_op(authentik_delete)
def delete_ldap_source_mapping(id: str):
    """Delete an LDAP source mapping. Irreversible."""
    return _ok(_get_client().delete(f"/propertymappings/source/ldap/{id}/"))


@_op(authentik_delete)
def delete_oauth_source_mapping(id: str):
    """Delete an OAuth source mapping. Irreversible."""
    return _ok(_get_client().delete(f"/propertymappings/source/oauth/{id}/"))


@_op(authentik_delete)
def delete_saml_source_mapping(id: str):
    """Delete a SAML source mapping. Irreversible."""
    return _ok(_get_client().delete(f"/propertymappings/source/saml/{id}/"))


@_op(authentik_delete)
def delete_scim_source_mapping(id: str):
    """Delete a SCIM source mapping. Irreversible."""
    return _ok(_get_client().delete(f"/propertymappings/source/scim/{id}/"))


@_op(authentik_delete)
def delete_kerberos_source_mapping(id: str):
    """Delete a Kerberos source mapping. Irreversible."""
    return _ok(_get_client().delete(f"/propertymappings/source/kerberos/{id}/"))


@_op(authentik_delete)
def delete_plex_source_mapping(id: str):
    """Delete a Plex source mapping. Irreversible."""
    return _ok(_get_client().delete(f"/propertymappings/source/plex/{id}/"))


@_op(authentik_delete)
def delete_telegram_source_mapping(id: str):
    """Delete a Telegram source mapping. Irreversible."""
    return _ok(_get_client().delete(f"/propertymappings/source/telegram/{id}/"))


# ── Managed ──────────────────────────────────────────────────────────


@_op(authentik_delete)
def delete_blueprint(id: str):
    """Delete a blueprint. Irreversible."""
    return _ok(_get_client().delete(f"/managed/blueprints/{id}/"))


# ── OAuth2 Tokens ────────────────────────────────────────────────────


@_op(authentik_delete)
def delete_oauth2_access_token(id: int):
    """Delete an OAuth2 access token. Irreversible."""
    return _ok(_get_client().delete(f"/oauth2/access_tokens/{id}/"))


@_op(authentik_delete)
def delete_oauth2_authorization_code(id: int):
    """Delete an OAuth2 authorization code. Irreversible."""
    return _ok(_get_client().delete(f"/oauth2/authorization_codes/{id}/"))


@_op(authentik_delete)
def delete_oauth2_refresh_token(id: int):
    """Delete an OAuth2 refresh token. Irreversible."""
    return _ok(_get_client().delete(f"/oauth2/refresh_tokens/{id}/"))


# ── RAC ──────────────────────────────────────────────────────────────


@_op(authentik_delete)
def delete_rac_connection_token(id: str):
    """Delete a RAC connection token. Irreversible."""
    return _ok(_get_client().delete(f"/rac/connection_tokens/{id}/"))


@_op(authentik_delete)
def delete_rac_endpoint(id: str):
    """Delete a RAC endpoint. Irreversible."""
    return _ok(_get_client().delete(f"/rac/endpoints/{id}/"))


# ── Endpoints (Device Management) ────────────────────────────────────


@_op(authentik_delete)
def delete_endpoint_connector(id: str):
    """Delete an endpoint connector. Irreversible."""
    return _ok(_get_client().delete(f"/endpoints/connectors/{id}/"))


@_op(authentik_delete)
def delete_agent_connector(id: str):
    """Delete an agent connector. Irreversible."""
    return _ok(_get_client().delete(f"/endpoints/agents/connectors/{id}/"))


@_op(authentik_delete)
def delete_agent_enrollment_token(id: str):
    """Delete an agent enrollment token. Irreversible."""
    return _ok(_get_client().delete(f"/endpoints/agents/enrollment_tokens/{id}/"))


@_op(authentik_delete)
def delete_endpoint_device(id: str):
    """Delete an endpoint device. Irreversible."""
    return _ok(_get_client().delete(f"/endpoints/devices/{id}/"))


@_op(authentik_delete)
def delete_device_access_group(id: str):
    """Delete a device access group. Irreversible."""
    return _ok(_get_client().delete(f"/endpoints/device_access_groups/{id}/"))


@_op(authentik_delete)
def delete_device_binding(id: str):
    """Delete a device binding. Irreversible."""
    return _ok(_get_client().delete(f"/endpoints/device_bindings/{id}/"))


@_op(authentik_delete)
def delete_fleet_connector(id: str):
    """Delete a fleet connector. Irreversible."""
    return _ok(_get_client().delete(f"/endpoints/fleet_connectors/{id}/"))


@_op(authentik_delete)
def delete_google_chrome_connector(id: str):
    """Delete a Google Chrome connector. Irreversible."""
    return _ok(_get_client().delete(f"/endpoints/google_chrome_connectors/{id}/"))


# ── Enterprise ───────────────────────────────────────────────────────


@_op(authentik_delete)
def delete_license(id: str):
    """Delete an enterprise license. Irreversible."""
    return _ok(_get_client().delete(f"/enterprise/license/{id}/"))


# ── Tenants ──────────────────────────────────────────────────────────


@_op(authentik_delete)
def delete_tenant(id: str):
    """Delete a tenant. Irreversible."""
    return _ok(_get_client().delete(f"/tenants/tenants/{id}/"))


@_op(authentik_delete)
def delete_tenant_domain(id: str):
    """Delete a tenant domain. Irreversible."""
    return _ok(_get_client().delete(f"/tenants/domains/{id}/"))


# ── Admin ────────────────────────────────────────────────────────────


@_op(authentik_delete)
def delete_admin_file(id: str):
    """Delete an admin file. Irreversible."""
    return _ok(_get_client().delete(f"/admin/file/{id}/"))


# ── Authenticators ───────────────────────────────────────────────────


@_op(authentik_delete)
def delete_authenticator_totp(id: int):
    """Delete a TOTP authenticator device. Irreversible."""
    return _ok(_get_client().delete(f"/authenticators/totp/{id}/"))


@_op(authentik_delete)
def delete_authenticator_webauthn(id: int):
    """Delete a WebAuthn authenticator device. Irreversible."""
    return _ok(_get_client().delete(f"/authenticators/webauthn/{id}/"))


@_op(authentik_delete)
def delete_authenticator_duo(id: int):
    """Delete a Duo authenticator device. Irreversible."""
    return _ok(_get_client().delete(f"/authenticators/duo/{id}/"))


@_op(authentik_delete)
def delete_authenticator_sms(id: int):
    """Delete an SMS authenticator device. Irreversible."""
    return _ok(_get_client().delete(f"/authenticators/sms/{id}/"))


@_op(authentik_delete)
def delete_authenticator_static(id: int):
    """Delete a static authenticator device. Irreversible."""
    return _ok(_get_client().delete(f"/authenticators/static/{id}/"))


@_op(authentik_delete)
def delete_authenticator_email(id: int):
    """Delete an email authenticator device. Irreversible."""
    return _ok(_get_client().delete(f"/authenticators/email/{id}/"))


@_op(authentik_delete)
def delete_admin_duo_device(id: int):
    """Delete an admin Duo device. Irreversible."""
    return _ok(_get_client().delete(f"/authenticators/admin/duo/{id}/"))


@_op(authentik_delete)
def delete_admin_email_device(id: int):
    """Delete an admin email device. Irreversible."""
    return _ok(_get_client().delete(f"/authenticators/admin/email/{id}/"))


@_op(authentik_delete)
def delete_admin_endpoint_device(id: int):
    """Delete an admin endpoint device. Irreversible."""
    return _ok(_get_client().delete(f"/authenticators/admin/endpoint/{id}/"))


@_op(authentik_delete)
def delete_admin_sms_device(id: int):
    """Delete an admin SMS device. Irreversible."""
    return _ok(_get_client().delete(f"/authenticators/admin/sms/{id}/"))


@_op(authentik_delete)
def delete_admin_static_device(id: int):
    """Delete an admin static device. Irreversible."""
    return _ok(_get_client().delete(f"/authenticators/admin/static/{id}/"))


@_op(authentik_delete)
def delete_admin_totp_device(id: int):
    """Delete an admin TOTP device. Irreversible."""
    return _ok(_get_client().delete(f"/authenticators/admin/totp/{id}/"))


@_op(authentik_delete)
def delete_admin_webauthn_device(id: int):
    """Delete an admin WebAuthn device. Irreversible."""
    return _ok(_get_client().delete(f"/authenticators/admin/webauthn/{id}/"))


# ── Reports ──────────────────────────────────────────────────────────


@_op(authentik_delete)
def delete_export(id: str):
    """Delete a report export. Irreversible."""
    return _ok(_get_client().delete(f"/reports/exports/{id}/"))
