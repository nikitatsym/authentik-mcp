from ..registry import _op
from .groups import authentik_flows_write
from .helpers import _get_client, _ok

# ── Stages — Identification ──────────────────────────────────────────


@_op(authentik_flows_write)
def create_identification_stage(name: str, **kwargs):
    """Create an identification stage. Required: name."""
    return _ok(_get_client().post("/stages/identification/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_identification_stage(id: str, **kwargs):
    """Update an identification stage."""
    return _ok(_get_client().patch(f"/stages/identification/{id}/", json=kwargs))


# ── Stages — Password ────────────────────────────────────────────────


@_op(authentik_flows_write)
def create_password_stage(name: str, **kwargs):
    """Create a password stage. Required: name."""
    return _ok(_get_client().post("/stages/password/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_password_stage(id: str, **kwargs):
    """Update a password stage."""
    return _ok(_get_client().patch(f"/stages/password/{id}/", json=kwargs))


# ── Stages — Authenticator ───────────────────────────────────────────


@_op(authentik_flows_write)
def create_authenticator_totp_stage(name: str, **kwargs):
    """Create a TOTP authenticator stage. Required: name."""
    return _ok(_get_client().post("/stages/authenticator/totp/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_authenticator_totp_stage(id: str, **kwargs):
    """Update a TOTP authenticator stage."""
    return _ok(_get_client().patch(f"/stages/authenticator/totp/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_authenticator_webauthn_stage(name: str, **kwargs):
    """Create a WebAuthn authenticator stage. Required: name."""
    return _ok(_get_client().post("/stages/authenticator/webauthn/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_authenticator_webauthn_stage(id: str, **kwargs):
    """Update a WebAuthn authenticator stage."""
    return _ok(_get_client().patch(f"/stages/authenticator/webauthn/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_authenticator_duo_stage(name: str, **kwargs):
    """Create a Duo authenticator stage. Required: name."""
    return _ok(_get_client().post("/stages/authenticator/duo/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_authenticator_duo_stage(id: str, **kwargs):
    """Update a Duo authenticator stage."""
    return _ok(_get_client().patch(f"/stages/authenticator/duo/{id}/", json=kwargs))


@_op(authentik_flows_write)
def import_duo_device_manual(stage_id: str, **kwargs):
    """Import a Duo device manually."""
    return _ok(_get_client().post(f"/stages/authenticator/duo/{stage_id}/import_device_manual/", json=kwargs))


@_op(authentik_flows_write)
def import_duo_devices_automatic(stage_id: str):
    """Import Duo devices automatically."""
    return _ok(_get_client().post(f"/stages/authenticator/duo/{stage_id}/import_devices_automatic/"))


@_op(authentik_flows_write)
def check_duo_enrollment_status(stage_id: str):
    """Check Duo enrollment status."""
    return _ok(_get_client().post(f"/stages/authenticator/duo/{stage_id}/enrollment_status/"))


@_op(authentik_flows_write)
def create_authenticator_sms_stage(name: str, **kwargs):
    """Create an SMS authenticator stage. Required: name."""
    return _ok(_get_client().post("/stages/authenticator/sms/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_authenticator_sms_stage(id: str, **kwargs):
    """Update an SMS authenticator stage."""
    return _ok(_get_client().patch(f"/stages/authenticator/sms/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_authenticator_email_stage(name: str, **kwargs):
    """Create an email authenticator stage. Required: name."""
    return _ok(_get_client().post("/stages/authenticator/email/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_authenticator_email_stage(id: str, **kwargs):
    """Update an email authenticator stage."""
    return _ok(_get_client().patch(f"/stages/authenticator/email/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_authenticator_static_stage(name: str, **kwargs):
    """Create a static authenticator stage. Required: name."""
    return _ok(_get_client().post("/stages/authenticator/static/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_authenticator_static_stage(id: str, **kwargs):
    """Update a static authenticator stage."""
    return _ok(_get_client().patch(f"/stages/authenticator/static/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_authenticator_validate_stage(name: str, **kwargs):
    """Create an authenticator validate stage. Required: name."""
    return _ok(_get_client().post("/stages/authenticator/validate/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_authenticator_validate_stage(id: str, **kwargs):
    """Update an authenticator validate stage."""
    return _ok(_get_client().patch(f"/stages/authenticator/validate/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_authenticator_endpoint_gdtc_stage(name: str, **kwargs):
    """Create an endpoint GDTC authenticator stage. Required: name."""
    return _ok(_get_client().post("/stages/authenticator/endpoint_gdtc/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_authenticator_endpoint_gdtc_stage(id: str, **kwargs):
    """Update an endpoint GDTC authenticator stage."""
    return _ok(_get_client().patch(f"/stages/authenticator/endpoint_gdtc/{id}/", json=kwargs))


# ── Stages — User ────────────────────────────────────────────────────


@_op(authentik_flows_write)
def create_user_login_stage(name: str, **kwargs):
    """Create a user login stage. Required: name."""
    return _ok(_get_client().post("/stages/user_login/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_user_login_stage(id: str, **kwargs):
    """Update a user login stage."""
    return _ok(_get_client().patch(f"/stages/user_login/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_user_logout_stage(name: str, **kwargs):
    """Create a user logout stage. Required: name."""
    return _ok(_get_client().post("/stages/user_logout/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_user_logout_stage(id: str, **kwargs):
    """Update a user logout stage."""
    return _ok(_get_client().patch(f"/stages/user_logout/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_user_write_stage(name: str, **kwargs):
    """Create a user write stage. Required: name."""
    return _ok(_get_client().post("/stages/user_write/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_user_write_stage(id: str, **kwargs):
    """Update a user write stage."""
    return _ok(_get_client().patch(f"/stages/user_write/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_user_delete_stage(name: str, **kwargs):
    """Create a user delete stage. Required: name."""
    return _ok(_get_client().post("/stages/user_delete/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_user_delete_stage(id: str, **kwargs):
    """Update a user delete stage."""
    return _ok(_get_client().patch(f"/stages/user_delete/{id}/", json=kwargs))


# ── Stages — Other ───────────────────────────────────────────────────


@_op(authentik_flows_write)
def create_consent_stage(name: str, **kwargs):
    """Create a consent stage. Required: name."""
    return _ok(_get_client().post("/stages/consent/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_consent_stage(id: str, **kwargs):
    """Update a consent stage."""
    return _ok(_get_client().patch(f"/stages/consent/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_captcha_stage(name: str, **kwargs):
    """Create a captcha stage. Required: name."""
    return _ok(_get_client().post("/stages/captcha/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_captcha_stage(id: str, **kwargs):
    """Update a captcha stage."""
    return _ok(_get_client().patch(f"/stages/captcha/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_deny_stage(name: str, **kwargs):
    """Create a deny stage. Required: name."""
    return _ok(_get_client().post("/stages/deny/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_deny_stage(id: str, **kwargs):
    """Update a deny stage."""
    return _ok(_get_client().patch(f"/stages/deny/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_dummy_stage(name: str, **kwargs):
    """Create a dummy stage. Required: name."""
    return _ok(_get_client().post("/stages/dummy/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_dummy_stage(id: str, **kwargs):
    """Update a dummy stage."""
    return _ok(_get_client().patch(f"/stages/dummy/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_email_stage(name: str, **kwargs):
    """Create an email stage. Required: name."""
    return _ok(_get_client().post("/stages/email/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_email_stage(id: str, **kwargs):
    """Update an email stage."""
    return _ok(_get_client().patch(f"/stages/email/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_redirect_stage(name: str, **kwargs):
    """Create a redirect stage. Required: name."""
    return _ok(_get_client().post("/stages/redirect/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_redirect_stage(id: str, **kwargs):
    """Update a redirect stage."""
    return _ok(_get_client().patch(f"/stages/redirect/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_source_stage(name: str, **kwargs):
    """Create a source stage. Required: name."""
    return _ok(_get_client().post("/stages/source/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_source_stage(id: str, **kwargs):
    """Update a source stage."""
    return _ok(_get_client().patch(f"/stages/source/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_mtls_stage(name: str, **kwargs):
    """Create an mTLS stage. Required: name."""
    return _ok(_get_client().post("/stages/mtls/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_mtls_stage(id: str, **kwargs):
    """Update an mTLS stage."""
    return _ok(_get_client().patch(f"/stages/mtls/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_endpoint_stage(name: str, **kwargs):
    """Create an endpoint stage. Required: name."""
    return _ok(_get_client().post("/stages/endpoints/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_endpoint_stage(id: str, **kwargs):
    """Update an endpoint stage."""
    return _ok(_get_client().patch(f"/stages/endpoints/{id}/", json=kwargs))


# ── Stages — Invitation ──────────────────────────────────────────────


@_op(authentik_flows_write)
def create_invitation_stage(name: str, **kwargs):
    """Create an invitation stage. Required: name."""
    return _ok(_get_client().post("/stages/invitation/stages/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_invitation_stage(id: str, **kwargs):
    """Update an invitation stage."""
    return _ok(_get_client().patch(f"/stages/invitation/stages/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_invitation(**kwargs):
    """Create an invitation."""
    return _ok(_get_client().post("/stages/invitation/invitations/", json=kwargs))


@_op(authentik_flows_write)
def update_invitation(id: str, **kwargs):
    """Update an invitation."""
    return _ok(_get_client().patch(f"/stages/invitation/invitations/{id}/", json=kwargs))


@_op(authentik_flows_write)
def send_invitation_email(id: str):
    """Send invitation email."""
    return _ok(_get_client().post(f"/stages/invitation/invitations/{id}/send_email/"))


# ── Stages — Prompt ──────────────────────────────────────────────────


@_op(authentik_flows_write)
def create_prompt_stage(name: str, **kwargs):
    """Create a prompt stage. Required: name."""
    return _ok(_get_client().post("/stages/prompt/stages/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_prompt_stage(id: str, **kwargs):
    """Update a prompt stage."""
    return _ok(_get_client().patch(f"/stages/prompt/stages/{id}/", json=kwargs))


@_op(authentik_flows_write)
def create_prompt(name: str, **kwargs):
    """Create a prompt. Required: name."""
    return _ok(_get_client().post("/stages/prompt/prompts/", json={"name": name, **kwargs}))


@_op(authentik_flows_write)
def update_prompt(id: str, **kwargs):
    """Update a prompt."""
    return _ok(_get_client().patch(f"/stages/prompt/prompts/{id}/", json=kwargs))


@_op(authentik_flows_write)
def preview_prompt(**kwargs):
    """Preview a prompt."""
    return _ok(_get_client().post("/stages/prompt/prompts/preview/", json=kwargs))
