import oracledb

connection = oracledb.connect(
    user="system",
    password="1000",
    dsn="localhost:1521/ORCL" 
)
print("✅ Connected to Oracle 21c Enterprise Edition")
connection.close()
