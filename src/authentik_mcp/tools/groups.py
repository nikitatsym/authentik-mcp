from ..registry import Group

authentik_read = Group(
    "authentik_read",
    "Query Authentik data (safe, read-only).\n\n"
    "Call with operation=\"help\" to list all available read operations.\n"
    "Otherwise pass the operation name and a JSON object with parameters.\n\n"
    "Example: authentik_read(operation=\"ListUsers\", params={\"search\": \"admin\"})",
)

authentik_write = Group(
    "authentik_write",
    "Create or update Authentik resources (non-destructive).\n\n"
    "Call with operation=\"help\" to list all available write operations.\n"
    "Otherwise pass the operation name and a JSON object with parameters.\n\n"
    "Example: authentik_write(operation=\"CreateUser\", "
    "params={\"username\": \"alice\", \"name\": \"Alice\"})",
)

authentik_delete = Group(
    "authentik_delete",
    "Delete Authentik resources (destructive, irreversible).\n\n"
    "Call with operation=\"help\" to list all available delete operations.\n"
    "Otherwise pass the operation name and a JSON object with parameters.\n\n"
    "Example: authentik_delete(operation=\"DeleteUser\", params={\"id\": 1})",
)

authentik_flows_read = Group(
    "authentik_flows_read",
    "Query Authentik auth pipeline config: flows, stages, policies, sources, events (safe, read-only).\n\n"
    "Call with operation=\"help\" to list all available operations.\n"
    "Otherwise pass the operation name and a JSON object with parameters.\n\n"
    "Example: authentik_flows_read(operation=\"ListFlows\")",
)

authentik_flows_write = Group(
    "authentik_flows_write",
    "Create or update Authentik auth pipeline config: flows, stages, policies, sources (non-destructive).\n\n"
    "Call with operation=\"help\" to list all available operations.\n"
    "Otherwise pass the operation name and a JSON object with parameters.\n\n"
    "Example: authentik_flows_write(operation=\"CreateFlow\", "
    "params={\"name\": \"my-flow\", \"slug\": \"my-flow\", \"designation\": \"authorization\"})",
)

authentik_admin = Group(
    "authentik_admin",
    "Admin-only Authentik operations: settings, system, version, files, admin authenticator devices.\n\n"
    "Call with operation=\"help\" to list all available admin operations.\n"
    "Otherwise pass the operation name and a JSON object with parameters.\n\n"
    "Example: authentik_admin(operation=\"GetSystemInfo\")",
)
