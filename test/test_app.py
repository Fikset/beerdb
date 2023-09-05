#!/usr/bin/env python3
from subprocess import Popen
from src.Client import Client

def test_server_client():
    server = Popen('./src/Server.py')
    client = Client()
    sum = client.get_sum(3, 4)
    assert (sum == 7)