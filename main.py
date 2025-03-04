import sys
import logging
from dotenv import load_dotenv
from src.core.config import AppConfig
from src.core.logging_config import setup_logging
from src.presentation.app import Application
# import pytesseract

def main():
    try:
        # Load environment variables
        load_dotenv()
        
        # Setup logging
        logger = setup_logging()
        
        logger.info("Uygulama başlatılıyor...")
        
        # Initialize configuration
        config = AppConfig()
        
        # Create and run application
        app = Application(config)
        app.run()
        
    except Exception as e:
        logging.error(f"Application failed to start: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()