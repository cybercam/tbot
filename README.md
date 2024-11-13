# UPSC Telegram Quiz Bot

A Telegram bot designed specifically for UPSC exam preparation, featuring automatic question condensing, domain-specific abbreviations, and quiz management.

## Features

- **Automatic Text Condensing**: Intelligently condenses long questions and answers to fit Telegram's poll limits
- **UPSC-Specific Abbreviations**: Built-in dictionary of UPSC-related terms and their abbreviations
- **Domain Recognition**: Automatically detects and applies domain-specific abbreviations (Governance, Economy, International Relations, etc.)
- **Quiz Format Support**: Supports multiple-choice questions with explanations
- **Telegram Poll Integration**: Creates interactive quiz polls with correct answer highlighting

## Prerequisites

- Python 3.7 or higher
- python-telegram-bot library (version 20.0 or higher)
- A Telegram Bot Token from [@BotFather](https://t.me/botfather)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/upsc-quiz-bot.git
cd upsc-quiz-bot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create `upsc_abbreviations.json` file in the project root directory

4. Configure your bot token in the code or environment variables

## Configuration

### Bot Token
Replace the placeholder token in `tbot.py`:
```python
bot_token = 'YOUR_BOT_TOKEN_HERE'
```

### Abbreviations
The bot uses a JSON file for abbreviations. Create `upsc_abbreviations.json` with your preferred abbreviations or use the default one provided.

## Usage

1. Start the bot:
```bash
python tbot.py
```

2. In Telegram, start the bot with `/start`

3. Send quiz questions in the following format:
```
What is your question?
a) First option
b) Second option
c) Correct option*
d) Fourth option
exp: Your explanation
```

Note: Mark the correct answer with an asterisk (*)

## Message Format Limits

- Question length: 300 characters
- Option length: 100 characters
- Maximum options: 10

## Example

Input:
```
Which one of the following statements about the Chief Justice of India is correct?
a) Appointment requires Parliamentary approval*
b) The tenure is fixed for 5 years
c) Can act as President when both President and Vice President offices are vacant
d) None of the above
exp: The CJI is appointed by the President of India
```

## Project Structure

```
upsc-quiz-bot/
│
├── tbot.py                     # Main bot code
├── upsc_abbreviations.json     # Abbreviations database
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── bot_log.txt                # Log file (created when bot runs)
```

## Error Handling

The bot includes comprehensive error handling for:
- Message format errors
- Length limit violations
- Network issues
- Invalid inputs

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter) - email@example.com

Project Link: [https://github.com/yourusername/upsc-quiz-bot](https://github.com/yourusername/upsc-quiz-bot)

## Acknowledgments

- [python-telegram-bot](https://python-telegram-bot.org/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
