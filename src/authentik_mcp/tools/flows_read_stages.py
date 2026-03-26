from ..registry import _op
from .groups import authentik_flows_read
from .helpers import SLIM_STAGE, _get_client, _paginated

# ── Stages — All ─────────────────────────────────────────────────────


@_op(authentik_flows_read)
def list_stages(limit: int = 20):
    """List all stages."""
    return _paginated("/stages/all/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_stage(id: str):
    """Get stage details."""
    return _get_client().get(f"/stages/all/{id}/")


@_op(authentik_flows_read)
def list_stage_types():
    """List stage types."""
    return _get_client().get("/stages/all/types/")


# ── Stages — Identification ──────────────────────────────────────────


@_op(authentik_flows_read)
def list_identification_stages(limit: int = 20):
    """List identification stages."""
    return _paginated("/stages/identification/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_identification_stage(id: str):
    """Get identification stage details."""
    return _get_client().get(f"/stages/identification/{id}/")


# ── Stages — Password ────────────────────────────────────────────────


@_op(authentik_flows_read)
def list_password_stages(limit: int = 20):
    """List password stages."""
    return _paginated("/stages/password/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_password_stage(id: str):
    """Get password stage details."""
    return _get_client().get(f"/stages/password/{id}/")


# ── Stages — Authenticator ───────────────────────────────────────────


@_op(authentik_flows_read)
def list_authenticator_totp_stages(limit: int = 20):
    """List authenticator TOTP stages."""
    return _paginated("/stages/authenticator/totp/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_authenticator_totp_stage(id: str):
    """Get authenticator TOTP stage details."""
    return _get_client().get(f"/stages/authenticator/totp/{id}/")


@_op(authentik_flows_read)
def list_authenticator_webauthn_stages(limit: int = 20):
    """List authenticator WebAuthn stages."""
    return _paginated("/stages/authenticator/webauthn/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_authenticator_webauthn_stage(id: str):
    """Get authenticator WebAuthn stage details."""
    return _get_client().get(f"/stages/authenticator/webauthn/{id}/")


@_op(authentik_flows_read)
def list_authenticator_duo_stages(limit: int = 20):
    """List authenticator Duo stages."""
    return _paginated("/stages/authenticator/duo/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_authenticator_duo_stage(id: str):
    """Get authenticator Duo stage details."""
    return _get_client().get(f"/stages/authenticator/duo/{id}/")


@_op(authentik_flows_read)
def list_authenticator_sms_stages(limit: int = 20):
    """List authenticator SMS stages."""
    return _paginated("/stages/authenticator/sms/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_authenticator_sms_stage(id: str):
    """Get authenticator SMS stage details."""
    return _get_client().get(f"/stages/authenticator/sms/{id}/")


@_op(authentik_flows_read)
def list_authenticator_email_stages(limit: int = 20):
    """List authenticator email stages."""
    return _paginated("/stages/authenticator/email/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_authenticator_email_stage(id: str):
    """Get authenticator email stage details."""
    return _get_client().get(f"/stages/authenticator/email/{id}/")


@_op(authentik_flows_read)
def list_authenticator_static_stages(limit: int = 20):
    """List authenticator static stages."""
    return _paginated("/stages/authenticator/static/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_authenticator_static_stage(id: str):
    """Get authenticator static stage details."""
    return _get_client().get(f"/stages/authenticator/static/{id}/")


@_op(authentik_flows_read)
def list_authenticator_validate_stages(limit: int = 20):
    """List authenticator validate stages."""
    return _paginated("/stages/authenticator/validate/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_authenticator_validate_stage(id: str):
    """Get authenticator validate stage details."""
    return _get_client().get(f"/stages/authenticator/validate/{id}/")


@_op(authentik_flows_read)
def list_authenticator_endpoint_gdtc_stages(limit: int = 20):
    """List authenticator endpoint GDTC stages."""
    return _paginated("/stages/authenticator/endpoint_gdtc/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_authenticator_endpoint_gdtc_stage(id: str):
    """Get authenticator endpoint GDTC stage details."""
    return _get_client().get(f"/stages/authenticator/endpoint_gdtc/{id}/")


# ── Stages — User ────────────────────────────────────────────────────


@_op(authentik_flows_read)
def list_user_login_stages(limit: int = 20):
    """List user login stages."""
    return _paginated("/stages/user_login/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_user_login_stage(id: str):
    """Get user login stage details."""
    return _get_client().get(f"/stages/user_login/{id}/")


@_op(authentik_flows_read)
def list_user_logout_stages(limit: int = 20):
    """List user logout stages."""
    return _paginated("/stages/user_logout/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_user_logout_stage(id: str):
    """Get user logout stage details."""
    return _get_client().get(f"/stages/user_logout/{id}/")


@_op(authentik_flows_read)
def list_user_write_stages(limit: int = 20):
    """List user write stages."""
    return _paginated("/stages/user_write/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_user_write_stage(id: str):
    """Get user write stage details."""
    return _get_client().get(f"/stages/user_write/{id}/")


@_op(authentik_flows_read)
def list_user_delete_stages(limit: int = 20):
    """List user delete stages."""
    return _paginated("/stages/user_delete/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_user_delete_stage(id: str):
    """Get user delete stage details."""
    return _get_client().get(f"/stages/user_delete/{id}/")


# ── Stages — Consent ─────────────────────────────────────────────────


@_op(authentik_flows_read)
def list_consent_stages(limit: int = 20):
    """List consent stages."""
    return _paginated("/stages/consent/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_consent_stage(id: str):
    """Get consent stage details."""
    return _get_client().get(f"/stages/consent/{id}/")


# ── Stages — Captcha ─────────────────────────────────────────────────


@_op(authentik_flows_read)
def list_captcha_stages(limit: int = 20):
    """List captcha stages."""
    return _paginated("/stages/captcha/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_captcha_stage(id: str):
    """Get captcha stage details."""
    return _get_client().get(f"/stages/captcha/{id}/")


# ── Stages — Deny ────────────────────────────────────────────────────


@_op(authentik_flows_read)
def list_deny_stages(limit: int = 20):
    """List deny stages."""
    return _paginated("/stages/deny/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_deny_stage(id: str):
    """Get deny stage details."""
    return _get_client().get(f"/stages/deny/{id}/")


# ── Stages — Dummy ───────────────────────────────────────────────────


@_op(authentik_flows_read)
def list_dummy_stages(limit: int = 20):
    """List dummy stages."""
    return _paginated("/stages/dummy/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_dummy_stage(id: str):
    """Get dummy stage details."""
    return _get_client().get(f"/stages/dummy/{id}/")


# ── Stages — Email ───────────────────────────────────────────────────


@_op(authentik_flows_read)
def list_email_stages(limit: int = 20):
    """List email stages."""
    return _paginated("/stages/email/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_email_stage(id: str):
    """Get email stage details."""
    return _get_client().get(f"/stages/email/{id}/")


@_op(authentik_flows_read)
def list_email_stage_templates():
    """List email stage templates."""
    return _get_client().get("/stages/email/templates/")


# ── Stages — Redirect ────────────────────────────────────────────────


@_op(authentik_flows_read)
def list_redirect_stages(limit: int = 20):
    """List redirect stages."""
    return _paginated("/stages/redirect/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_redirect_stage(id: str):
    """Get redirect stage details."""
    return _get_client().get(f"/stages/redirect/{id}/")


# ── Stages — Source ──────────────────────────────────────────────────


@_op(authentik_flows_read)
def list_source_stages(limit: int = 20):
    """List source stages."""
    return _paginated("/stages/source/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_source_stage(id: str):
    """Get source stage details."""
    return _get_client().get(f"/stages/source/{id}/")


# ── Stages — mTLS ────────────────────────────────────────────────────


@_op(authentik_flows_read)
def list_mtls_stages(limit: int = 20):
    """List mTLS stages."""
    return _paginated("/stages/mtls/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_mtls_stage(id: str):
    """Get mTLS stage details."""
    return _get_client().get(f"/stages/mtls/{id}/")


# ── Stages — Endpoint ────────────────────────────────────────────────


@_op(authentik_flows_read)
def list_endpoint_stages(limit: int = 20):
    """List endpoint stages."""
    return _paginated("/stages/endpoints/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_endpoint_stage(id: str):
    """Get endpoint stage details."""
    return _get_client().get(f"/stages/endpoints/{id}/")


# ── Stages — Invitation ──────────────────────────────────────────────


@_op(authentik_flows_read)
def list_invitation_stages(limit: int = 20):
    """List invitation stages."""
    return _paginated("/stages/invitation/stages/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_invitation_stage(id: str):
    """Get invitation stage details."""
    return _get_client().get(f"/stages/invitation/stages/{id}/")


@_op(authentik_flows_read)
def list_invitations(limit: int = 20):
    """List invitations."""
    return _paginated("/stages/invitation/invitations/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_invitation(id: str):
    """Get invitation details."""
    return _get_client().get(f"/stages/invitation/invitations/{id}/")


# ── Stages — Prompt ──────────────────────────────────────────────────


@_op(authentik_flows_read)
def list_prompt_stages(limit: int = 20):
    """List prompt stages."""
    return _paginated("/stages/prompt/stages/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_prompt_stage(id: str):
    """Get prompt stage details."""
    return _get_client().get(f"/stages/prompt/stages/{id}/")


@_op(authentik_flows_read)
def list_prompts(limit: int = 20):
    """List prompts."""
    return _paginated("/stages/prompt/prompts/", limit=limit, slim_fields=SLIM_STAGE)


@_op(authentik_flows_read)
def show_prompt(id: str):
    """Get prompt details."""
    return _get_client().get(f"/stages/prompt/prompts/{id}/")
