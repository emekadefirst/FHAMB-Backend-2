from .base import template


def alert(firstname, lastname):
    return template(
        username=f"{firstname} {lastname}",
            body="""
            We Noticed some unusal activity, you logged in on a new device
            FHA Mortgage Bank Team
            """
            )