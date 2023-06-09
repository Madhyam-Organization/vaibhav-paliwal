"""
ASGI config for chatApplication project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatApplication.settings')

# application = get_asgi_application()
application = ProtocolTypeRouter({
    # Here we are doing is that our application can use both protocols HTTP for synchronous communication and WebSocket for asynchronous
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    )
})