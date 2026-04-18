"""Cleanup-only seed for the canned response creation task."""


def setup(env):
    env["mail.canned.response"].search([("source", "=", ":greet")]).unlink()
