from .base import template
from src.config.env import FRONTEND_URL

def content_email(title, image, id, content_type):
    url_map = {
        "news": f"{FRONTEND_URL}/news",
        "event": f"{FRONTEND_URL}/events"
    }

    # ✅ Choose URL based on content type
    if content_type == "news":
        read_more_url = f"{url_map['news']}/{id}"
    else:
        read_more_url = f"{url_map['event']}/{id}"

    body = f"""
        <div style="font-family:Arial, sans-serif; text-align:center;">
            <h2 style="color:#004274; margin-bottom:10px;">{title}</h2>
            <div style="margin-top:15px;">
                <img src="{image}" alt="{title}" 
                     style="width:180px; height:auto; border-radius:8px; object-fit:cover;">
            </div>
            <a href="{read_more_url}"
                style="display:inline-block; margin-top:15px;
                       background:#28a745; color:#fff; padding:10px 18px;
                       text-decoration:none; border-radius:5px; font-weight:bold;">
                Read more
            </a>
        </div>
    """
    return template(body=body)


