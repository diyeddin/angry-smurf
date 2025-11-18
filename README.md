# Angry Smurf Discord Bot 🤬

A hilariously over-the-top Discord bot that responds to messages with dramatic Arabic warnings, treating every innocent message as a grave offense.

## Features

- **Probability-based responses**: Gets progressively more likely to respond as users chat more
- **Arabic comedy**: Responds with theatrical Arabic warnings
- **Smart cooldowns**: Prevents spam with global and per-user rate limiting
- **Mention triggers**: Instant response when bot is mentioned
- **Testing mode**: Aggressive settings for testing in private servers
- **LLM-powered**: Uses Groq API for dynamic, contextual angry responses
- **Memory efficient**: Automatic cleanup of inactive user data
- **Docker support**: Easy deployment with Docker

## Setup

### Prerequisites

- Python 3.8+
- Discord Bot Token
- Groq API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/angry-smurf.git
   cd angry-smurf
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your tokens and settings
   ```

4. **Run the bot**
   ```bash
   python bot.py
   ```

### Docker Deployment

```bash
# Build the image
docker build -t angry-smurf .

# Run with environment file
docker run --env-file .env angry-smurf
```

## Configuration

### Required Environment Variables

- `DISCORD_TOKEN`: Your Discord bot token
- `CHANNEL_ID`: Discord channel ID to monitor
- `GROQ_API_KEY`: Your Groq API key

### Optional Settings

- `COOLDOWN`: Global cooldown between responses (default: 600s)
- `USER_COOLDOWN`: Per-user cooldown (default: 60s)
- `BASE_CHANCE`: Base probability of responding (default: 0.001)
- `SCALE_FACTOR`: Probability increase per message (default: 0.0005)

### Testing Mode

For testing in private servers:

```env
TESTING_MODE=true
TEST_CHANNEL_ID=your_test_channel_id
TEST_BASE_CHANCE=0.1
TEST_COOLDOWN=30
```

## How It Works

1. **Message Tracking**: Bot tracks each user's message count
2. **Escalating Probability**: More messages = higher chance of angry response
3. **Smart Triggers**: Mentions bypass all cooldowns and probability checks
4. **Arabic Responses**: LLM generates contextual Arabic warnings
5. **Rate Limiting**: Multiple cooldown layers prevent spam

### Example Response Flow

```
User: "hello"           (0.05% chance - no response)
User: "how are you?"    (0.075% chance - no response) 
User: "nice weather"    (0.1% chance - TRIGGERED!)
Bot: "@user هاد آخر إنذار! 'nice weather'?! تسامحت معك كتير..."
```

## Architecture

- `bot.py`: Main Discord client and event handling
- `config.py`: Configuration management and validation
- `llm_client.py`: Groq API integration with retry logic
- `message_tracker.py`: User tracking and probability calculations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Disclaimer

This bot is for entertainment purposes only. The "angry" responses are comedic and theatrical, not genuinely threatening or offensive.