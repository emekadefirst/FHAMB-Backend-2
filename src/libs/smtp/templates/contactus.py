from .base import template

def contact(sender_name):
    return template(
        username=sender_name,
        body=f"""
            <p>Thank you for reaching out to us. We have received your message and will get back to you as soon as possible.</p>
            <p>Best regards,<br>
            The FHA Mortgage Support Team</p>
        """
    )
