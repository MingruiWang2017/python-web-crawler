import MySQLdb
import dj_database_url
from twisted.enterprise import adbapi

url = "mysql://root:pass@192.168.73.130:3406/properties"
params = dj_database_url.parse(url)

conn_kwargs = {}
conn_kwargs['host'] = params['HOST']
conn_kwargs['user'] = params['USER']
conn_kwargs['passwd'] = params['PASSWORD']
conn_kwargs['db'] = params['NAME']
conn_kwargs['port'] = params['PORT']

# 建立连接
pool = adbapi.ConnectionPool('MySQLdb',  use_unicode=True, connect_timeout=5, **conn_kwargs)
conn = adbapi.Connection(pool)
tx = adbapi.Transaction(pool, conn)

# 执行SQL
sql = 'select * from properties'
result = tx.execute(sql)
print(result)
print(tx.fetchall())

tx.close()
conn.close()
pool.close()
