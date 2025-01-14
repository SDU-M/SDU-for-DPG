from clickhouse_driver import Client

client = Client(host='clickhouse', port=9000, user='default', password='')
result = client.execute('SELECT version()')
print(f"ClickHouse Version: {result[0][0]}")
