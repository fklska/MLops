import os

import pandas as pd
import psycopg2
from datasets import load_dataset
from evidently import Report
from evidently.presets import (
    DataDriftPreset,
    TextEvals,
)
from evidently.ui.workspace import Workspace

DB_HOST = os.getenv("POSTGRES_SERVER", "localhost")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_NAME = os.getenv("POSTGRES_DB", "postgres")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

WORKSPACE_PATH = "/app/evidently_workspace"

dataset = load_dataset("fklska/bert_sentiment_ds", split="train").shuffle(42).select(range(10000))
ref = pd.DataFrame(dataset)

conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)
query = "SELECT description, label_id FROM review ORDER BY id DESC LIMIT 10000;"

curr = pd.read_sql_query(query, conn)
conn.close()

if curr.empty:
    ws = Workspace.create(WORKSPACE_PATH)
    if not ws.get_project("kinootziv_monitoring"):
        ws.create_project("kinootziv_monitoring")
    exit(0)

curr.columns = ["text", "label"]
ref = ref[["text", "label"]]


drift_report = Report(metrics=[DataDriftPreset(), TextEvals()], include_tests=True)

drift_report.run(reference_data=ref, current_data=curr)

ws = Workspace.create(WORKSPACE_PATH)
project = ws.get_project("kinootziv_monitoring")
if not project:
    project = ws.create_project("kinootziv_monitoring")

ws.add_report(project.id, drift_report)
