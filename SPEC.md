# Authentik operation contract

This server targets Authentik **2026.8.3 only**. The vendored JSON OpenAPI
schema is `codegen/schema-2026.8.3.json`; `codegen/schema-source.json` records
the source URL and requested media type. Generation and conformance checks are
offline and never negotiate server versions.

## Sources of truth

- The OpenAPI schema owns HTTP methods, paths, request fields, types,
  nullability, and requiredness.
- `codegen/operations/<api-area>.json` owns the public name, description, group,
  and exposed flag for every schema operationId. Each schema operation has
  exactly one row, including excluded operations.
- A PUT sharing its path with PATCH is not exposed. Its table row has
  `exposed: false`; the PATCH operation is the public update operation.
- `src/authentik_mcp/_generated.py` contains generated wrappers, nested request
  models, and transport metadata. Do not edit it manually.
- `src/authentik_mcp/tools/overrides.py` preserves hand-maintained list
  projections and policy-binding read-modify-write updates. The binding
  serializer requires a complete target and subject even during partial
  validation, so UpdatePolicyBinding merges omitted fields from GET and sends
  PUT while retaining PATCH's public optional-parameter contract. The PUT row
  remains excluded from public exposure.
- Transport and pagination behavior live in `tools/runtime.py`; generated
  files do not contain handwritten edits.

## Parameters and responses

Required schema inputs have no default. Optional inputs default to `_UNSET`;
omission is different from explicit JSON null. Null is accepted only for
nullable inputs. Unknown fields are rejected before HTTP, including unknown
nested object fields. Open-ended schema objects remain open-ended.

Parameter names use the upstream wire name. Python keywords gain a trailing
underscore. If a body field collides with a path/query input, the body input
has a `body_` prefix: `UpdateApplication(slug="old", body_slug="new")` changes
the slug while addressing the existing application. Required path parameters
use upstream names such as `group_uuid`, `policy_binding_uuid`, and
`stage_uuid`, rather than the old generic `id` aliases.

Paginated operations return the results list. `limit` defaults to a page size
of 20 at transport time; `page`, `page_size`, and every schema filter are
exposed. Pass either `limit` or `page_size`, or the same value for both.
Existing slim list projections are preserved; operations without a projection
return their upstream result objects. Show operations return full details.

Multipart `file` inputs are server-local file paths. Binary response endpoints
(such as flow export) return text rather than attempting JSON parsing.

## Groups

The public group set remains `authentik_read`, `authentik_write`,
`authentik_delete`, `authentik_flows_read`, `authentik_flows_write`, and
`authentik_admin`. Existing assignments are retained except reviewed risk
corrections. New read/write operations for flows, stages, policies, sources,
events, and requests belong to the flow groups; other areas use the core groups.
Deletes belong to `authentik_delete` except retained admin-only operations.
Admin-area operations and full admin-device replacements stay in
`authentik_admin`. `ShowFlowChallenge` and `ExecuteFlow` belong to
`authentik_flows_write` despite using GET: they mutate session plans.

## Regeneration and validation

```sh
uv run python codegen/generate.py
uv run python codegen/generate.py --check
uv run python codegen/check_contract.py
./dev.py check
```

The generator gate rejects missing/stale rows, blank metadata, unknown groups,
public-name collisions, invalid exposure flags, and changed generated output.
The independent contract gate compares the actual registered wrapper signature
and Pydantic required fields with every exposed operation's body/query/path
contract in the vendored schema.

For a table review slice, validate without modifying generated output:

```sh
uv run python codegen/generate.py --check --area stages
```

Review names in the established PascalCase operation style: ListX, ShowX,
CreateX, UpdateX, DeleteX; `ShowXUsedBy` identifies reference lookup endpoints.
Excluded full updates use ReplaceX. Prefer task-specific names for actions.
Descriptions explain the user-visible operation and constraints, not upstream
Viewset/Serializer/Mixin boilerplate. Keep names and descriptions ASCII English.
Do not alter operationIds or move operations between API-area files.

## Test environment

```sh
uv run python scripts/bootstrap.py
./dev.py check
./dev.py e2e
```

The compose stack pins Authentik 2026.8.3, isolates its database in a
version-named Compose project, and includes a local Mailpit SMTP server.
Recovery-email tests create an email stage and recovery flow, temporarily
select that flow on the default brand, and verify delivery before restoring
the brand. Tests never write to live instances.

## Replaced endpoints

- `SetApplicationIconUrl`, `SetApplicationIcon`, and `ClearApplicationIcon`:
  use `UpdateApplication(slug=..., meta_icon=<URL>)`, or `meta_icon=""` to clear.
  To upload a local icon, use `CreateAdminFile` and supply its storage URL.
- `ImportFlow`: use `ImportBlueprint(file=<local YAML path>)`. It applies
  flow-export blueprint YAML once without storing a blueprint instance.
- Group `parent`: use `parents=[<group UUID>, ...]`.
- `ListWorkers` uses `/tasks/workers/` including the trailing slash.
- Tenant and tenant-domain operations are absent from the 2026.8.3 schema and
  are not exposed. There is no replacement in this version's API schema.
