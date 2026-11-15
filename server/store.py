"""Durable application records; existing diagnostic tables are untouched."""
import os
import psycopg
from psycopg.types.json import Jsonb
from contextlib import contextmanager

def connect():
    c=psycopg.connect(os.environ['DATABASE_URL'],connect_timeout=10,autocommit=True)
    c.execute("SET statement_timeout='15s'")
    return c

def initialise():
    with connect() as c:
        c.execute('CREATE TABLE IF NOT EXISTS finn_records (kind text, id text, data jsonb NOT NULL, updated_at timestamptz NOT NULL DEFAULT now(), PRIMARY KEY(kind,id))')

def get(kind,key,default=None):
    with connect() as c:
        row=c.execute('SELECT data FROM finn_records WHERE kind=%s AND id=%s',(kind,key)).fetchone()
    return row[0] if row else default

def put(kind,key,data):
    with connect() as c:
        c.execute('INSERT INTO finn_records(kind,id,data) VALUES(%s,%s,%s) ON CONFLICT(kind,id) DO UPDATE SET data=EXCLUDED.data,updated_at=now()',(kind,key,Jsonb(data)))
    return data

def all_records(kind):
    with connect() as c:
        return [r[0] for r in c.execute('SELECT data FROM finn_records WHERE kind=%s ORDER BY id',(kind,)).fetchall()]

def for_ticker(kind,ticker):
    with connect() as c:
        return [r[0] for r in c.execute("SELECT data FROM finn_records WHERE kind=%s AND data->>'ticker'=%s ORDER BY id",(kind,ticker)).fetchall()]

@contextmanager
def lock(name):
    """Session lock releases on crash/disconnect; checkpoints are separate commits."""
    with connect() as c:
        acquired=c.execute('SELECT pg_try_advisory_lock(hashtextextended(%s,0))',(name,)).fetchone()[0]
        try:
            yield acquired
        finally:
            if acquired:c.execute('SELECT pg_advisory_unlock(hashtextextended(%s,0))',(name,))
