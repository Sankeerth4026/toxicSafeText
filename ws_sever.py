import asyncio
import websockets
import json

connected_clients = set()

async def handler(websocket, path):
    print("[✓] Client connected")
    connected_clients.add(websocket)

    try:
        async for message in websocket:
            print("[→] Forwarding message to clients")
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
    except websockets.exceptions.ConnectionClosed:
        print("[x] Client disconnected")
    finally:
        connected_clients.remove(websocket)

async def main():
    print("[✓] Starting WebSocket server on ws://localhost:8765")
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())
