import sys
import pytest

from sanic import Sanic
from sanic.testing import SanicTestClient
import socket
from contextlib import closing

if sys.platform in ['win32', 'cygwin']:
    collect_ignore = ["test_worker.py"]


def is_port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def get_free_port():
    while True:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(('localhost', 0))
            port = s.getsockname()[1]
            if not is_port_in_use(port):
                return port


@pytest.fixture
def free_port():
    return get_free_port()


@pytest.fixture
def app(request):
    app = Sanic(request.node.name)
    app.test_client = SanicTestClient(app=app, port=get_free_port())
    return app

