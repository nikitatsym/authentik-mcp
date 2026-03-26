---
tags: [mcp, python, task]
domain: dev
type: task
---

# authentik-mcp

MCP server for [Authentik](https://goauthentik.io/) identity provider.

- **MCP standard:** `/home/ari/src/obsidian_vault/specs/mcp-server.md` — follow it exactly (structure, registry, server dispatch, groups, config, client patterns)
- **API base:** `{AUTHENTIK_URL}/api/v3/`, auth: `Authorization: Bearer <token>`
- **OpenAPI spec:** `{AUTHENTIK_URL}/api/v3/schema/`
- **Health:** `GET /-/health/live/` (200 = running), `GET /-/health/ready/` (200 = DB ok)
- **Hosting:** GitHub — CI/CD from `/home/ari/src/vastai-mcp/.github/workflows/build.yml`, enable Pages (Actions source), create `docs/index.html` setup page

## Config

```
AUTHENTIK_URL     — base URL (e.g. https://auth.example.com)
AUTHENTIK_TOKEN   — API token (Bearer)
```

## Groups

authentik_read        — core resources: users, groups, apps, tokens, brands, sessions, providers, outposts, crypto, rbac, authenticators, property mappings, oauth2 tokens, managed, rac, endpoints, enterprise, tenants, tasks, reports, ssf, root (safe, read-only)
authentik_write       — create/update core resources (non-destructive)
authentik_delete      — all delete operations across all domains (destructive, irreversible)
authentik_flows_read  — auth pipeline config: flows, stages, policies, sources, events (safe, read-only)
authentik_flows_write — create/update auth pipeline config (non-destructive)
authentik_admin       — admin-only: settings, system, version, files, admin authenticator devices

## Operations

### authentik_read

| Operation | Endpoint | Notes |
|---|---|---|
| **Core — Users** | | |
| `list_users(search, path)` | `GET /core/users/` | Slim `_slim_user` |
| `show_user(id)` | `GET /core/users/{id}/` | Full |
| `get_me()` | `GET /core/users/me/` | Current user |
| `list_user_paths()` | `GET /core/users/paths/` | |
| `list_user_consent(user)` | `GET /core/user_consent/` | |
| `show_user_consent(id)` | `GET /core/user_consent/{id}/` | |
| **Core — Groups** | | |
| `list_groups(search)` | `GET /core/groups/` | Slim `_slim_group` |
| `show_group(id)` | `GET /core/groups/{id}/` | Full |
| **Core — Applications** | | |
| `list_applications(search)` | `GET /core/applications/` | Slim `_slim_app` |
| `show_application(slug)` | `GET /core/applications/{slug}/` | Full |
| `check_access(slug)` | `GET /core/applications/{slug}/check_access/` | |
| **Core — Application Entitlements** | | |
| `list_app_entitlements(app)` | `GET /core/application_entitlements/` | |
| `show_app_entitlement(id)` | `GET /core/application_entitlements/{id}/` | |
| **Core — Tokens** | | |
| `list_tokens()` | `GET /core/tokens/` | |
| `show_token(identifier)` | `GET /core/tokens/{identifier}/` | |
| `view_token_key(identifier)` | `GET /core/tokens/{identifier}/view_key/` | |
| **Core — Brands** | | |
| `list_brands()` | `GET /core/brands/` | |
| `show_brand(id)` | `GET /core/brands/{id}/` | |
| `get_current_brand()` | `GET /core/brands/current/` | |
| **Core — Sessions** | | |
| `list_sessions()` | `GET /core/authenticated_sessions/` | |
| `show_session(id)` | `GET /core/authenticated_sessions/{id}/` | |
| **Providers — All** | | |
| `list_providers()` | `GET /providers/all/` | All types |
| `show_provider(id)` | `GET /providers/all/{id}/` | Full |
| `list_provider_types()` | `GET /providers/all/types/` | |
| **Providers — OAuth2** | | |
| `list_oauth2_providers()` | `GET /providers/oauth2/` | |
| `show_oauth2_provider(id)` | `GET /providers/oauth2/{id}/` | |
| `get_oauth2_setup_urls(id)` | `GET /providers/oauth2/{id}/setup_urls/` | |
| `preview_oauth2_user(id)` | `GET /providers/oauth2/{id}/preview_user/` | |
| **Providers — LDAP** | | |
| `list_ldap_providers()` | `GET /providers/ldap/` | |
| `show_ldap_provider(id)` | `GET /providers/ldap/{id}/` | |
| **Providers — SAML** | | |
| `list_saml_providers()` | `GET /providers/saml/` | |
| `show_saml_provider(id)` | `GET /providers/saml/{id}/` | |
| `get_saml_metadata(id)` | `GET /providers/saml/{id}/metadata/` | |
| `preview_saml_user(id)` | `GET /providers/saml/{id}/preview_user/` | |
| **Providers — Proxy** | | |
| `list_proxy_providers()` | `GET /providers/proxy/` | |
| `show_proxy_provider(id)` | `GET /providers/proxy/{id}/` | |
| **Providers — SCIM** | | |
| `list_scim_providers()` | `GET /providers/scim/` | |
| `show_scim_provider(id)` | `GET /providers/scim/{id}/` | |
| `get_scim_sync_status(id)` | `GET /providers/scim/{id}/sync_status/` | |
| `list_scim_users(provider)` | `GET /providers/scim/{id}/users/` | |
| `list_scim_groups(provider)` | `GET /providers/scim/{id}/groups/` | |
| **Providers — Radius** | | |
| `list_radius_providers()` | `GET /providers/radius/` | |
| `show_radius_provider(id)` | `GET /providers/radius/{id}/` | |
| **Providers — RAC** | | |
| `list_rac_providers()` | `GET /providers/rac/` | |
| `show_rac_provider(id)` | `GET /providers/rac/{id}/` | |
| **Providers — Google Workspace** | | |
| `list_google_workspace_providers()` | `GET /providers/google_workspace/` | |
| `show_google_workspace_provider(id)` | `GET /providers/google_workspace/{id}/` | |
| `get_google_workspace_sync_status(id)` | `GET /providers/google_workspace/{id}/sync_status/` | |
| **Providers — Microsoft Entra** | | |
| `list_microsoft_entra_providers()` | `GET /providers/microsoft_entra/` | |
| `show_microsoft_entra_provider(id)` | `GET /providers/microsoft_entra/{id}/` | |
| `get_microsoft_entra_sync_status(id)` | `GET /providers/microsoft_entra/{id}/sync_status/` | |
| **Providers — WS-Fed** | | |
| `list_wsfed_providers()` | `GET /providers/wsfed/` | |
| `show_wsfed_provider(id)` | `GET /providers/wsfed/{id}/` | |
| `get_wsfed_metadata(id)` | `GET /providers/wsfed/{id}/metadata/` | |
| **Providers — SSF** | | |
| `list_ssf_providers()` | `GET /providers/ssf/` | |
| `show_ssf_provider(id)` | `GET /providers/ssf/{id}/` | |
| **Outposts** | | |
| `list_outposts()` | `GET /outposts/instances/` | |
| `show_outpost(id)` | `GET /outposts/instances/{id}/` | |
| `get_outpost_health(id)` | `GET /outposts/instances/{id}/health/` | |
| `get_outpost_default_settings()` | `GET /outposts/instances/default_settings/` | |
| `list_outpost_service_connections()` | `GET /outposts/service_connections/all/` | |
| `show_outpost_service_connection(id)` | `GET /outposts/service_connections/all/{id}/` | |
| `get_service_connection_state(id)` | `GET /outposts/service_connections/all/{id}/state/` | |
| `list_service_connection_types()` | `GET /outposts/service_connections/all/types/` | |
| `list_docker_service_connections()` | `GET /outposts/service_connections/docker/` | |
| `show_docker_service_connection(id)` | `GET /outposts/service_connections/docker/{id}/` | |
| `list_kubernetes_service_connections()` | `GET /outposts/service_connections/kubernetes/` | |
| `show_kubernetes_service_connection(id)` | `GET /outposts/service_connections/kubernetes/{id}/` | |
| `list_outpost_ldap(id)` | `GET /outposts/ldap/` | |
| `list_outpost_proxy(id)` | `GET /outposts/proxy/` | |
| `list_outpost_radius(id)` | `GET /outposts/radius/` | |
| **Crypto** | | |
| `list_certificates()` | `GET /crypto/certificatekeypairs/` | |
| `show_certificate(id)` | `GET /crypto/certificatekeypairs/{id}/` | |
| `view_certificate(id)` | `GET /crypto/certificatekeypairs/{id}/view_certificate/` | |
| `view_private_key(id)` | `GET /crypto/certificatekeypairs/{id}/view_private_key/` | |
| **RBAC** | | |
| `list_roles()` | `GET /rbac/roles/` | |
| `show_role(id)` | `GET /rbac/roles/{id}/` | |
| `list_permissions()` | `GET /rbac/permissions/` | |
| `show_permission(id)` | `GET /rbac/permissions/{id}/` | |
| `list_initial_permissions()` | `GET /rbac/initial_permissions/` | |
| `show_initial_permission(id)` | `GET /rbac/initial_permissions/{id}/` | |
| `list_permissions_assigned_by_roles()` | `GET /rbac/permissions/assigned_by_roles/` | |
| `list_permissions_roles()` | `GET /rbac/permissions/roles/` | |
| **Authenticators** | | |
| `list_authenticators()` | `GET /authenticators/all/` | All types |
| `list_authenticator_totp_devices()` | `GET /authenticators/totp/` | |
| `show_authenticator_totp_device(id)` | `GET /authenticators/totp/{id}/` | |
| `list_authenticator_webauthn_devices()` | `GET /authenticators/webauthn/` | |
| `show_authenticator_webauthn_device(id)` | `GET /authenticators/webauthn/{id}/` | |
| `list_authenticator_duo_devices()` | `GET /authenticators/duo/` | |
| `show_authenticator_duo_device(id)` | `GET /authenticators/duo/{id}/` | |
| `list_authenticator_sms_devices()` | `GET /authenticators/sms/` | |
| `show_authenticator_sms_device(id)` | `GET /authenticators/sms/{id}/` | |
| `list_authenticator_static_devices()` | `GET /authenticators/static/` | |
| `show_authenticator_static_device(id)` | `GET /authenticators/static/{id}/` | |
| `list_authenticator_email_devices()` | `GET /authenticators/email/` | |
| `show_authenticator_email_device(id)` | `GET /authenticators/email/{id}/` | |
| `list_authenticator_endpoint_devices()` | `GET /authenticators/endpoint/` | |
| `show_authenticator_endpoint_device(id)` | `GET /authenticators/endpoint/{id}/` | |
| **Property Mappings** | | |
| `list_property_mappings()` | `GET /propertymappings/all/` | All types |
| `show_property_mapping(id)` | `GET /propertymappings/all/{id}/` | Full |
| `list_property_mapping_types()` | `GET /propertymappings/all/types/` | |
| `list_scope_mappings()` | `GET /propertymappings/provider/scope/` | |
| `show_scope_mapping(id)` | `GET /propertymappings/provider/scope/{id}/` | |
| `list_saml_property_mappings()` | `GET /propertymappings/provider/saml/` | |
| `show_saml_property_mapping(id)` | `GET /propertymappings/provider/saml/{id}/` | |
| `list_scim_property_mappings()` | `GET /propertymappings/provider/scim/` | |
| `show_scim_property_mapping(id)` | `GET /propertymappings/provider/scim/{id}/` | |
| `list_radius_property_mappings()` | `GET /propertymappings/provider/radius/` | |
| `show_radius_property_mapping(id)` | `GET /propertymappings/provider/radius/{id}/` | |
| `list_rac_property_mappings()` | `GET /propertymappings/provider/rac/` | |
| `show_rac_property_mapping(id)` | `GET /propertymappings/provider/rac/{id}/` | |
| `list_google_workspace_property_mappings()` | `GET /propertymappings/provider/google_workspace/` | |
| `show_google_workspace_property_mapping(id)` | `GET /propertymappings/provider/google_workspace/{id}/` | |
| `list_microsoft_entra_property_mappings()` | `GET /propertymappings/provider/microsoft_entra/` | |
| `show_microsoft_entra_property_mapping(id)` | `GET /propertymappings/provider/microsoft_entra/{id}/` | |
| `list_notification_mappings()` | `GET /propertymappings/notification/` | |
| `show_notification_mapping(id)` | `GET /propertymappings/notification/{id}/` | |
| `list_ldap_source_mappings()` | `GET /propertymappings/source/ldap/` | |
| `show_ldap_source_mapping(id)` | `GET /propertymappings/source/ldap/{id}/` | |
| `list_oauth_source_mappings()` | `GET /propertymappings/source/oauth/` | |
| `show_oauth_source_mapping(id)` | `GET /propertymappings/source/oauth/{id}/` | |
| `list_saml_source_mappings()` | `GET /propertymappings/source/saml/` | |
| `show_saml_source_mapping(id)` | `GET /propertymappings/source/saml/{id}/` | |
| `list_scim_source_mappings()` | `GET /propertymappings/source/scim/` | |
| `show_scim_source_mapping(id)` | `GET /propertymappings/source/scim/{id}/` | |
| `list_kerberos_source_mappings()` | `GET /propertymappings/source/kerberos/` | |
| `show_kerberos_source_mapping(id)` | `GET /propertymappings/source/kerberos/{id}/` | |
| `list_plex_source_mappings()` | `GET /propertymappings/source/plex/` | |
| `show_plex_source_mapping(id)` | `GET /propertymappings/source/plex/{id}/` | |
| `list_telegram_source_mappings()` | `GET /propertymappings/source/telegram/` | |
| `show_telegram_source_mapping(id)` | `GET /propertymappings/source/telegram/{id}/` | |
| **OAuth2 Tokens** | | |
| `list_oauth2_access_tokens()` | `GET /oauth2/access_tokens/` | |
| `show_oauth2_access_token(id)` | `GET /oauth2/access_tokens/{id}/` | |
| `list_oauth2_authorization_codes()` | `GET /oauth2/authorization_codes/` | |
| `show_oauth2_authorization_code(id)` | `GET /oauth2/authorization_codes/{id}/` | |
| `list_oauth2_refresh_tokens()` | `GET /oauth2/refresh_tokens/` | |
| `show_oauth2_refresh_token(id)` | `GET /oauth2/refresh_tokens/{id}/` | |
| **Managed** | | |
| `list_blueprints()` | `GET /managed/blueprints/` | |
| `show_blueprint(id)` | `GET /managed/blueprints/{id}/` | |
| `list_available_blueprints()` | `GET /managed/blueprints/available/` | |
| **RAC** | | |
| `list_rac_connection_tokens()` | `GET /rac/connection_tokens/` | |
| `show_rac_connection_token(id)` | `GET /rac/connection_tokens/{id}/` | |
| `list_rac_endpoints()` | `GET /rac/endpoints/` | |
| `show_rac_endpoint(id)` | `GET /rac/endpoints/{id}/` | |
| **Endpoints (Device Management)** | | |
| `list_endpoint_devices()` | `GET /endpoints/devices/` | |
| `show_endpoint_device(id)` | `GET /endpoints/devices/{id}/` | |
| `get_endpoint_device_summary()` | `GET /endpoints/devices/summary/` | |
| `list_endpoint_connectors()` | `GET /endpoints/connectors/` | |
| `show_endpoint_connector(id)` | `GET /endpoints/connectors/{id}/` | |
| `list_endpoint_connector_types()` | `GET /endpoints/connectors/types/` | |
| `list_agent_connectors()` | `GET /endpoints/agents/connectors/` | |
| `show_agent_connector(id)` | `GET /endpoints/agents/connectors/{id}/` | |
| `list_agent_enrollment_tokens()` | `GET /endpoints/agents/enrollment_tokens/` | |
| `show_agent_enrollment_token(id)` | `GET /endpoints/agents/enrollment_tokens/{id}/` | |
| `view_enrollment_token_key(id)` | `GET /endpoints/agents/enrollment_tokens/{id}/view_key/` | |
| `list_device_access_groups()` | `GET /endpoints/device_access_groups/` | |
| `show_device_access_group(id)` | `GET /endpoints/device_access_groups/{id}/` | |
| `list_device_bindings()` | `GET /endpoints/device_bindings/` | |
| `show_device_binding(id)` | `GET /endpoints/device_bindings/{id}/` | |
| `list_fleet_connectors()` | `GET /endpoints/fleet_connectors/` | |
| `show_fleet_connector(id)` | `GET /endpoints/fleet_connectors/{id}/` | |
| `list_google_chrome_connectors()` | `GET /endpoints/google_chrome_connectors/` | |
| `show_google_chrome_connector(id)` | `GET /endpoints/google_chrome_connectors/{id}/` | |
| **Enterprise** | | |
| `list_licenses()` | `GET /enterprise/license/` | |
| `show_license(id)` | `GET /enterprise/license/{id}/` | |
| `get_license_forecast()` | `GET /enterprise/license/forecast/` | |
| `get_license_summary()` | `GET /enterprise/license/summary/` | |
| `get_install_id()` | `GET /enterprise/license/install_id/` | |
| **Tenants** | | |
| `list_tenants()` | `GET /tenants/tenants/` | |
| `show_tenant(id)` | `GET /tenants/tenants/{id}/` | |
| `list_tenant_domains()` | `GET /tenants/domains/` | |
| `show_tenant_domain(id)` | `GET /tenants/domains/{id}/` | |
| **Tasks** | | |
| `list_task_schedules()` | `GET /tasks/schedules/` | |
| `show_task_schedule(id)` | `GET /tasks/schedules/{id}/` | |
| `list_tasks()` | `GET /tasks/tasks/` | |
| `show_task(id)` | `GET /tasks/tasks/{id}/` | |
| `get_task_status(id)` | `GET /tasks/tasks/{id}/status/` | |
| `list_workers()` | `GET /tasks/workers/` | |
| **Reports** | | |
| `list_exports()` | `GET /reports/exports/` | |
| `show_export(id)` | `GET /reports/exports/{id}/` | |
| **SSF** | | |
| `list_ssf_streams()` | `GET /ssf/streams/` | |
| `show_ssf_stream(id)` | `GET /ssf/streams/{id}/` | |
| **Root** | | |
| `get_config()` | `GET /root/config/` | |

### authentik_flows_read

| Operation | Endpoint | Notes |
|---|---|---|
| **Flows** | | |
| `list_flows()` | `GET /flows/instances/` | Slim `_slim_flow` |
| `show_flow(slug)` | `GET /flows/instances/{slug}/` | Full |
| `get_flow_diagram(slug)` | `GET /flows/instances/{slug}/diagram/` | |
| `export_flow(slug)` | `GET /flows/instances/{slug}/export/` | |
| `list_flow_bindings()` | `GET /flows/bindings/` | |
| `show_flow_binding(id)` | `GET /flows/bindings/{id}/` | |
| **Policies — All** | | |
| `list_policies()` | `GET /policies/all/` | |
| `show_policy(id)` | `GET /policies/all/{id}/` | |
| `list_policy_types()` | `GET /policies/all/types/` | |
| `list_policy_bindings()` | `GET /policies/bindings/` | |
| `show_policy_binding(id)` | `GET /policies/bindings/{id}/` | |
| **Policies — Expression** | | |
| `list_expression_policies()` | `GET /policies/expression/` | |
| `show_expression_policy(id)` | `GET /policies/expression/{id}/` | |
| **Policies — Password** | | |
| `list_password_policies()` | `GET /policies/password/` | |
| `show_password_policy(id)` | `GET /policies/password/{id}/` | |
| `list_password_expiry_policies()` | `GET /policies/password_expiry/` | |
| `show_password_expiry_policy(id)` | `GET /policies/password_expiry/{id}/` | |
| `list_unique_password_policies()` | `GET /policies/unique_password/` | |
| `show_unique_password_policy(id)` | `GET /policies/unique_password/{id}/` | |
| **Policies — Reputation** | | |
| `list_reputation_policies()` | `GET /policies/reputation/` | |
| `show_reputation_policy(id)` | `GET /policies/reputation/{id}/` | |
| `list_reputation_scores()` | `GET /policies/reputation/scores/` | |
| `show_reputation_score(id)` | `GET /policies/reputation/scores/{id}/` | |
| **Policies — Event Matcher** | | |
| `list_event_matcher_policies()` | `GET /policies/event_matcher/` | |
| `show_event_matcher_policy(id)` | `GET /policies/event_matcher/{id}/` | |
| **Policies — GeoIP** | | |
| `list_geoip_policies()` | `GET /policies/geoip/` | |
| `show_geoip_policy(id)` | `GET /policies/geoip/{id}/` | |
| **Policies — Dummy** | | |
| `list_dummy_policies()` | `GET /policies/dummy/` | |
| `show_dummy_policy(id)` | `GET /policies/dummy/{id}/` | |
| **Events** | | |
| `list_events(action, search)` | `GET /events/events/` | Slim `_slim_event` |
| `show_event(id)` | `GET /events/events/{id}/` | Full |
| `list_event_actions()` | `GET /events/events/actions/` | |
| `list_event_per_month()` | `GET /events/events/per_month/` | |
| `list_event_top_per_user()` | `GET /events/events/top_per_user/` | |
| `get_event_volume()` | `GET /events/events/volume/` | |
| `list_notifications()` | `GET /events/notifications/` | |
| `show_notification(id)` | `GET /events/notifications/{id}/` | |
| `list_notification_rules()` | `GET /events/rules/` | |
| `show_notification_rule(id)` | `GET /events/rules/{id}/` | |
| `list_notification_transports()` | `GET /events/transports/` | |
| `show_notification_transport(id)` | `GET /events/transports/{id}/` | |
| `list_system_tasks()` | `GET /events/system_tasks/` | |
| `show_system_task(id)` | `GET /events/system_tasks/{id}/` | |
| **Stages — All** | | |
| `list_stages()` | `GET /stages/all/` | |
| `show_stage(id)` | `GET /stages/all/{id}/` | |
| `list_stage_types()` | `GET /stages/all/types/` | |
| **Stages — Identification** | | |
| `list_identification_stages()` | `GET /stages/identification/` | |
| `show_identification_stage(id)` | `GET /stages/identification/{id}/` | |
| **Stages — Password** | | |
| `list_password_stages()` | `GET /stages/password/` | |
| `show_password_stage(id)` | `GET /stages/password/{id}/` | |
| **Stages — Authenticator** | | |
| `list_authenticator_totp_stages()` | `GET /stages/authenticator/totp/` | |
| `show_authenticator_totp_stage(id)` | `GET /stages/authenticator/totp/{id}/` | |
| `list_authenticator_webauthn_stages()` | `GET /stages/authenticator/webauthn/` | |
| `show_authenticator_webauthn_stage(id)` | `GET /stages/authenticator/webauthn/{id}/` | |
| `list_authenticator_duo_stages()` | `GET /stages/authenticator/duo/` | |
| `show_authenticator_duo_stage(id)` | `GET /stages/authenticator/duo/{id}/` | |
| `list_authenticator_sms_stages()` | `GET /stages/authenticator/sms/` | |
| `show_authenticator_sms_stage(id)` | `GET /stages/authenticator/sms/{id}/` | |
| `list_authenticator_email_stages()` | `GET /stages/authenticator/email/` | |
| `show_authenticator_email_stage(id)` | `GET /stages/authenticator/email/{id}/` | |
| `list_authenticator_static_stages()` | `GET /stages/authenticator/static/` | |
| `show_authenticator_static_stage(id)` | `GET /stages/authenticator/static/{id}/` | |
| `list_authenticator_validate_stages()` | `GET /stages/authenticator/validate/` | |
| `show_authenticator_validate_stage(id)` | `GET /stages/authenticator/validate/{id}/` | |
| `list_authenticator_endpoint_gdtc_stages()` | `GET /stages/authenticator/endpoint_gdtc/` | |
| `show_authenticator_endpoint_gdtc_stage(id)` | `GET /stages/authenticator/endpoint_gdtc/{id}/` | |
| **Stages — User** | | |
| `list_user_login_stages()` | `GET /stages/user_login/` | |
| `show_user_login_stage(id)` | `GET /stages/user_login/{id}/` | |
| `list_user_logout_stages()` | `GET /stages/user_logout/` | |
| `show_user_logout_stage(id)` | `GET /stages/user_logout/{id}/` | |
| `list_user_write_stages()` | `GET /stages/user_write/` | |
| `show_user_write_stage(id)` | `GET /stages/user_write/{id}/` | |
| `list_user_delete_stages()` | `GET /stages/user_delete/` | |
| `show_user_delete_stage(id)` | `GET /stages/user_delete/{id}/` | |
| **Stages — Consent** | | |
| `list_consent_stages()` | `GET /stages/consent/` | |
| `show_consent_stage(id)` | `GET /stages/consent/{id}/` | |
| **Stages — Captcha** | | |
| `list_captcha_stages()` | `GET /stages/captcha/` | |
| `show_captcha_stage(id)` | `GET /stages/captcha/{id}/` | |
| **Stages — Deny** | | |
| `list_deny_stages()` | `GET /stages/deny/` | |
| `show_deny_stage(id)` | `GET /stages/deny/{id}/` | |
| **Stages — Dummy** | | |
| `list_dummy_stages()` | `GET /stages/dummy/` | |
| `show_dummy_stage(id)` | `GET /stages/dummy/{id}/` | |
| **Stages — Email** | | |
| `list_email_stages()` | `GET /stages/email/` | |
| `show_email_stage(id)` | `GET /stages/email/{id}/` | |
| `list_email_stage_templates()` | `GET /stages/email/templates/` | |
| **Stages — Redirect** | | |
| `list_redirect_stages()` | `GET /stages/redirect/` | |
| `show_redirect_stage(id)` | `GET /stages/redirect/{id}/` | |
| **Stages — Source** | | |
| `list_source_stages()` | `GET /stages/source/` | |
| `show_source_stage(id)` | `GET /stages/source/{id}/` | |
| **Stages — mTLS** | | |
| `list_mtls_stages()` | `GET /stages/mtls/` | |
| `show_mtls_stage(id)` | `GET /stages/mtls/{id}/` | |
| **Stages — Endpoint** | | |
| `list_endpoint_stages()` | `GET /stages/endpoints/` | |
| `show_endpoint_stage(id)` | `GET /stages/endpoints/{id}/` | |
| **Stages — Invitation** | | |
| `list_invitation_stages()` | `GET /stages/invitation/stages/` | |
| `show_invitation_stage(id)` | `GET /stages/invitation/stages/{id}/` | |
| `list_invitations()` | `GET /stages/invitation/invitations/` | |
| `show_invitation(id)` | `GET /stages/invitation/invitations/{id}/` | |
| **Stages — Prompt** | | |
| `list_prompt_stages()` | `GET /stages/prompt/stages/` | |
| `show_prompt_stage(id)` | `GET /stages/prompt/stages/{id}/` | |
| `list_prompts()` | `GET /stages/prompt/prompts/` | |
| `show_prompt(id)` | `GET /stages/prompt/prompts/{id}/` | |
| **Sources — All** | | |
| `list_sources()` | `GET /sources/all/` | |
| `show_source(slug)` | `GET /sources/all/{slug}/` | |
| `list_source_types()` | `GET /sources/all/types/` | |
| **Sources — LDAP** | | |
| `list_ldap_sources()` | `GET /sources/ldap/` | |
| `show_ldap_source(slug)` | `GET /sources/ldap/{slug}/` | |
| `get_ldap_sync_status(slug)` | `GET /sources/ldap/{slug}/sync_status/` | |
| **Sources — OAuth** | | |
| `list_oauth_sources()` | `GET /sources/oauth/` | |
| `show_oauth_source(slug)` | `GET /sources/oauth/{slug}/` | |
| `list_oauth_source_types()` | `GET /sources/oauth/source_types/` | |
| **Sources — SAML** | | |
| `list_saml_sources()` | `GET /sources/saml/` | |
| `show_saml_source(slug)` | `GET /sources/saml/{slug}/` | |
| `get_saml_source_metadata(slug)` | `GET /sources/saml/{slug}/metadata/` | |
| **Sources — SCIM** | | |
| `list_scim_sources()` | `GET /sources/scim/` | |
| `show_scim_source(slug)` | `GET /sources/scim/{slug}/` | |
| `get_scim_sync_status(slug)` | `GET /sources/scim/{slug}/sync_status/` | |
| **Sources — Plex** | | |
| `list_plex_sources()` | `GET /sources/plex/` | |
| `show_plex_source(slug)` | `GET /sources/plex/{slug}/` | |
| **Sources — Kerberos** | | |
| `list_kerberos_sources()` | `GET /sources/kerberos/` | |
| `show_kerberos_source(slug)` | `GET /sources/kerberos/{slug}/` | |
| `get_kerberos_sync_status(slug)` | `GET /sources/kerberos/{slug}/sync_status/` | |
| **Sources — Telegram** | | |
| `list_telegram_sources()` | `GET /sources/telegram/` | |
| `show_telegram_source(slug)` | `GET /sources/telegram/{slug}/` | |
| **Sources — Connections** | | |
| `list_user_connections()` | `GET /sources/user_connections/all/` | |
| `show_user_connection(id)` | `GET /sources/user_connections/all/{id}/` | |
| `list_group_connections()` | `GET /sources/group_connections/all/` | |
| `show_group_connection(id)` | `GET /sources/group_connections/all/{id}/` | |

### authentik_admin

| Operation | Endpoint | Notes |
|---|---|---|
| **Admin (Read)** | | |
| `list_admin_apps()` | `GET /admin/apps/` | |
| `list_admin_models()` | `GET /admin/models/` | |
| `get_admin_settings()` | `GET /admin/settings/` | |
| `get_system_info()` | `GET /admin/system/` | |
| `get_admin_version()` | `GET /admin/version/` | |
| `list_version_history()` | `GET /admin/version/history/` | |
| `show_version_history(id)` | `GET /admin/version/history/{id}/` | |
| `list_admin_files()` | `GET /admin/file/` | |
| **Admin (Write)** | | |
| `update_admin_settings(...)` | `PATCH /admin/settings/` | |
| `create_admin_system()` | `POST /admin/system/` | |
| `create_admin_file(...)` | `POST /admin/file/` | |
| **Authenticators — Admin (Read)** | | |
| `list_admin_authenticators()` | `GET /authenticators/admin/all/` | |
| `list_admin_duo_devices()` | `GET /authenticators/admin/duo/` | |
| `show_admin_duo_device(id)` | `GET /authenticators/admin/duo/{id}/` | |
| `list_admin_email_devices()` | `GET /authenticators/admin/email/` | |
| `show_admin_email_device(id)` | `GET /authenticators/admin/email/{id}/` | |
| `list_admin_endpoint_devices()` | `GET /authenticators/admin/endpoint/` | |
| `show_admin_endpoint_device(id)` | `GET /authenticators/admin/endpoint/{id}/` | |
| `list_admin_sms_devices()` | `GET /authenticators/admin/sms/` | |
| `show_admin_sms_device(id)` | `GET /authenticators/admin/sms/{id}/` | |
| `list_admin_static_devices()` | `GET /authenticators/admin/static/` | |
| `show_admin_static_device(id)` | `GET /authenticators/admin/static/{id}/` | |
| `list_admin_totp_devices()` | `GET /authenticators/admin/totp/` | |
| `show_admin_totp_device(id)` | `GET /authenticators/admin/totp/{id}/` | |
| `list_admin_webauthn_devices()` | `GET /authenticators/admin/webauthn/` | |
| `show_admin_webauthn_device(id)` | `GET /authenticators/admin/webauthn/{id}/` | |
| **Authenticators — Admin (Write)** | | |
| `create_admin_duo_device(...)` | `POST /authenticators/admin/duo/` | |
| `update_admin_duo_device(id, ...)` | `PATCH /authenticators/admin/duo/{id}/` | |
| `create_admin_email_device(...)` | `POST /authenticators/admin/email/` | |
| `update_admin_email_device(id, ...)` | `PATCH /authenticators/admin/email/{id}/` | |
| `create_admin_endpoint_device(...)` | `POST /authenticators/admin/endpoint/` | |
| `update_admin_endpoint_device(id, ...)` | `PATCH /authenticators/admin/endpoint/{id}/` | |
| `create_admin_sms_device(...)` | `POST /authenticators/admin/sms/` | |
| `update_admin_sms_device(id, ...)` | `PATCH /authenticators/admin/sms/{id}/` | |
| `create_admin_static_device(...)` | `POST /authenticators/admin/static/` | |
| `update_admin_static_device(id, ...)` | `PATCH /authenticators/admin/static/{id}/` | |
| `create_admin_totp_device(...)` | `POST /authenticators/admin/totp/` | |
| `update_admin_totp_device(id, ...)` | `PATCH /authenticators/admin/totp/{id}/` | |
| `create_admin_webauthn_device(...)` | `POST /authenticators/admin/webauthn/` | |
| `update_admin_webauthn_device(id, ...)` | `PATCH /authenticators/admin/webauthn/{id}/` | |
| **Lifecycle** | | |
| `create_lifecycle_iteration()` | `POST /lifecycle/iterations/` | |

### authentik_write

| Operation | Endpoint | Notes |
|---|---|---|
| **Core — Users** | | |
| `create_user(username, name, ...)` | `POST /core/users/` | |
| `update_user(id, ...)` | `PATCH /core/users/{id}/` | |
| `set_password(id, password)` | `POST /core/users/{id}/set_password/` | |
| `create_service_account(username, ...)` | `POST /core/users/service_account/` | |
| `create_recovery_link(id)` | `POST /core/users/{id}/recovery/` | |
| `send_recovery_email(id)` | `POST /core/users/{id}/recovery_email/` | |
| `export_users()` | `POST /core/users/export/` | |
| `impersonate_user(id)` | `POST /core/users/{id}/impersonate/` | |
| `impersonate_end()` | `GET /core/users/impersonate_end/` | |
| **Core — Groups** | | |
| `create_group(name, ...)` | `POST /core/groups/` | |
| `update_group(id, ...)` | `PATCH /core/groups/{id}/` | |
| `add_user_to_group(group_id, user_id)` | `POST /core/groups/{id}/add_user/` | |
| `remove_user_from_group(group_id, user_id)` | `POST /core/groups/{id}/remove_user/` | |
| **Core — Applications** | | |
| `create_application(name, slug, ...)` | `POST /core/applications/` | |
| `update_application(slug, ...)` | `PATCH /core/applications/{slug}/` | |
| `update_transactional_application(...)` | `PUT /core/transactional_applications/` | |
| **Core — Application Entitlements** | | |
| `create_app_entitlement(app, ...)` | `POST /core/application_entitlements/` | |
| `update_app_entitlement(id, ...)` | `PATCH /core/application_entitlements/{id}/` | |
| **Core — Tokens** | | |
| `create_token(identifier, ...)` | `POST /core/tokens/` | |
| `update_token(identifier, ...)` | `PATCH /core/tokens/{identifier}/` | |
| `set_token_key(identifier, key)` | `POST /core/tokens/{identifier}/set_key/` | |
| **Core — Brands** | | |
| `create_brand(domain, ...)` | `POST /core/brands/` | |
| `update_brand(id, ...)` | `PATCH /core/brands/{id}/` | |
| **Providers — OAuth2** | | |
| `create_oauth2_provider(name, ...)` | `POST /providers/oauth2/` | |
| `update_oauth2_provider(id, ...)` | `PATCH /providers/oauth2/{id}/` | |
| **Providers — LDAP** | | |
| `create_ldap_provider(name, ...)` | `POST /providers/ldap/` | |
| `update_ldap_provider(id, ...)` | `PATCH /providers/ldap/{id}/` | |
| **Providers — SAML** | | |
| `create_saml_provider(name, ...)` | `POST /providers/saml/` | |
| `update_saml_provider(id, ...)` | `PATCH /providers/saml/{id}/` | |
| `import_saml_metadata()` | `POST /providers/saml/import_metadata/` | |
| **Providers — Proxy** | | |
| `create_proxy_provider(name, ...)` | `POST /providers/proxy/` | |
| `update_proxy_provider(id, ...)` | `PATCH /providers/proxy/{id}/` | |
| **Providers — SCIM** | | |
| `create_scim_provider(name, ...)` | `POST /providers/scim/` | |
| `update_scim_provider(id, ...)` | `PATCH /providers/scim/{id}/` | |
| `sync_scim_object(id, ...)` | `POST /providers/scim/{id}/sync_object/` | |
| **Providers — Radius** | | |
| `create_radius_provider(name, ...)` | `POST /providers/radius/` | |
| `update_radius_provider(id, ...)` | `PATCH /providers/radius/{id}/` | |
| **Providers — RAC** | | |
| `create_rac_provider(name, ...)` | `POST /providers/rac/` | |
| `update_rac_provider(id, ...)` | `PATCH /providers/rac/{id}/` | |
| **Providers — Google Workspace** | | |
| `create_google_workspace_provider(name, ...)` | `POST /providers/google_workspace/` | |
| `update_google_workspace_provider(id, ...)` | `PATCH /providers/google_workspace/{id}/` | |
| `sync_google_workspace_object(id, ...)` | `POST /providers/google_workspace/{id}/sync_object/` | |
| **Providers — Microsoft Entra** | | |
| `create_microsoft_entra_provider(name, ...)` | `POST /providers/microsoft_entra/` | |
| `update_microsoft_entra_provider(id, ...)` | `PATCH /providers/microsoft_entra/{id}/` | |
| `sync_microsoft_entra_object(id, ...)` | `POST /providers/microsoft_entra/{id}/sync_object/` | |
| **Providers — WS-Fed** | | |
| `create_wsfed_provider(name, ...)` | `POST /providers/wsfed/` | |
| `update_wsfed_provider(id, ...)` | `PATCH /providers/wsfed/{id}/` | |
| **Providers — SSF** | | |
| `create_ssf_provider(name, ...)` | `POST /providers/ssf/` | |
| `update_ssf_provider(id, ...)` | `PATCH /providers/ssf/{id}/` | |
| **Outposts** | | |
| `create_outpost(name, type, ...)` | `POST /outposts/instances/` | |
| `update_outpost(id, ...)` | `PATCH /outposts/instances/{id}/` | |
| `create_docker_service_connection(name, ...)` | `POST /outposts/service_connections/docker/` | |
| `update_docker_service_connection(id, ...)` | `PATCH /outposts/service_connections/docker/{id}/` | |
| `create_kubernetes_service_connection(name, ...)` | `POST /outposts/service_connections/kubernetes/` | |
| `update_kubernetes_service_connection(id, ...)` | `PATCH /outposts/service_connections/kubernetes/{id}/` | |
| **Crypto** | | |
| `create_certificate(name, ...)` | `POST /crypto/certificatekeypairs/` | |
| `update_certificate(id, ...)` | `PATCH /crypto/certificatekeypairs/{id}/` | |
| `generate_certificate(name, ...)` | `POST /crypto/certificatekeypairs/generate/` | |
| **RBAC** | | |
| `create_role(name)` | `POST /rbac/roles/` | |
| `update_role(id, ...)` | `PATCH /rbac/roles/{id}/` | |
| `add_user_to_role(role_id, user_id)` | `POST /rbac/roles/{id}/add_user/` | |
| `remove_user_from_role(role_id, user_id)` | `POST /rbac/roles/{id}/remove_user/` | |
| `create_initial_permission(...)` | `POST /rbac/initial_permissions/` | |
| `update_initial_permission(id, ...)` | `PATCH /rbac/initial_permissions/{id}/` | |
| `assign_permissions_to_role(role, ...)` | `POST /rbac/permissions/assigned_by_roles/assign/` | |
| `unassign_permissions_from_role(role, ...)` | `PATCH /rbac/permissions/assigned_by_roles/unassign/` | |
| **Property Mappings** | | |
| `test_property_mapping(id, ...)` | `POST /propertymappings/all/{id}/test/` | |
| `create_scope_mapping(name, ...)` | `POST /propertymappings/provider/scope/` | |
| `update_scope_mapping(id, ...)` | `PATCH /propertymappings/provider/scope/{id}/` | |
| `create_saml_property_mapping(name, ...)` | `POST /propertymappings/provider/saml/` | |
| `update_saml_property_mapping(id, ...)` | `PATCH /propertymappings/provider/saml/{id}/` | |
| `create_scim_property_mapping(name, ...)` | `POST /propertymappings/provider/scim/` | |
| `update_scim_property_mapping(id, ...)` | `PATCH /propertymappings/provider/scim/{id}/` | |
| `create_radius_property_mapping(name, ...)` | `POST /propertymappings/provider/radius/` | |
| `update_radius_property_mapping(id, ...)` | `PATCH /propertymappings/provider/radius/{id}/` | |
| `create_rac_property_mapping(name, ...)` | `POST /propertymappings/provider/rac/` | |
| `update_rac_property_mapping(id, ...)` | `PATCH /propertymappings/provider/rac/{id}/` | |
| `create_google_workspace_property_mapping(name, ...)` | `POST /propertymappings/provider/google_workspace/` | |
| `update_google_workspace_property_mapping(id, ...)` | `PATCH /propertymappings/provider/google_workspace/{id}/` | |
| `create_microsoft_entra_property_mapping(name, ...)` | `POST /propertymappings/provider/microsoft_entra/` | |
| `update_microsoft_entra_property_mapping(id, ...)` | `PATCH /propertymappings/provider/microsoft_entra/{id}/` | |
| `create_notification_mapping(name, ...)` | `POST /propertymappings/notification/` | |
| `update_notification_mapping(id, ...)` | `PATCH /propertymappings/notification/{id}/` | |
| `create_ldap_source_mapping(name, ...)` | `POST /propertymappings/source/ldap/` | |
| `update_ldap_source_mapping(id, ...)` | `PATCH /propertymappings/source/ldap/{id}/` | |
| `create_oauth_source_mapping(name, ...)` | `POST /propertymappings/source/oauth/` | |
| `update_oauth_source_mapping(id, ...)` | `PATCH /propertymappings/source/oauth/{id}/` | |
| `create_saml_source_mapping(name, ...)` | `POST /propertymappings/source/saml/` | |
| `update_saml_source_mapping(id, ...)` | `PATCH /propertymappings/source/saml/{id}/` | |
| `create_scim_source_mapping(name, ...)` | `POST /propertymappings/source/scim/` | |
| `update_scim_source_mapping(id, ...)` | `PATCH /propertymappings/source/scim/{id}/` | |
| `create_kerberos_source_mapping(name, ...)` | `POST /propertymappings/source/kerberos/` | |
| `update_kerberos_source_mapping(id, ...)` | `PATCH /propertymappings/source/kerberos/{id}/` | |
| `create_plex_source_mapping(name, ...)` | `POST /propertymappings/source/plex/` | |
| `update_plex_source_mapping(id, ...)` | `PATCH /propertymappings/source/plex/{id}/` | |
| `create_telegram_source_mapping(name, ...)` | `POST /propertymappings/source/telegram/` | |
| `update_telegram_source_mapping(id, ...)` | `PATCH /propertymappings/source/telegram/{id}/` | |
| **Managed** | | |
| `create_blueprint(name, ...)` | `POST /managed/blueprints/` | |
| `update_blueprint(id, ...)` | `PATCH /managed/blueprints/{id}/` | |
| `apply_blueprint(id)` | `POST /managed/blueprints/{id}/apply/` | |
| **RAC** | | |
| `update_rac_connection_token(id, ...)` | `PATCH /rac/connection_tokens/{id}/` | |
| `create_rac_endpoint(name, ...)` | `POST /rac/endpoints/` | |
| `update_rac_endpoint(id, ...)` | `PATCH /rac/endpoints/{id}/` | |
| **Endpoints (Device Management)** | | |
| `update_endpoint_device(id, ...)` | `PATCH /endpoints/devices/{id}/` | |
| `create_agent_connector(name, ...)` | `POST /endpoints/agents/connectors/` | |
| `update_agent_connector(id, ...)` | `PATCH /endpoints/agents/connectors/{id}/` | |
| `create_agent_enrollment_token(...)` | `POST /endpoints/agents/enrollment_tokens/` | |
| `update_agent_enrollment_token(id, ...)` | `PATCH /endpoints/agents/enrollment_tokens/{id}/` | |
| `create_device_access_group(name, ...)` | `POST /endpoints/device_access_groups/` | |
| `update_device_access_group(id, ...)` | `PATCH /endpoints/device_access_groups/{id}/` | |
| `create_device_binding(...)` | `POST /endpoints/device_bindings/` | |
| `update_device_binding(id, ...)` | `PATCH /endpoints/device_bindings/{id}/` | |
| `create_fleet_connector(name, ...)` | `POST /endpoints/fleet_connectors/` | |
| `update_fleet_connector(id, ...)` | `PATCH /endpoints/fleet_connectors/{id}/` | |
| `create_google_chrome_connector(name, ...)` | `POST /endpoints/google_chrome_connectors/` | |
| `update_google_chrome_connector(id, ...)` | `PATCH /endpoints/google_chrome_connectors/{id}/` | |
| **Enterprise** | | |
| `create_license(key)` | `POST /enterprise/license/` | |
| `update_license(id, ...)` | `PATCH /enterprise/license/{id}/` | |
| **Tenants** | | |
| `create_tenant(name, ...)` | `POST /tenants/tenants/` | |
| `update_tenant(id, ...)` | `PATCH /tenants/tenants/{id}/` | |
| `create_tenant_admin_group(id)` | `POST /tenants/tenants/{id}/create_admin_group/` | |
| `create_tenant_recovery_key(id)` | `POST /tenants/tenants/{id}/create_recovery_key/` | |
| `create_tenant_domain(domain, tenant)` | `POST /tenants/domains/` | |
| `update_tenant_domain(id, ...)` | `PATCH /tenants/domains/{id}/` | |
| **Tasks** | | |
| `update_task_schedule(id, ...)` | `PATCH /tasks/schedules/{id}/` | |
| `send_task_schedule(id)` | `POST /tasks/schedules/{id}/send/` | |
| `retry_task(id)` | `POST /tasks/tasks/{id}/retry/` | |
| **Authenticators (User)** | | |
| `update_authenticator_totp(id, ...)` | `PATCH /authenticators/totp/{id}/` | |
| `update_authenticator_webauthn(id, ...)` | `PATCH /authenticators/webauthn/{id}/` | |
| `update_authenticator_duo(id, ...)` | `PATCH /authenticators/duo/{id}/` | |
| `update_authenticator_sms(id, ...)` | `PATCH /authenticators/sms/{id}/` | |
| `update_authenticator_static(id, ...)` | `PATCH /authenticators/static/{id}/` | |
| `update_authenticator_email(id, ...)` | `PATCH /authenticators/email/{id}/` | |

### authentik_flows_write

| Operation | Endpoint | Notes |
|---|---|---|
| **Flows** | | |
| `create_flow(name, slug, ...)` | `POST /flows/instances/` | |
| `update_flow(slug, ...)` | `PATCH /flows/instances/{slug}/` | |
| `import_flow()` | `POST /flows/instances/import/` | |
| `clear_flow_cache()` | `POST /flows/instances/cache_clear/` | |
| `create_flow_binding(target, stage, order)` | `POST /flows/bindings/` | |
| `update_flow_binding(id, ...)` | `PATCH /flows/bindings/{id}/` | |
| **Policies** | | |
| `test_policy(id, ...)` | `POST /policies/all/{id}/test/` | |
| `clear_policy_cache()` | `POST /policies/all/cache_clear/` | |
| `create_policy_binding(target, policy, order)` | `POST /policies/bindings/` | |
| `update_policy_binding(id, ...)` | `PATCH /policies/bindings/{id}/` | |
| `create_expression_policy(name, expression)` | `POST /policies/expression/` | |
| `update_expression_policy(id, ...)` | `PATCH /policies/expression/{id}/` | |
| `create_password_policy(name, ...)` | `POST /policies/password/` | |
| `update_password_policy(id, ...)` | `PATCH /policies/password/{id}/` | |
| `create_password_expiry_policy(name, ...)` | `POST /policies/password_expiry/` | |
| `update_password_expiry_policy(id, ...)` | `PATCH /policies/password_expiry/{id}/` | |
| `create_reputation_policy(name, ...)` | `POST /policies/reputation/` | |
| `update_reputation_policy(id, ...)` | `PATCH /policies/reputation/{id}/` | |
| `create_event_matcher_policy(name, ...)` | `POST /policies/event_matcher/` | |
| `update_event_matcher_policy(id, ...)` | `PATCH /policies/event_matcher/{id}/` | |
| `create_geoip_policy(name, ...)` | `POST /policies/geoip/` | |
| `update_geoip_policy(id, ...)` | `PATCH /policies/geoip/{id}/` | |
| `create_dummy_policy(name)` | `POST /policies/dummy/` | |
| `update_dummy_policy(id, ...)` | `PATCH /policies/dummy/{id}/` | |
| `create_unique_password_policy(name, ...)` | `POST /policies/unique_password/` | |
| `update_unique_password_policy(id, ...)` | `PATCH /policies/unique_password/{id}/` | |
| **Events** | | |
| `create_event(action, ...)` | `POST /events/events/` | |
| `update_event(id, ...)` | `PATCH /events/events/{id}/` | |
| `export_events()` | `POST /events/events/export/` | |
| `update_notification(id, ...)` | `PATCH /events/notifications/{id}/` | |
| `mark_all_notifications_seen()` | `POST /events/notifications/mark_all_seen/` | |
| `create_notification_rule(name, ...)` | `POST /events/rules/` | |
| `update_notification_rule(id, ...)` | `PATCH /events/rules/{id}/` | |
| `create_notification_transport(name, ...)` | `POST /events/transports/` | |
| `update_notification_transport(id, ...)` | `PATCH /events/transports/{id}/` | |
| `test_notification_transport(id)` | `POST /events/transports/{id}/test/` | |
| **Stages — All types** | | |
| `create_identification_stage(name, ...)` | `POST /stages/identification/` | |
| `update_identification_stage(id, ...)` | `PATCH /stages/identification/{id}/` | |
| `create_password_stage(name, ...)` | `POST /stages/password/` | |
| `update_password_stage(id, ...)` | `PATCH /stages/password/{id}/` | |
| `create_authenticator_totp_stage(name, ...)` | `POST /stages/authenticator/totp/` | |
| `update_authenticator_totp_stage(id, ...)` | `PATCH /stages/authenticator/totp/{id}/` | |
| `create_authenticator_webauthn_stage(name, ...)` | `POST /stages/authenticator/webauthn/` | |
| `update_authenticator_webauthn_stage(id, ...)` | `PATCH /stages/authenticator/webauthn/{id}/` | |
| `create_authenticator_duo_stage(name, ...)` | `POST /stages/authenticator/duo/` | |
| `update_authenticator_duo_stage(id, ...)` | `PATCH /stages/authenticator/duo/{id}/` | |
| `import_duo_device_manual(stage_id, ...)` | `POST /stages/authenticator/duo/{id}/import_device_manual/` | |
| `import_duo_devices_automatic(stage_id)` | `POST /stages/authenticator/duo/{id}/import_devices_automatic/` | |
| `check_duo_enrollment_status(stage_id)` | `POST /stages/authenticator/duo/{id}/enrollment_status/` | |
| `create_authenticator_sms_stage(name, ...)` | `POST /stages/authenticator/sms/` | |
| `update_authenticator_sms_stage(id, ...)` | `PATCH /stages/authenticator/sms/{id}/` | |
| `create_authenticator_email_stage(name, ...)` | `POST /stages/authenticator/email/` | |
| `update_authenticator_email_stage(id, ...)` | `PATCH /stages/authenticator/email/{id}/` | |
| `create_authenticator_static_stage(name, ...)` | `POST /stages/authenticator/static/` | |
| `update_authenticator_static_stage(id, ...)` | `PATCH /stages/authenticator/static/{id}/` | |
| `create_authenticator_validate_stage(name, ...)` | `POST /stages/authenticator/validate/` | |
| `update_authenticator_validate_stage(id, ...)` | `PATCH /stages/authenticator/validate/{id}/` | |
| `create_authenticator_endpoint_gdtc_stage(name, ...)` | `POST /stages/authenticator/endpoint_gdtc/` | |
| `update_authenticator_endpoint_gdtc_stage(id, ...)` | `PATCH /stages/authenticator/endpoint_gdtc/{id}/` | |
| `create_user_login_stage(name, ...)` | `POST /stages/user_login/` | |
| `update_user_login_stage(id, ...)` | `PATCH /stages/user_login/{id}/` | |
| `create_user_logout_stage(name, ...)` | `POST /stages/user_logout/` | |
| `update_user_logout_stage(id, ...)` | `PATCH /stages/user_logout/{id}/` | |
| `create_user_write_stage(name, ...)` | `POST /stages/user_write/` | |
| `update_user_write_stage(id, ...)` | `PATCH /stages/user_write/{id}/` | |
| `create_user_delete_stage(name, ...)` | `POST /stages/user_delete/` | |
| `update_user_delete_stage(id, ...)` | `PATCH /stages/user_delete/{id}/` | |
| `create_consent_stage(name, ...)` | `POST /stages/consent/` | |
| `update_consent_stage(id, ...)` | `PATCH /stages/consent/{id}/` | |
| `create_captcha_stage(name, ...)` | `POST /stages/captcha/` | |
| `update_captcha_stage(id, ...)` | `PATCH /stages/captcha/{id}/` | |
| `create_deny_stage(name, ...)` | `POST /stages/deny/` | |
| `update_deny_stage(id, ...)` | `PATCH /stages/deny/{id}/` | |
| `create_dummy_stage(name, ...)` | `POST /stages/dummy/` | |
| `update_dummy_stage(id, ...)` | `PATCH /stages/dummy/{id}/` | |
| `create_email_stage(name, ...)` | `POST /stages/email/` | |
| `update_email_stage(id, ...)` | `PATCH /stages/email/{id}/` | |
| `create_redirect_stage(name, ...)` | `POST /stages/redirect/` | |
| `update_redirect_stage(id, ...)` | `PATCH /stages/redirect/{id}/` | |
| `create_source_stage(name, ...)` | `POST /stages/source/` | |
| `update_source_stage(id, ...)` | `PATCH /stages/source/{id}/` | |
| `create_mtls_stage(name, ...)` | `POST /stages/mtls/` | |
| `update_mtls_stage(id, ...)` | `PATCH /stages/mtls/{id}/` | |
| `create_endpoint_stage(name, ...)` | `POST /stages/endpoints/` | |
| `update_endpoint_stage(id, ...)` | `PATCH /stages/endpoints/{id}/` | |
| `create_invitation_stage(name, ...)` | `POST /stages/invitation/stages/` | |
| `update_invitation_stage(id, ...)` | `PATCH /stages/invitation/stages/{id}/` | |
| `create_invitation(...)` | `POST /stages/invitation/invitations/` | |
| `update_invitation(id, ...)` | `PATCH /stages/invitation/invitations/{id}/` | |
| `send_invitation_email(id)` | `POST /stages/invitation/invitations/{id}/send_email/` | |
| `create_prompt_stage(name, ...)` | `POST /stages/prompt/stages/` | |
| `update_prompt_stage(id, ...)` | `PATCH /stages/prompt/stages/{id}/` | |
| `create_prompt(name, ...)` | `POST /stages/prompt/prompts/` | |
| `update_prompt(id, ...)` | `PATCH /stages/prompt/prompts/{id}/` | |
| `preview_prompt(...)` | `POST /stages/prompt/prompts/preview/` | |
| **Sources — LDAP** | | |
| `create_ldap_source(name, ...)` | `POST /sources/ldap/` | |
| `update_ldap_source(slug, ...)` | `PATCH /sources/ldap/{slug}/` | |
| **Sources — OAuth** | | |
| `create_oauth_source(name, ...)` | `POST /sources/oauth/` | |
| `update_oauth_source(slug, ...)` | `PATCH /sources/oauth/{slug}/` | |
| **Sources — SAML** | | |
| `create_saml_source(name, ...)` | `POST /sources/saml/` | |
| `update_saml_source(slug, ...)` | `PATCH /sources/saml/{slug}/` | |
| **Sources — SCIM** | | |
| `create_scim_source(name, ...)` | `POST /sources/scim/` | |
| `update_scim_source(slug, ...)` | `PATCH /sources/scim/{slug}/` | |
| **Sources — Plex** | | |
| `create_plex_source(name, ...)` | `POST /sources/plex/` | |
| `update_plex_source(slug, ...)` | `PATCH /sources/plex/{slug}/` | |
| `redeem_plex_token(slug)` | `POST /sources/plex/{slug}/redeem_token/` | |
| `redeem_plex_token_authenticated(slug)` | `POST /sources/plex/{slug}/redeem_token_authenticated/` | |
| **Sources — Kerberos** | | |
| `create_kerberos_source(name, ...)` | `POST /sources/kerberos/` | |
| `update_kerberos_source(slug, ...)` | `PATCH /sources/kerberos/{slug}/` | |
| **Sources — Telegram** | | |
| `create_telegram_source(name, ...)` | `POST /sources/telegram/` | |
| `update_telegram_source(slug, ...)` | `PATCH /sources/telegram/{slug}/` | |
| `connect_telegram_user(slug)` | `POST /sources/telegram/{slug}/connect_user/` | |
| **Sources — Connections** | | |
| `update_user_connection(id, ...)` | `PATCH /sources/user_connections/all/{id}/` | |
| `update_group_connection(id, ...)` | `PATCH /sources/group_connections/all/{id}/` | |

### authentik_delete

| Operation | Endpoint | Notes |
|---|---|---|
| **Core** | | |
| `delete_user(id)` | `DELETE /core/users/{id}/` | |
| `delete_group(id)` | `DELETE /core/groups/{id}/` | |
| `delete_application(slug)` | `DELETE /core/applications/{slug}/` | |
| `delete_app_entitlement(id)` | `DELETE /core/application_entitlements/{id}/` | |
| `delete_token(identifier)` | `DELETE /core/tokens/{identifier}/` | |
| `delete_brand(id)` | `DELETE /core/brands/{id}/` | |
| `delete_session(id)` | `DELETE /core/authenticated_sessions/{id}/` | |
| `bulk_delete_sessions()` | `DELETE /core/authenticated_sessions/bulk_delete/` | |
| `delete_user_consent(id)` | `DELETE /core/user_consent/{id}/` | |
| **Providers** | | |
| `delete_provider(id)` | `DELETE /providers/all/{id}/` | |
| `delete_oauth2_provider(id)` | `DELETE /providers/oauth2/{id}/` | |
| `delete_ldap_provider(id)` | `DELETE /providers/ldap/{id}/` | |
| `delete_saml_provider(id)` | `DELETE /providers/saml/{id}/` | |
| `delete_proxy_provider(id)` | `DELETE /providers/proxy/{id}/` | |
| `delete_scim_provider(id)` | `DELETE /providers/scim/{id}/` | |
| `delete_radius_provider(id)` | `DELETE /providers/radius/{id}/` | |
| `delete_rac_provider(id)` | `DELETE /providers/rac/{id}/` | |
| `delete_google_workspace_provider(id)` | `DELETE /providers/google_workspace/{id}/` | |
| `delete_microsoft_entra_provider(id)` | `DELETE /providers/microsoft_entra/{id}/` | |
| `delete_wsfed_provider(id)` | `DELETE /providers/wsfed/{id}/` | |
| `delete_ssf_provider(id)` | `DELETE /providers/ssf/{id}/` | |
| **Flows** | | |
| `delete_flow(slug)` | `DELETE /flows/instances/{slug}/` | |
| `delete_flow_binding(id)` | `DELETE /flows/bindings/{id}/` | |
| **Outposts** | | |
| `delete_outpost(id)` | `DELETE /outposts/instances/{id}/` | |
| `delete_service_connection(id)` | `DELETE /outposts/service_connections/all/{id}/` | |
| `delete_docker_service_connection(id)` | `DELETE /outposts/service_connections/docker/{id}/` | |
| `delete_kubernetes_service_connection(id)` | `DELETE /outposts/service_connections/kubernetes/{id}/` | |
| **Policies** | | |
| `delete_policy(id)` | `DELETE /policies/all/{id}/` | |
| `delete_policy_binding(id)` | `DELETE /policies/bindings/{id}/` | |
| `delete_expression_policy(id)` | `DELETE /policies/expression/{id}/` | |
| `delete_password_policy(id)` | `DELETE /policies/password/{id}/` | |
| `delete_password_expiry_policy(id)` | `DELETE /policies/password_expiry/{id}/` | |
| `delete_reputation_policy(id)` | `DELETE /policies/reputation/{id}/` | |
| `delete_reputation_score(id)` | `DELETE /policies/reputation/scores/{id}/` | |
| `delete_event_matcher_policy(id)` | `DELETE /policies/event_matcher/{id}/` | |
| `delete_geoip_policy(id)` | `DELETE /policies/geoip/{id}/` | |
| `delete_dummy_policy(id)` | `DELETE /policies/dummy/{id}/` | |
| `delete_unique_password_policy(id)` | `DELETE /policies/unique_password/{id}/` | |
| **Events** | | |
| `delete_event(id)` | `DELETE /events/events/{id}/` | |
| `delete_notification(id)` | `DELETE /events/notifications/{id}/` | |
| `delete_notification_rule(id)` | `DELETE /events/rules/{id}/` | |
| `delete_notification_transport(id)` | `DELETE /events/transports/{id}/` | |
| **Stages** | | |
| `delete_stage(id)` | `DELETE /stages/all/{id}/` | |
| `delete_identification_stage(id)` | `DELETE /stages/identification/{id}/` | |
| `delete_password_stage(id)` | `DELETE /stages/password/{id}/` | |
| `delete_authenticator_totp_stage(id)` | `DELETE /stages/authenticator/totp/{id}/` | |
| `delete_authenticator_webauthn_stage(id)` | `DELETE /stages/authenticator/webauthn/{id}/` | |
| `delete_authenticator_duo_stage(id)` | `DELETE /stages/authenticator/duo/{id}/` | |
| `delete_authenticator_sms_stage(id)` | `DELETE /stages/authenticator/sms/{id}/` | |
| `delete_authenticator_email_stage(id)` | `DELETE /stages/authenticator/email/{id}/` | |
| `delete_authenticator_static_stage(id)` | `DELETE /stages/authenticator/static/{id}/` | |
| `delete_authenticator_validate_stage(id)` | `DELETE /stages/authenticator/validate/{id}/` | |
| `delete_authenticator_endpoint_gdtc_stage(id)` | `DELETE /stages/authenticator/endpoint_gdtc/{id}/` | |
| `delete_user_login_stage(id)` | `DELETE /stages/user_login/{id}/` | |
| `delete_user_logout_stage(id)` | `DELETE /stages/user_logout/{id}/` | |
| `delete_user_write_stage(id)` | `DELETE /stages/user_write/{id}/` | |
| `delete_user_delete_stage(id)` | `DELETE /stages/user_delete/{id}/` | |
| `delete_consent_stage(id)` | `DELETE /stages/consent/{id}/` | |
| `delete_captcha_stage(id)` | `DELETE /stages/captcha/{id}/` | |
| `delete_deny_stage(id)` | `DELETE /stages/deny/{id}/` | |
| `delete_dummy_stage(id)` | `DELETE /stages/dummy/{id}/` | |
| `delete_email_stage(id)` | `DELETE /stages/email/{id}/` | |
| `delete_redirect_stage(id)` | `DELETE /stages/redirect/{id}/` | |
| `delete_source_stage(id)` | `DELETE /stages/source/{id}/` | |
| `delete_mtls_stage(id)` | `DELETE /stages/mtls/{id}/` | |
| `delete_endpoint_stage(id)` | `DELETE /stages/endpoints/{id}/` | |
| `delete_invitation_stage(id)` | `DELETE /stages/invitation/stages/{id}/` | |
| `delete_invitation(id)` | `DELETE /stages/invitation/invitations/{id}/` | |
| `delete_prompt_stage(id)` | `DELETE /stages/prompt/stages/{id}/` | |
| `delete_prompt(id)` | `DELETE /stages/prompt/prompts/{id}/` | |
| **Sources** | | |
| `delete_source(slug)` | `DELETE /sources/all/{slug}/` | |
| `delete_ldap_source(slug)` | `DELETE /sources/ldap/{slug}/` | |
| `delete_oauth_source(slug)` | `DELETE /sources/oauth/{slug}/` | |
| `delete_saml_source(slug)` | `DELETE /sources/saml/{slug}/` | |
| `delete_scim_source(slug)` | `DELETE /sources/scim/{slug}/` | |
| `delete_plex_source(slug)` | `DELETE /sources/plex/{slug}/` | |
| `delete_kerberos_source(slug)` | `DELETE /sources/kerberos/{slug}/` | |
| `delete_telegram_source(slug)` | `DELETE /sources/telegram/{slug}/` | |
| `delete_user_connection(id)` | `DELETE /sources/user_connections/all/{id}/` | |
| `delete_group_connection(id)` | `DELETE /sources/group_connections/all/{id}/` | |
| **Crypto** | | |
| `delete_certificate(id)` | `DELETE /crypto/certificatekeypairs/{id}/` | |
| **RBAC** | | |
| `delete_role(id)` | `DELETE /rbac/roles/{id}/` | |
| `delete_initial_permission(id)` | `DELETE /rbac/initial_permissions/{id}/` | |
| **Property Mappings** | | |
| `delete_property_mapping(id)` | `DELETE /propertymappings/all/{id}/` | |
| `delete_scope_mapping(id)` | `DELETE /propertymappings/provider/scope/{id}/` | |
| `delete_saml_property_mapping(id)` | `DELETE /propertymappings/provider/saml/{id}/` | |
| `delete_scim_property_mapping(id)` | `DELETE /propertymappings/provider/scim/{id}/` | |
| `delete_radius_property_mapping(id)` | `DELETE /propertymappings/provider/radius/{id}/` | |
| `delete_rac_property_mapping(id)` | `DELETE /propertymappings/provider/rac/{id}/` | |
| `delete_google_workspace_property_mapping(id)` | `DELETE /propertymappings/provider/google_workspace/{id}/` | |
| `delete_microsoft_entra_property_mapping(id)` | `DELETE /propertymappings/provider/microsoft_entra/{id}/` | |
| `delete_notification_mapping(id)` | `DELETE /propertymappings/notification/{id}/` | |
| `delete_ldap_source_mapping(id)` | `DELETE /propertymappings/source/ldap/{id}/` | |
| `delete_oauth_source_mapping(id)` | `DELETE /propertymappings/source/oauth/{id}/` | |
| `delete_saml_source_mapping(id)` | `DELETE /propertymappings/source/saml/{id}/` | |
| `delete_scim_source_mapping(id)` | `DELETE /propertymappings/source/scim/{id}/` | |
| `delete_kerberos_source_mapping(id)` | `DELETE /propertymappings/source/kerberos/{id}/` | |
| `delete_plex_source_mapping(id)` | `DELETE /propertymappings/source/plex/{id}/` | |
| `delete_telegram_source_mapping(id)` | `DELETE /propertymappings/source/telegram/{id}/` | |
| **Managed** | | |
| `delete_blueprint(id)` | `DELETE /managed/blueprints/{id}/` | |
| **OAuth2 Tokens** | | |
| `delete_oauth2_access_token(id)` | `DELETE /oauth2/access_tokens/{id}/` | |
| `delete_oauth2_authorization_code(id)` | `DELETE /oauth2/authorization_codes/{id}/` | |
| `delete_oauth2_refresh_token(id)` | `DELETE /oauth2/refresh_tokens/{id}/` | |
| **RAC** | | |
| `delete_rac_connection_token(id)` | `DELETE /rac/connection_tokens/{id}/` | |
| `delete_rac_endpoint(id)` | `DELETE /rac/endpoints/{id}/` | |
| **Endpoints (Device Management)** | | |
| `delete_endpoint_connector(id)` | `DELETE /endpoints/connectors/{id}/` | |
| `delete_agent_connector(id)` | `DELETE /endpoints/agents/connectors/{id}/` | |
| `delete_agent_enrollment_token(id)` | `DELETE /endpoints/agents/enrollment_tokens/{id}/` | |
| `delete_endpoint_device(id)` | `DELETE /endpoints/devices/{id}/` | |
| `delete_device_access_group(id)` | `DELETE /endpoints/device_access_groups/{id}/` | |
| `delete_device_binding(id)` | `DELETE /endpoints/device_bindings/{id}/` | |
| `delete_fleet_connector(id)` | `DELETE /endpoints/fleet_connectors/{id}/` | |
| `delete_google_chrome_connector(id)` | `DELETE /endpoints/google_chrome_connectors/{id}/` | |
| **Enterprise** | | |
| `delete_license(id)` | `DELETE /enterprise/license/{id}/` | |
| **Tenants** | | |
| `delete_tenant(id)` | `DELETE /tenants/tenants/{id}/` | |
| `delete_tenant_domain(id)` | `DELETE /tenants/domains/{id}/` | |
| **Admin** | | |
| `delete_admin_file(id)` | `DELETE /admin/file/{id}/` | |
| **Authenticators** | | |
| `delete_authenticator_totp(id)` | `DELETE /authenticators/totp/{id}/` | |
| `delete_authenticator_webauthn(id)` | `DELETE /authenticators/webauthn/{id}/` | |
| `delete_authenticator_duo(id)` | `DELETE /authenticators/duo/{id}/` | |
| `delete_authenticator_sms(id)` | `DELETE /authenticators/sms/{id}/` | |
| `delete_authenticator_static(id)` | `DELETE /authenticators/static/{id}/` | |
| `delete_authenticator_email(id)` | `DELETE /authenticators/email/{id}/` | |
| `delete_admin_duo_device(id)` | `DELETE /authenticators/admin/duo/{id}/` | |
| `delete_admin_email_device(id)` | `DELETE /authenticators/admin/email/{id}/` | |
| `delete_admin_endpoint_device(id)` | `DELETE /authenticators/admin/endpoint/{id}/` | |
| `delete_admin_sms_device(id)` | `DELETE /authenticators/admin/sms/{id}/` | |
| `delete_admin_static_device(id)` | `DELETE /authenticators/admin/static/{id}/` | |
| `delete_admin_totp_device(id)` | `DELETE /authenticators/admin/totp/{id}/` | |
| `delete_admin_webauthn_device(id)` | `DELETE /authenticators/admin/webauthn/{id}/` | |
| **Reports** | | |
| `delete_export(id)` | `DELETE /reports/exports/{id}/` | |

## Slim fields

All list operations use `slim_fields` to reduce response size. Full objects via `show_*`.

```python
# Core
SLIM_USER = {"pk", "username", "name", "email", "is_active", "path", "last_login"}
SLIM_GROUP = {"pk", "name", "parent_name", "num_pk", "is_superuser"}
SLIM_APP = {"pk", "name", "slug", "provider", "provider_obj.name", "meta_launch_url"}
SLIM_TOKEN = {"pk", "identifier", "intent", "user", "description", "expiring", "expires"}
SLIM_SESSION = {"uuid", "user", "last_ip", "last_used", "expires", "geo_ip.country", "geo_ip.city"}
SLIM_BRAND = {"brand_uuid", "domain", "default", "branding_title"}
SLIM_USER_CONSENT = {"pk", "user.pk", "user.username", "application.slug", "application.name", "expires", "permissions"}
SLIM_APP_ENTITLEMENT = {"pbm_uuid", "name", "app"}

# Flows
SLIM_FLOW = {"pk", "name", "slug", "title", "designation"}
SLIM_FLOW_BINDING = {"pk", "target", "stage", "order", "evaluate_on_plan", "re_evaluate_policies"}

# Policies
SLIM_POLICY = {"pk", "name", "component", "execution_logging", "bound_to"}
SLIM_POLICY_BINDING = {"pk", "policy", "group", "user", "target", "negate", "enabled", "order", "timeout"}
SLIM_REPUTATION_SCORE = {"pk", "identifier", "ip", "score", "updated"}

# Stages
SLIM_STAGE = {"pk", "name", "component", "verbose_name"}

# Sources
SLIM_SOURCE = {"pk", "name", "slug", "enabled", "component", "verbose_name"}
SLIM_SOURCE_CONNECTION = {"pk", "source", "identifier"}

# Providers
SLIM_PROVIDER = {"pk", "name", "component", "authorization_flow", "assigned_application_slug", "assigned_application_name"}

# Property mappings
SLIM_PROPERTY_MAPPING = {"pk", "name", "managed", "component", "verbose_name"}

# Events
SLIM_EVENT = {"pk", "action", "app", "user", "created"}
SLIM_NOTIFICATION = {"pk", "severity", "body", "created", "seen"}
SLIM_NOTIFICATION_RULE = {"pk", "name", "transports", "severity", "destination_group"}
SLIM_NOTIFICATION_TRANSPORT = {"pk", "name", "mode"}

# Crypto, Outposts, RBAC, Authenticators, OAuth2, Managed, Tasks, etc.
SLIM_CERTIFICATE = {"pk", "name", "fingerprint_sha256", "cert_expiry", "managed"}
SLIM_OUTPOST = {"pk", "name", "type", "providers", "service_connection", "managed"}
SLIM_SERVICE_CONNECTION = {"pk", "name", "component", "local"}
SLIM_ROLE = {"pk", "name"}
SLIM_PERMISSION = {"id", "name", "codename", "model", "app_label"}
SLIM_AUTHENTICATOR_DEVICE = {"pk", "name", "user.pk", "user.username"}
SLIM_OAUTH2_TOKEN = {"pk", "provider.pk", "provider.name", "user.pk", "user.username", "is_expired", "expires", "scope", "revoked"}
SLIM_BLUEPRINT = {"pk", "name", "path", "enabled", "status"}
SLIM_TASK = {"uid", "state", "description", "mtime"}
SLIM_LICENSE = {"pk", "name", "expiry", "internal_users", "external_users"}
SLIM_TENANT = {"pk", "name", "schema_name", "ready"}
SLIM_TENANT_DOMAIN = {"pk", "domain", "is_primary", "tenant"}
SLIM_RAC_ENDPOINT = {"pk", "name", "protocol", "host", "provider"}
SLIM_RAC_TOKEN = {"pk", "provider", "endpoint", "user"}
SLIM_ENDPOINT = {"pk", "name"}
SLIM_EXPORT = {"pk", "name", "created"}
SLIM_SSF_STREAM = {"pk", "provider", "delivery_method", "endpoint_url"}
SLIM_VERSION_HISTORY = {"pk", "version", "build", "created"}
SLIM_ADMIN_FILE = {"pk", "name", "path"}
```

## Out of scope

- **Flow executor** — interactive multi-step, not suitable for MCP
- `used_by_list` endpoints — meta, low value

## Deploy checklist

- [ ] CI/CD workflow (`.github/workflows/build.yml`)
- [ ] GitHub: enable Pages in repo settings (source: GitHub Actions) — `gh api repos/OWNER/REPO/pages -X POST -f build_type=workflow`
- [ ] GitHub: `docs/index.html` setup page (API key input → config JSON generator)
- [ ] First push to `main` triggers build → tag v1.0.0 → release with wheel → PEP 503 index
- [ ] Verify install: `uvx --extra-index-url INDEX_URL authentik-mcp`
