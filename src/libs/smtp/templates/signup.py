from .base import template


def newuser(firstname, lastname):
    return template(
        username=f"{firstname} {lastname}",
            body="""
            Thank you for signing up with FHA Mortgage Bank.
            Your account has been successfully created. You can now log in to explore our mortgage solutions, apply for loans, and manage your account with ease.
            If you didn’t sign up for this account, please ignore this email or contact our support team.
            We’re excited to support you on your journey to homeownership!
            Best regards,
            FHA Mortgage Bank Team
            """
            )