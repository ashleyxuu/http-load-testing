import pytest
import asyncio
import aiohttp
from aiohttp import web
from unittest.mock import patch
from load_tester import main
from aiohttp.test_utils import TestClient


@pytest.fixture
async def mock_server():
    # Setup a mock HTTP server with success and error routes
    app = web.Application()
    app.router.add_get('/success', lambda request: web.Response(text='Success', status=200))
    app.router.add_get('/error', lambda request: web.Response(text='Error', status=500))

    runner = web.AppRunner(app)
    await runner.setup()
    server = web.TCPSite(runner, 'localhost', 0)  # 0 for dynamic port assignment
    await server.start()
    
    # Get the server's address
    host = server._host
    port = server._port

    url = f'http://{host}:{port}'
    
    yield url

    await server.stop()
    await runner.cleanup()


@pytest.mark.asyncio
@patch('builtins.print')
async def test_load_tester_success(mock_print, mock_server):
    # Use the mock server's URL
    url = f'{mock_server}/success'
    await main(url, qps=5, duration=2)
    
    output = [call.args[0] for call in mock_print.call_args_list]
    assert any("Average Latency:" in line for line in output)
    assert any("Latency Standard Deviation:" in line for line in output)
    assert any("Error rate: 0%" in line for line in output)


@pytest.mark.asyncio
@patch('builtins.print')
async def test_load_tester_error(mock_print, mock_server):
    # Use the mock server's URL
    url = f'{mock_server}/error'
    await main(url, qps=5, duration=2)
    
    output = [call.args[0] for call in mock_print.call_args_list]

    assert any("Total Requests:" in line for line in output)
    assert any("Error rate:" in line for line in output)


@pytest.mark.asyncio
@patch('builtins.print')
async def test_load_tester_invalid_url(mock_print):
    await main('http://invalid_url', qps=1, duration=1)
    
    output = [call.args[0] for call in mock_print.call_args_list]

    assert any("No successful requests." in line for line in output)
