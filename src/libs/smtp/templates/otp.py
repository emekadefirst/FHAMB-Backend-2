from .base import template


def otp(firstname, lastname, otp):
    return template(
        username=f"{firstname} {lastname}",
        body=f"""
            Your One-Time Password (OTP) for resetting your password is:

            OTP: {otp}

            This code is valid for the next 5 minutes. If you did not request this, please ignore this message.

        """
        )