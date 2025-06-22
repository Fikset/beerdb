#!/usr/bin/env python3
import time
from subprocess import Popen
from src.Client import Client

def test_server_client():
    server = Popen(['python', './src/Server.py'])
    time.sleep(2)  # Give server time to start
    try:
        client = Client()
        sum_result = client.get_sum(3, 4)
        assert sum_result == 7
        client.close()
    finally:
        server.terminate()
        server.wait()