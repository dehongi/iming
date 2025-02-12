# Django Instant Messaging

A real-time instant messaging application built with Django, demonstrating the use of WebSocket technology for instant communication. This project serves as a practical example of implementing real-time features in Django applications.

## Features

- Real-time messaging using WebSocket
- Public and private messaging
- Online user status tracking
- Message persistence
- Automatic reconnection handling
- User authentication
- Responsive design

## Technology Stack

- **Backend Framework**: Django 5.1
- **WebSocket Implementation**: Django Channels
- **ASGI Server**: Daphne
- **Message Broker**: Redis
- **Database**: SQLite (default)
- **Frontend**: Vanilla JavaScript with WebSocket API

## Prerequisites

- Python 3.12+
- Redis Server
- Virtual Environment (recommended)

## Installation

1. Clone the repository

```bash
git clone https://github.com/dehongi/iming.git
cd iming
```

2. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies

```bash
pip install django==5.1.6
pip install channels
pip install daphne
pip install channels-redis
```

4. Set up Redis (Required for WebSocket)

```bash
# On Ubuntu/Debian
sudo apt-get install redis-server
sudo service redis-server start

# On macOS with Homebrew
brew install redis
brew services start redis
```

5. Apply database migrations

```bash
python manage.py makemigrations accounts
python manage.py makemigrations iming
python manage.py migrate
```

6. Create a superuser (admin account)

```bash
python manage.py createsuperuser
```

## Running the Application

1. Make sure Redis server is running
2. Start the Daphne server:

```bash
daphne django_project.asgi:application
```

3. Access the application at `http://localhost:8000`

## Usage

1. Register a new account or log in with existing credentials
2. The main chat interface provides:
   - List of online users in the sidebar
   - Chat history in the main area
   - Message input form at the bottom
3. Sending messages:
   - To send a public message: Type your message and click Send
   - To send a private message: Select a user from the dropdown, type your message, and click Send
4. Features:
   - Real-time message delivery
   - Online/offline status updates
   - Message persistence (chat history)
   - Automatic reconnection if connection is lost

## Project Structure

```
django_project/          # Project configuration
├── settings.py         # Project settings
├── asgi.py            # ASGI configuration with Channels
├── routing.py         # WebSocket routing
└── urls.py            # URL routing

accounts/               # User authentication app
├── models.py          # Custom user model
└── views.py           # Authentication views

iming/                  # Main chat application
├── consumers.py       # WebSocket consumer
├── models.py          # Message model
├── urls.py            # App URLs
└── views.py           # Chat view

templates/             # HTML templates
├── base.html         # Base template
└── registration/     # Auth templates
    ├── login.html    # Login page
    └── signup.html   # Registration page
```

## Key Components

### WebSocket Consumer (iming/consumers.py)
Handles real-time communication including:
- Message broadcasting
- Private messaging
- Online status tracking
- Message history

### Message Model (iming/models.py)
Stores chat messages with:
- Sender information
- Message content
- Timestamp
- Private message handling

### Authentication
Uses Django's built-in authentication with a custom user model and includes:
- User registration
- Login/logout functionality
- User session management

## Channel Layer Configuration

The project uses Redis as the channel layer backend. Configuration in settings.py:
```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Author

Hamed Dehongi

## Acknowledgments

- Django Channels documentation
- Django documentation
- The Python community

## Disclaimer

This application is created for demonstration purposes and might not be suitable for production use without additional security measures and optimizations.

