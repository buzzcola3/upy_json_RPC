# json-rpc (Modified for Cython/MicroPython)

This is a modified version of [pavlov99/json-rpc](https://github.com/pavlov99/json-rpc) with the following changes:

- Removed `includes` to work on **Cython/MicroPython**.
- Added support for **awaitable RPC methods**.

## Features
- Lightweight JSON-RPC implementation.
- Works with **Cython** and **MicroPython**.
- Supports asynchronous (`await`) RPC methods.

## Installation

For Cython:
```sh
pip install cython json-rpc
```

For MicroPython, copy the modified `jsonrpc` module to your device:
```sh
mpremote cp jsonrpc.py :/jsonrpc.py
```

## Usage

### Example WebServer using await Methods and Microdot on ESP32 (MicroPython Example)
```python
import asyncio
from jsonrpc import JSONRPCResponseManager, dispatcher
from microdot import Microdot, send_file
from microdot.websocket import with_websocket

app = Microdot()

@app.route('/')
async def run(request):
    return send_file("webserver/index.html")

@app.route('webserver/<path:path>')
async def static(request, path):
    if '..' in path:
        return 'Not found', 404
    return send_file('webserver/' + path)

@app.route('/ws')
@with_websocket
async def rpc_handler(request, ws):
    while True:
        message = await ws.receive()
        response = await JSONRPCResponseManager.handle(message, dispatcher)
        await ws.send(response.json)

app.run(debug=True, port=80)
```

## License
This project follows the original license from `pavlov99/json-rpc`.

## Contributing
Pull requests and issue reports are welcome!

## Acknowledgments
Thanks to [pavlov99](https://github.com/pavlov99) for the original implementation.

