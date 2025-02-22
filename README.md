# Telegram Bot - Content Management

A simple Telegram bot for managing and displaying content with favorites functionality, built using Python and SQLite.

## Features

- **Paginated Content Navigation**: Users can view content one page at a time with navigation controls (Next, Previous).
- **Favorites Management**: Users can add and remove content from their favorites list.
- **Search**: Users can search for specific content (optional feature for future enhancements).
- **Database Integration**: All user interactions (current page, favorites) are stored in a SQLite database.
- **Environment Configuration**: Use environment variables for secure token storage.

## Installation

### Prerequisites

Make sure you have the following installed:
- Python 3.7 or higher
- `pip` (Python package manager)

### Steps to Install

1. **Clone the repository**:
    ```bash
    git clone https://github.com/javadyeganeh1/Newbot.git
    cd Newbot
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:
    Create a `.env` file in the root directory and add your Telegram bot token:
    ```
    TELEGRAM_BOT_TOKEN=your-telegram-bot-token
    ```

4. **Run the bot**:
    ```bash
    python src/bot.py
    ```

### Development

To run tests:
```bash
pytest
```
