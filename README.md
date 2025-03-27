# Bug Automation Tool

A Python-based automation tool that extracts bug information from Jira and exports it to Google Sheets automatically at scheduled intervals.

## Overview

This tool connects to Jira's API, retrieves bug information based on a configurable JQL query, and exports the data to a Google Sheets spreadsheet. It runs on a schedule, allowing for regular, automatic updates to the bug tracking sheet.

## Features

- Automatic export of bug data from Jira to Google Sheets
- Configurable export interval (default: 4 hours)
- Custom JQL query support for filtering bugs
- Labels filtering capability
- Date formatting for better readability
- Robust error handling and logging
- Supports both basic auth and token-based authentication for Jira

## Prerequisites

- Python 3.8+
- Jira account with API access
- Google Cloud account with Sheets API enabled
- Google Cloud service account with appropriate permissions

## Installation

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/souravLevel/Bug-Automation.git
   cd Bug-Automation
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project root with the following content:
   ```
   # Jira configuration
   JIRA_SERVER=https://your-jira-instance.atlassian.net
   JIRA_USERNAME=your-email@example.com
   JIRA_TOKEN=your-jira-api-token

   # Google Sheets configuration
   GOOGLE_SHEETS_CREDENTIALS_PATH=path/to/credentials.json
   GOOGLE_SHEETS_SPREADSHEET_ID=your-google-spreadsheet-id

   # Export configuration
   EXPORT_INTERVAL_HOURS=4
   JQL_QUERY=type = Bug AND status != Closed AND Labels in (android_bugs)
   ```

5. **Set up Google Sheets API:**
   - Create a project in the Google Cloud Console
   - Enable the Google Sheets API
   - Create a service account and download the credentials.json file
   - Share your target spreadsheet with the service account email

### Server Deployment (Ubuntu)

1. **Launch an Ubuntu EC2 instance** (t2.nano or larger)

2. **Install dependencies:**
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip python3-dev git
   sudo apt install -y python3.12-venv  # Adjust version if needed
   ```

3. **Clone the repository:**
   ```bash
   mkdir -p ~/projects
   cd ~/projects
   git clone https://github.com/souravLevel/Bug-Automation.git
   cd Bug-Automation
   ```

4. **Set up Python environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Configure the application:**
   - Create `.env` file as described above
   - Upload credentials.json to the server

6. **Setup PM2 for process management:**
   ```bash
   # Install Node.js and PM2
   sudo apt install -y nodejs npm
   sudo npm install -g pm2

   # Create run script
   echo '#!/bin/bash
   cd /home/ubuntu/projects/Bug-Automation
   source venv/bin/activate
   python main.py
   ' > ~/projects/Bug-Automation/run.sh
   chmod +x ~/projects/Bug-Automation/run.sh

   # Add to PM2
   pm2 start ~/projects/Bug-Automation/run.sh --name "bug-automation"
   pm2 save

   # Set PM2 to start on system boot
   pm2 startup
   # Run the command that PM2 provides
   ```

## Configuration Options

### Jira Configuration

- `JIRA_SERVER`: URL of your Jira instance
- `JIRA_USERNAME`: Email address associated with your Jira account
- `JIRA_TOKEN`: API token generated from your Jira account

### Google Sheets Configuration

- `GOOGLE_SHEETS_CREDENTIALS_PATH`: Path to the Google service account credentials JSON file
- `GOOGLE_SHEETS_SPREADSHEET_ID`: ID of the Google Sheet (found in the URL)

### Export Configuration

- `EXPORT_INTERVAL_HOURS`: How often the export should run (in hours)
- `JQL_QUERY`: JQL query to filter bugs (e.g., `type = Bug AND status != Closed AND Labels in (android_bugs)`)

## Project Structure

```
Bug-Automation/
├── main.py                  # Entry point script
├── requirements.txt         # Dependencies
├── .env                     # Configuration (not in repo)
├── credentials.json         # Google credentials (not in repo)
├── src/
│   ├── config/
│   │   └── settings.py      # Settings management
│   ├── exporters/
│   │   └── bug_exporter.py  # Main export logic
│   ├── services/
│   │   ├── jira_service.py  # Jira API interaction
│   │   └── sheets_service.py# Google Sheets interaction
│   └── utils/
│       └── logger.py        # Logging configuration
├── logs/                    # Log files directory
└── README.md                # Project documentation
```

## Troubleshooting

### Common Issues

1. **Jira Connection Issues:**
   - Verify your Jira credentials
   - Check if your token has expired
   - Ensure your account has API access permissions

2. **Google Sheets Issues:**
   - Verify the service account has editor access to the spreadsheet
   - Check if the credentials.json file is correctly formatted
   - Ensure the Google Sheets API is enabled in your Google Cloud Console

3. **Python Environment Issues:**
   - If modules are missing, ensure you've activated the virtual environment
   - Run `pip install -r requirements.txt` again to ensure all dependencies are installed

### Checking Logs

- **Local logs:** Check the `logs/` directory
- **Server logs with PM2:** Run `pm2 logs bug-automation` 

## Managing the Service

### PM2 Commands

- **Check status:** `pm2 status`
- **View logs:** `pm2 logs bug-automation`
- **Restart application:** `pm2 restart bug-automation`
- **Stop application:** `pm2 stop bug-automation`
- **Delete from PM2:** `pm2 delete bug-automation`
- **Monitor CPU/Memory:** `pm2 monit`

## License

[MIT License](LICENSE)

## Contributions

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

- [Jira Python Library](https://pypi.org/project/jira/)
- [Google API Python Client](https://github.com/googleapis/google-api-python-client)
- [Schedule](https://pypi.org/project/schedule/)
- [Python-dotenv](https://pypi.org/project/python-dotenv/)