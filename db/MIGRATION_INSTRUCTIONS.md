# MongoDB Data Migration Instructions

## Current Situation
- MongoDB data is stored in: `C:\Program Files\MongoDB\Server\8.2\data`
- You want to move it to: `<project folder>\db\data`

## Migration Steps

### Method 1: Change MongoDB Configuration (Recommended)

This permanently changes where MongoDB stores its data.

#### Step 1: Stop MongoDB Service
Run PowerShell as Administrator and execute:
```powershell
net stop MongoDB
```

#### Step 2: Copy Data Files
Copy the MongoDB data directory:
```powershell
# Make sure the target directory exists
mkdir "C:\Users\AKHIL\OneDrive\Desktop\kbn (2)\kbn\kbn\db\data"

# Copy all data files
robocopy "C:\Program Files\MongoDB\Server\8.2\data" "C:\Users\AKHIL\OneDrive\Desktop\kbn (2)\kbn\kbn\db\data" /E /COPYALL
```

#### Step 3: Update MongoDB Configuration
Edit the configuration file:
```powershell
notepad "C:\Program Files\MongoDB\Server\8.2\bin\mongod.cfg"
```

Change line 5 from:
```yaml
  dbPath: C:\Program Files\MongoDB\Server\8.2\data
```

To your project path:
```yaml
  dbPath: C:\Users\AKHIL\OneDrive\Desktop\kbn (2)\kbn\kbn\db\data
```

#### Step 4: Start MongoDB
```powershell
net start MongoDB
```

#### Step 5: Verify Data
```powershell
mongosh smarthealthcare --eval "db.getCollectionNames()"
```

You should see: `['users', 'doctors']`

---

### Method 2: Use Local MongoDB Instance (Alternative)

Run a separate MongoDB instance using the local config.

#### Step 1: Export Existing Data
```powershell
cd "C:\Users\AKHIL\OneDrive\Desktop\kbn (2)\kbn\kbn"
python db\export_and_migrate_data.py
```

#### Step 2: Start Local MongoDB Instance
```powershell
mongod --config db\mongod.conf
```

#### Step 3: Import Data
```powershell
mongosh smarthealthcare --eval "load('./db/backup/users.json')"
```

---

## Verification

After migration, verify your data:

```powershell
mongosh smarthealthcare
```

Then run:
```javascript
use smarthealthcare
db.users.countDocuments()
db.doctors.countDocuments()
```

---

## Important Notes

- **Backup First**: Always backup your data before migration
- **Permissions**: Method 1 requires Administrator privileges
- **Service**: Method 1 modifies the system MongoDB service
- **Instance**: Method 2 runs a separate MongoDB instance
- **Port Conflict**: Only one MongoDB instance can run on port 27017

---

## Troubleshooting

### "Cannot bind to port 27017"
Stop the MongoDB service before running a local instance:
```powershell
net stop MongoDB
```

### "Access Denied"
Run PowerShell as Administrator

### "Data directory not found"
Make sure the db/data directory exists before starting MongoDB

