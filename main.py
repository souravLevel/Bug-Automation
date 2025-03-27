import schedule
import time
from src.config.settings import Settings
from src.exporters.bug_exporter import BugExporter
from src.utils.logger import Logger

def main():
    # Initialize logger
    logger = Logger(__name__)
    
    try:
        # Load settings
        settings = Settings()
        
        # Create bug exporter
        exporter = BugExporter(settings)
        
        # Schedule export
        export_interval = settings.export_config['interval_hours']
        schedule.every(export_interval).hours.do(exporter.run_export)
        
        logger.info(f"Bug export scheduled every {export_interval} hours")
        
        # Keep the script running
        while True:
            schedule.run_pending()
            time.sleep(1)
    
    except Exception as e:
        logger.error(f"Critical error in main execution: {e}")

if __name__ == '__main__':
    main()