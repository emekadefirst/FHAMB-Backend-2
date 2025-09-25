from src.apps.auth.user.routes import user_route
from src.apps.auth.permssion.routes import permission_route, permission_group_route
from src.apps.file.routes import file_router
from src.apps.public.mail.routes import mail_router


routes = [
    user_route,
    permission_route, 
    permission_group_route,
    file_router,
    mail_router
]