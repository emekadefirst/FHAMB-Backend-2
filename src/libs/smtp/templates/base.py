from typing import Optional, List

def template(body: str, username: Optional[str] = None, attachment: Optional[List[str]] = None) -> str:
    name = username or "Customer"
    attachment_section = ""
    
    if attachment:
        attachment_list = "".join(f"<li>{file}</li>" for file in attachment)
        attachment_section = f"""
        <div class="info-box">
            <h3>Attached Documents:</h3>
            <ul>{attachment_list}</ul>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <style>
            /* [Same CSS styles from your original code, omitted here for brevity] */
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <img src="https://fhambank-dev.s3.eu-north-1.amazonaws.com/public/fham.png" alt="FHA Mortgage Bank" class="logo">
                <h1>Your Trusted Mortgage Partner</h1>
            </div>

            <div class="content">
                <div class="greeting">
                    Hello {name},
                </div>

                <div class="message">
                    <p>{body}</p>
                </div>

                {attachment_section}

                <div class="cta-section">
                    <a href="#" class="cta-button">Get Pre-Approved Today</a>
                </div>

                <div class="divider"></div>

                <div class="message">
                    <p>Ready to take the next step? Our mortgage specialists are standing by to discuss your options and help you find the perfect loan solution for your needs.</p>
                    <p>Contact us today for a free consultation and discover how we can make your homeownership goals a reality.</p>
                </div>
            </div>

            <div class="footer">
                <div class="footer-content">
                    <div class="contact-info">
                        <div class="contact-item">
                            <h4>Phone</h4>
                            <p>+1 (555) 123-4567</p>
                        </div>
                        <div class="contact-item">
                            <h4>Email</h4>
                            <p>info@fhamortgagebank.com</p>
                        </div>
                        <div class="contact-item">
                            <h4>Website</h4>
                            <p>www.fhamortgagebank.com</p>
                        </div>
                    </div>

                    <div class="social-links">
                        <a href="#">Facebook</a>
                        <a href="#">LinkedIn</a>
                        <a href="#">Twitter</a>
                    </div>

                    <div class="disclaimer">
                        <p>This email was sent by FHA Mortgage Bank Limited. All loan applications are subject to credit approval. Terms and conditions apply. 
                        Equal Housing Lender. NMLS ID: [License Number]</p>

                        <p>If you no longer wish to receive these emails, you can <a href="#" style="color: #28a745;">unsubscribe here</a>.</p>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
