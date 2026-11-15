"""Read-only Neon check. Never log connection strings or driver errors."""
import json
import os
from dotenv import load_dotenv
import psycopg
load_dotenv()
try:
    with psycopg.connect(os.environ['DATABASE_URL'],connect_timeout=15) as conn:
        result=conn.execute('SELECT 1').fetchone()[0]
        # pg_stat_ssl behind a pooler describes its upstream hop, not this client.
        ssl=conn.pgconn.ssl_in_use
    print(json.dumps({'database_query':result==1,'client_tls':bool(ssl)}))
except Exception as exc:
    print(json.dumps({'database_query':False,'error_type':type(exc).__name__,'details':'Credential and driver error omitted'}))
    raise SystemExit(1)
