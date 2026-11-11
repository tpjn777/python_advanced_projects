# Python Chat Room

A simple multi-client chat room built with Python sockets and a Tkinter GUI. One server accepts multiple clients, and every message a client sends is broadcast to everyone connected.

## Features

- Multiple clients chatting at the same time
- Name registration when joining
- Join and leave notifications for all users
- Messages shown with the sender's name (`Ali: hello`)
- Graphical client with scrollable message list, Send button, and Quit button
- Press Enter to send
- Clean exit with `#quit`, the Quit button, or closing the window

## Project Structure

| File | Description |
|------|-------------|
| `server.py` | The chat server. Accepts connections and broadcasts messages. |
| `client.py` | GUI client. Asks you to type your name in the chat window after connecting. |
| `client2.py` | GUI client that takes your name at launch and registers automatically. The name also appears in the window title. |

## Requirements

- Python 3.6 or newer
- Tkinter (included with most Python installations)

On some Linux distributions Tkinter must be installed separately:

```
sudo apt install python3-tk
```

No third-party packages are needed.

## How to Run

1. Start the server first:

   ```
   python server.py
   ```

2. In a new terminal, start a client. Use either option:

   **Option A: `client.py`**

   ```
   python client.py
   ```

   Type your name in the message box and press Enter or click Send.

   **Option B: `client2.py`**

   ```
   python client2.py Ali
   ```

   If you leave out the name, the program asks for it in the terminal.

3. To chat with more than one person, open more terminals and start more clients, each with a different name:

   ```
   python client2.py Sara
   ```

4. Type a message and press Enter. Everyone connected sees it.

5. To leave, type `#quit`, click Quit, or close the window.

## Configuration

Both files use these defaults:

| Setting | Value |
|---------|-------|
| Host | `localhost` / `127.0.0.1` |
| Port | `9090` |

To change the port, edit `PORT` at the top of `server.py`, `client.py`, and `client2.py` so they all match.

To chat across different computers on the same network:

1. In `server.py`, set `HOST = '0.0.0.0'`.
2. In the client files, set `HOST` to the server computer's local IP address (for example `192.168.1.20`).
3. Allow port 9090 through the server computer's firewall.

## How It Works

- The server listens on a TCP socket and starts a new thread for each client.
- The first message a client sends is its name. The server then sends a welcome message and announces the new user.
- Each message a client sends is broadcast to every connected client with the sender's name as a prefix.
- When a client sends `#quit`, or disconnects unexpectedly, the server removes it and tells the others.
- On the client side, a background thread receives messages while the Tkinter window handles input.

## Known Limitations

- No encryption or authentication. Use only on trusted networks.
- Names are not checked for uniqueness.
- Messages are limited to 1024 bytes each.
- No message history. You only see messages sent while you are connected.
- Tkinter is not fully thread-safe, and the receive thread updates the message list directly. This works for a small project. A larger app should pass messages to the main thread with `queue.Queue` and `window.after()`.

## Possible Improvements

- Private messages (`@name message`)
- A list of online users
- Timestamps on messages
- Unique-name checking
- Message history
- Encryption with TLS (`ssl` module)

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ConnectionRefusedError` | The server is not running. Start `server.py` first. |
| `Address already in use` | Wait a few seconds or close the old server process, then try again. |
| No window appears | Make sure Tkinter is installed. |
| Can't connect from another computer | Check the host settings and firewall (see Configuration). |