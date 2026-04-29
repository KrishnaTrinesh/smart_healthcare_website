# MongoDB Configuration

This folder contains the MongoDB database for the Smart Healthcare system.

## Directory Structure

```
db/
├── data/          # MongoDB data files (created automatically)
├── logs/          # MongoDB log files (created automatically)
├── mongod.conf    # MongoDB configuration file
└── README.md      # This file
```

## Starting MongoDB

To start MongoDB using this local configuration:

### Option 1: Using the batch file (Windows)
```
Start-MongoDB.bat
```

### Option 2: Manual start
```
mongod --config db\mongod.conf
```

### Option 3: Using the MongoDB service
If you want to change the default MongoDB data location permanently:

1. Stop MongoDB service:
   ```
   net stop MongoDB
   ```

2. Edit the config file at:
   `C:\Program Files\MongoDB\Server\8.2\bin\mongod.cfg`
   
   Change:
   ```
   storage:
     dbPath: C:\Program Files\MongoDB\Server\8.2\data
   ```
   
   To:
   ```
   storage:
     dbPath: <full path to kbn folder>\db\data
   ```

3. Start MongoDB service:
   ```
   net start MongoDB
   ```

## Notes

- Data is stored locally in the project folder
- Database name: `smarthealthcare`
- Collections: `users`, `doctors`
- The application connects to `mongodb://localhost:27017`

