import asyncio
import aiosmtplib
import logging
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from typing import List, Optional
from src.config.env import EMAIL_USER, EMAIL_HOST, EMAIL_PASSWORD, EMAIL_PORT

# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Production TLS context (verifies cert)
tls_context = ssl.create_default_context()

class EmailService:
    def __init__(self):
        self.host = EMAIL_HOST
        self.port = EMAIL_PORT
        self.username = EMAIL_USER
        self.password = EMAIL_PASSWORD
        self.timeout = 10
        self.semaphore = asyncio.Semaphore(10)

    async def send_email(
        self,
        subject: str,
        body: str,
        to_emails: List[str],
        from_email: Optional[str] = None,
        cc_emails: Optional[List[str]] = None,
        bcc_emails: Optional[List[str]] = None,
        body_type: str = "html",
        reply_to: Optional[str] = None
    ) -> bool:
        if not to_emails:
            raise ValueError("At least one recipient email is required")

        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = formataddr(("", from_email or self.username))
        msg["To"] = ", ".join(to_emails)

        if cc_emails:
            msg["Cc"] = ", ".join(cc_emails)
        if bcc_emails:
            msg["Bcc"] = ", ".join(bcc_emails)
        if reply_to:
            msg["Reply-To"] = reply_to

        msg.attach(MIMEText(body, body_type))

        recipients = to_emails + (cc_emails or []) + (bcc_emails or [])

        async with self.semaphore:
            try:
                async with aiosmtplib.SMTP(
                    hostname="st201.sternhost.net",
                    port=self.port,
                    use_tls=True,
                    start_tls=False,
                    timeout=30,
                    tls_context=ssl.create_default_context() 
                ) as server:
                    await server.login(self.username, self.password)
                    await server.sendmail(
                        from_email or self.username,
                        recipients,
                        msg.as_string()
                    )
                logger.info(f"✅ Email sent to {recipients}")
                return True
            except aiosmtplib.SMTPException as e:
                logger.error(f"SMTP error sending email: {str(e)}")
                return False
            except Exception as e:
                logger.error(f"Unexpected error sending email: {str(e)}")
                return False
