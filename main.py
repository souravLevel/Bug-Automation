import os
import sys
import traceback

# Ensure project root is in Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

import schedule
import time

def setup_python_path():
    """Ensure all project directories are in Python path"""
    base_path = os.path.abspath(os.path.dirname(__file__))
    src_path = os.path.join(base_path, 'src')
    sys.path.insert(0, base_path)
    sys.path.insert(0, src_path)
    print("Python path:", sys.path)

def main():
    try:
        # Setup Python path
        setup_python_path()

        # Import after path setup
        from src.config.settings import Settings
        from src.exporters.bug_exporter import BugExporter
        from src.utils.logger import Logger

        # Initialize logger
        logger = Logger(__name__)
        
        # Load settings
        settings = Settings()
        
        # Create bug exporter
        exporter = BugExporter(settings)
        
        # Schedule export
        export_interval = settings.export_config['interval_hours']
        schedule.every(export_interval).hours.do(exporter.run_export)
        
        logger.info(f"Bug export scheduled every {export_interval} hours")
        
        # Immediately run the first export
        exporter.run_export()
        
        # Keep the script running
        while True:
            schedule.run_pending()
            time.sleep(1)
    
    except Exception as e:
        print("Critical error in main execution:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()