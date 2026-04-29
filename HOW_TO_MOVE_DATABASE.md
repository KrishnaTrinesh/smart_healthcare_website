# How to Move MongoDB Database to Project Folder

Your MongoDB data is currently stored in `C:\Program Files\MongoDB\Server\8.2\data\`.

To move it into your project folder at `db\data\`, follow these steps:

## Quick Migration (Automated)

1. **Right-click** on PowerShell and select **"Run as Administrator"**

2. Navigate to your project folder:
   ```powershell
   cd "C:\Users\AKHIL\OneDrive\Desktop\kbn (2)\kbn\kbn"
   ```

3. Run the migration script:
   ```powershell
   .\Migrate-MongoDB-Data.ps1
   ```

4. Wait for the script to complete. It will:
   - Stop MongoDB service
   - Copy all data files to `db\data\`
   - Update MongoDB configuration
   - Start MongoDB service

5. Verify it worked:
   ```powershell
   mongosh smarthealthcare --eval "db.getCollectionNames()"
   ```
   You should see: `['users', 'doctors']`

## What Gets Changed

- **Data Location**: From Program Files → Project folder
- **MongoDB Config**: Updated to point to new location
- **Data Files**: All copied (users, doctors, etc.)

## After Migration

Your data will be stored at:
```
C:\Users\AKHIL\OneDrive\Desktop\kbn (2)\kbn\kbn\db\data\
```

This folder can be backed up, shared, or moved with your project!

## Files Created

- `Migrate-MongoDB-Data.ps1` - Automated migration script
- `db/mongod.conf` - MongoDB configuration file
- `db/README.md` - Detailed documentation
- `db/MIGRATION_INSTRUCTIONS.md` - Step-by-step guide

## Important Notes

⚠️ **Backup First**: The script creates a copy, but always have a backup!
⚠️ **Admin Rights**: Required to modify MongoDB configuration
⚠️ **Service Must Be Stopped**: The script does this automatically

