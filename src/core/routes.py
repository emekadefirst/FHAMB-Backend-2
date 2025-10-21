from src.apps.auth.user.routes import user_route
from src.apps.auth.permisssion.routes import permission_route, permission_group_route
from src.apps.file.routes import file_router
from src.apps.public.mail.routes import mail_router
from src.apps.public.subscribers.routes import subscriber_router
from src.apps.public.contact.routes import contact_router, team_router, social_router, branch_router
from src.apps.public.blog.routes import category_router, blogs_router
from src.apps.public.event.routes import event_router
from src.apps.public.faq.routes import faq_router
from src.apps.public.gallery.routes import gallery_router

routes = [
    user_route,
    category_router,
    blogs_router,
    subscriber_router,
    event_router,
    gallery_router,
    faq_router,
    permission_route, 
    permission_group_route,
    file_router,
    mail_router,
    contact_router,
    team_router,
    social_router,
    branch_router
]