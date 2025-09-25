import asyncio
import aiosmtplib
import logging
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from typing import List, Optional
from src.config.env import EMAIL_USER, EMAIL_HOST, EMAIL_PASSWORD, EMAIL_PORT

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class EmailService:
    def __init__(self):
        self.host = EMAIL_HOST
        self.port = int(EMAIL_PORT)
        self.username = EMAIL_USER
        self.password = EMAIL_PASSWORD
        self.timeout = 20
        self.semaphore = asyncio.Semaphore(10)
        self.tls_context = ssl.create_default_context()

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
                if self.port == 465:  # Implicit SSL
                    server = aiosmtplib.SMTP(
                        hostname=self.host,
                        port=self.port,
                        use_tls=True,
                        timeout=self.timeout,
                        tls_context=self.tls_context
                    )
                else:  # Typically port 587 with STARTTLS
                    server = aiosmtplib.SMTP(
                        hostname=self.host,
                        port=self.port,
                        use_tls=False,
                        start_tls=True,
                        timeout=self.timeout,
                        tls_context=self.tls_context
                    )

                await server.connect()
                await server.login(self.username, self.password)
                await server.sendmail(
                    from_email or self.username,
                    recipients,
                    msg.as_string()
                )
                await server.quit()

                print(f"✅ Email sent to {recipients}")
                return True

            except aiosmtplib.SMTPException as e:
                logger.error(f"SMTP error sending email: {e}")
                return False
            except Exception as e:
                logger.error(f"Unexpected error sending email: {e}")
                return False
