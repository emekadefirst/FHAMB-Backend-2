from .base import template


def verify(otp):
    return template(
            body=f"""
            Thank you for signing up with FHA Mortgage Bank.
            verify your account using this OTP: <h4>{otp}</h4>
            """
            )