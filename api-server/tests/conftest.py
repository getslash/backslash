from uuid import uuid4
import gzip
import hashlib
import os
import pytest
import requests
import socket
import subprocess
import threading
import time
import yarl
from contextlib import contextmanager


@pytest.fixture(scope="session")
def proxy_port():
    return int(os.environ.get("PROXY_PORT", 7777))

@pytest.fixture(params=['get', 'put', 'post', 'delete', 'options'])
def proxy_method(request, proxy):
    def func(*args, **kwargs):
        return proxy.request(request.param, *args, **kwargs)
    return func


@pytest.fixture(scope="session")
def backend_port():
    return int(os.environ.get("BACKEND_PORT", 7778))


@pytest.fixture(scope="session", autouse=True)
def proxy_process(proxy_port, backend_port):
    with _start_process(
        port=proxy_port,
        envvar="BACKSLASH_SPAWN_PROXY",
        cmd=f"cargo run 127.0.0.1 {proxy_port} 127.0.0.1 {backend_port}",
    ):
        yield


@pytest.fixture(scope="session", autouse=True)
def backend_process(backend_port):

    with _start_process(
        port=backend_port,
        envvar="BACKSLASH_SPAWN_BACKEND",
        cmd=f"python tests/stub_backend.py {backend_port}",
    ):
        yield


@pytest.fixture
def proxy(proxy_port):
    return Proxy(proxy_port)


class Proxy:
    def __init__(self, port):
        self.port = port

    def request(self, method, path, **kw):
        return requests.request(
            method,
            yarl.URL.build(scheme="http", host="127.0.0.1", port=self.port).with_path(
                path
            ),
            **kw,
        )

    def get(self, path, **kw):
        return self.request("get", path, **kw)

    def post(self, path, **kw):
        return self.request("post", path, **kw)


@contextmanager
def _start_process(*, port, envvar, cmd):

    if os.environ.get(envvar, "true").lower() == "true":
        print("Running", cmd, "...")
        process = subprocess.Popen(cmd, shell=True)
        print("Executed. PID=", process.pid)
    else:
        yield None
        return
    check_connectivity(port, process)

    try:
        yield process
    finally:
        process.terminate()
        process.wait()
    return process


def check_connectivity(port, process, *, timeout=60):
    end_time = time.time() + timeout
    while process is None or process.poll() is None:
        try:
            if port == 80:
                requests.get(f"http://127.0.0.1:{port}")
            else:
                s = socket.socket()
                s.connect(("127.0.0.1", port))
        except socket.error:
            if time.time() > end_time:
                raise
            time.sleep(0.1)
        else:
            break
    if process is not None and process.poll() is not None:
        raise RuntimeError("Process terminated!")
    print("*** Port", port, "is responsive")


@pytest.fixture
def random_data():
    class RandomData:
        def __init__(self, size=4096):
            self.data = os.urandom(size)
            self.sha1 = hashlib.sha1(self.data).hexdigest()

    return RandomData()


@pytest.fixture
def random_gzip():
    class RandomGzipData:
        def __init__(self, size=4096):
            self.inner_data = os.urandom(size)
            self.inner_digest = hashlib.sha1(self.inner_data).hexdigest()
            self.data = gzip.compress(self.inner_data)
            self.outer_digest = hashlib.sha1(self.data).hexdigest()

    return RandomGzipData()


@pytest.fixture
def random_stream(request):

    rd, wr = os.pipe()
    rd = os.fdopen(rd, mode="rb")
    wr = os.fdopen(wr, mode="wb")

    request.addfinalizer(rd.close)

    iterations = 10
    size = 1024 * 1024

    class BackgroundData:
        def __init__(self, thread):
            self._thread = thread
            self.stream = rd

        def wait(self):
            self._thread.join()
            self.digest = self._thread.sha1.hexdigest()

    class WritingThread(threading.Thread):
        def run(self):
            self.sha1 = hashlib.sha1()
            for i in range(iterations):
                data = os.urandom(size)
                self.sha1.update(data)
                print("Writing data...")
                wr.write(data)
                time.sleep(0.1)
            wr.close()

    thread = WritingThread()
    thread.start()

    return BackgroundData(thread)


@pytest.fixture
def header_name():
    return 'X-Example-Header'

@pytest.fixture
def header_value():
    return str(uuid4())
