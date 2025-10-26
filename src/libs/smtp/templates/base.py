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
            body {{
                font-family: Arial, sans-serif;
                background-color: #f5f7fa;
                color: #333;
                margin: 0;
                padding: 0;
            }}
            .email-container {{
                max-width: 600px;
                margin: 30px auto;
                background: #fff;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                background-color: #004274;
                color: #fff;
                text-align: center;
                padding: 20px 10px;
            }}
            .header .logo {{
                width: 50px;
                height: 50px;
                border-radius: 50%;
                object-fit: cover;
                margin-bottom: 8px;
            }}
            .content {{
                padding: 25px 20px;
            }}
            .greeting {{
                font-size: 18px;
                font-weight: bold;
                color: #004274;
                margin-bottom: 10px;
            }}
            .message {{
                font-size: 15px;
                line-height: 1.6;
                margin-bottom: 20px;
            }}
            .cta-section {{
                text-align: center;
                margin: 25px 0;
            }}
            .cta-button {{
                background-color: #28a745;
                color: #fff;
                padding: 12px 25px;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                display: inline-block;
            }}
            .divider {{
                height: 1px;
                background-color: #e1e1e1;
                margin: 20px 0;
            }}
            .info-box {{
                background: #f1f1f1;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
            }}
            .info-box h3 {{
                margin-top: 0;
                color: #004274;
            }}
            .footer {{
                background-color: #004274;
                color: #fff;
                text-align: center;
                padding: 20px 10px;
                font-size: 13px;
            }}
            .footer a {{
                color: #28a745;
                text-decoration: none;
                margin: 0 8px;
            }}
            .footer .contact-info h4 {{
                margin: 0;
                font-size: 14px;
                color: #28a745;
            }}
            .footer .contact-item p {{
                margin: 3px 0 10px;
                font-size: 13px;
            }}
            @media (max-width: 600px) {{
                .email-container {{
                    width: 95%;
                }}
                .cta-button {{
                    width: 100%;
                    display: block;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <img src="https://fhamortgage.gov.ng/assets/fha-BYkM8mil.png" alt="FHA Mortgage Bank" class="logo">
                <h1>Your Trusted Mortgage Partner</h1>
            </div>

            <div class="content">
                <div class="greeting">
                    Hello {name},
                </div>

                <div class="message">
                    {body}
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
                <div class="contact-info">
                    <div class="contact-item">
                        <h4>Email</h4>
                        <p>info@fhamortgage.gov.ng</p>
                    </div>
                    <div class="contact-item">
                        <h4>Website</h4>
                        <p>fhamortgage.gov.ng</p>
                    </div>
                </div>

                <div class="social-links">
                    <a href="#">Facebook</a> | 
                    <a href="#">LinkedIn</a> | 
                    <a href="#">Twitter</a>
                </div>

                <div class="disclaimer" style="margin-top: 10px; font-size: 12px;">
                    <p>This email was sent by FHA Mortgage Bank Limited. All loan applications are subject to credit approval. Terms and conditions apply.
                    Equal Housing Lender.</p>
                    <p>If you no longer wish to receive these emails, you can <a href="#" style="color: #28a745;">unsubscribe here</a>.</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
