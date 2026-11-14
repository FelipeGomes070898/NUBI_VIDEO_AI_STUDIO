from backend.database import init_db, connect
from ai.director import make_plan
from ai.ltx.client import LTXClient, LTXError

def test_director_plan():
 p=make_plan("Origem das estrelas",duration=60)
 assert len(p["scenes"])==5 and abs(sum(x["duration"] for x in p["scenes"])-60)<1

def test_database_schema():
 init_db()
 with connect() as c:
  tables={r[0] for r in c.execute("select name from sqlite_master where type='table'")}
 assert {"projects","scenes","assets","generation_jobs","render_jobs","engine_integrations","settings","logs","usage_records","users"}<=tables

def test_ltx_requires_secret():
 c=LTXClient(api_key="")
 try:c._headers()
 except LTXError as e:assert "LTX_API_KEY" in str(e)
 else:assert False
