import asyncio
from src.libs.smtp.mailer import EmailService
from src.libs.smtp.templates.newsnevent import content_email

mail = EmailService()

async def demo():
    content = content_email(title="Test", image="s://res.cloudinary.com/dpmpvftcw/image/upload/v1761525687/tjoq16qfwsuz2jdcruba.jpg", id="be82fd93-cc00-4c14-83b5-d67f71f96be6", content_type="news")
    return await mail.send_email(subject="Test", body=content, to_emails=["emekadefirst@gmail.com"])

print(asyncio.run(demo()))