import asyncio
from src.libs.smtp.mailer import EmailService

async def main():
    smtp = EmailService()
    success = await smtp.send_email(
        subject="Test Email from FHA Mortgage",
        body="<h1>Hello Victor!</h1><p>This is a working test email.</p>",
        to_emails=["emekadefirst@gmail.com"],  # ✅ send to Gmail
    )
    print("Email sent:", success)

asyncio.run(main())
