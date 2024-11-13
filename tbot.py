import sys
import json
import re
import logging
from pathlib import Path
from telegram import Update, Poll
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_log.txt'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Constants for Telegram Poll Limits
POLL_OPTION_MAX_LENGTH = 100
POLL_QUESTION_MAX_LENGTH = 300
POLL_MAX_OPTIONS = 10

# Load UPSC abbreviations
def load_abbreviations():
    try:
        # First try to load from external file
        file_path = Path('upsc_abbreviations.json')
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # If file doesn't exist, create it with default abbreviations
            default_abbrevs = {
                # [Previous abbreviations dictionary content goes here]
                # Copy the content from the first artifact above
            }
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(default_abbrevs, f, indent=4)
            return default_abbrevs
    except Exception as e:
        logger.error(f"Error loading abbreviations: {str(e)}")
        return {}

DOMAIN_ABBREVIATIONS = load_abbreviations()

def truncate_text(text, max_length, add_ellipsis=True):
    """Truncate text to max length, optionally adding ellipsis"""
    if len(text) <= max_length:
        return text
    truncated = text[:max_length-3] if add_ellipsis else text[:max_length]
    return truncated + '...' if add_ellipsis else truncated

def apply_abbreviations(text):
    """Apply all relevant abbreviations to the text"""
    modified_text = text
    for domain in DOMAIN_ABBREVIATIONS.values():
        for full, abbr in domain.items():
            pattern = re.compile(r'\b' + re.escape(full) + r'\b', re.IGNORECASE)
            modified_text = pattern.sub(abbr, modified_text)
    return modified_text

def smart_condense(text, max_length):
    """Smart condense text with abbreviations and length limit"""
    # First apply abbreviations
    condensed = apply_abbreviations(text)
    
    # If still too long, truncate
    if len(condensed) > max_length:
        condensed = truncate_text(condensed, max_length)
    
    return condensed

async def handle_quiz_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle quiz input with abbreviations and length limits"""
    try:
        input_text = update.message.text
        lines = input_text.split('\n')
        
        # Process question and options
        question_lines = []
        options = []
        correct_answer = None
        explanation = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith(('a)', 'b)', 'c)', 'd)')):
                option_text = line[2:].strip()
                if option_text.endswith('*'):
                    correct_answer = len(options)
                    option_text = option_text[:-1].strip()
                
                # Apply abbreviations and truncate if needed
                option_text = smart_condense(option_text, POLL_OPTION_MAX_LENGTH)
                options.append(option_text)
                
            elif line.startswith('exp:'):
                explanation = line[4:].strip()
            else:
                question_lines.append(line)
        
        # Combine and condense question
        question_text = ' '.join(question_lines)
        question_text = smart_condense(question_text, POLL_QUESTION_MAX_LENGTH)
        
        # Show preview of condensed content
        preview = (
            "Preview of condensed content:\n\n"
            f"Question: {question_text}\n\n"
            "Options:\n"
        )
        for i, opt in enumerate(options):
            preview += f"{chr(97+i)}) {opt}\n"
        
        await update.message.reply_text(preview)
        
        # Create poll
        await context.bot.send_poll(
            chat_id=update.effective_chat.id,
            question=question_text,
            options=options,
            type=Poll.QUIZ,
            correct_option_id=correct_answer,
            explanation=explanation,
            is_anonymous=True
        )
        
    except Exception as e:
        await update.message.reply_text(
            f"Error: {str(e)}\n\n"
            "Telegram Poll Limits:\n"
            f"- Option length: {POLL_OPTION_MAX_LENGTH} characters\n"
            f"- Question length: {POLL_QUESTION_MAX_LENGTH} characters\n"
            f"- Maximum options: {POLL_MAX_OPTIONS}"
        )

async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command"""
    instructions = (
        "Welcome to the UPSC Quiz Bot!\n\n"
        "Please provide your questions following these limits:\n"
        f"- Option length: {POLL_OPTION_MAX_LENGTH} characters max\n"
        f"- Question length: {POLL_QUESTION_MAX_LENGTH} characters max\n"
        f"- Maximum options: {POLL_MAX_OPTIONS}\n\n"
        "The bot will automatically:\n"
        "1. Apply UPSC-related abbreviations\n"
        "2. Condense long content\n"
        "3. Show you a preview before creating the poll\n\n"
        "Format example:\n"
        "Your question here?\n"
        "a) First option\n"
        "b) Second option\n"
        "c) Correct option*\n"
        "d) Fourth option\n"
        "exp: Your explanation"
    )
    await update.message.reply_text(instructions)

def main():
    """Initialize and start the bot"""
    try:
        # Bot token
        bot_token = ''
        
        # Create application
        application = Application.builder().token(bot_token).build()
        
        # Add handlers
        application.add_handler(CommandHandler('start', start_quiz))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_quiz_input))
        
        print("Bot is running! Press Ctrl+C to stop.")
        
        # Start polling
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        print(f"Critical error: {str(e)}")
    
    finally:
        print("\nPress Enter to exit...")
        input()

if __name__ == '__main__':
    main()
