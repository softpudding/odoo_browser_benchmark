"""Seed data for mail.create_channel_invite_members.

Admin creates a private Discuss group channel and invites two users.
Seed ensures the two invitees exist as internal users and that no prior
channel with the target name lingers from a previous run.
"""


CHANNEL_NAME = "Release Rehearsal Team"

INVITEES = [
    {
        "name": "Nadia Rossi",
        "login": "nadia.rossi",
        "email": "nadia.rossi@example.com",
    },
    {
        "name": "Oliver Chen",
        "login": "oliver.chen",
        "email": "oliver.chen@example.com",
    },
]


def setup(env):
    # Remove any prior channel from a previous run so we always start clean.
    env["discuss.channel"].search([("name", "=", CHANNEL_NAME)]).unlink()

    admin = env.ref("base.user_admin")

    # Pre-create the OdooBot DM so it's in the before-state. Without this,
    # first-time Discuss access auto-creates it and shows up as a stray diff.
    odoobot = env.ref("base.partner_root")
    env["discuss.channel"].with_user(admin)._get_or_create_chat(
        partners_to=[odoobot.id]
    )

    # Ensure the two invitee users exist as internal users so they are
    # selectable in Discuss' "Add members" picker.
    internal_group = env.ref("base.group_user").id
    for spec in INVITEES:
        user = env["res.users"].search([("login", "=", spec["login"])], limit=1)
        if not user:
            user = env["res.users"].search([("name", "=", spec["name"])], limit=1)
        if not user:
            env["res.users"].create({
                "name": spec["name"],
                "login": spec["login"],
                "email": spec["email"],
                "group_ids": [(6, 0, [internal_group])],
            })
