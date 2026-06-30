import os

import pandas as pd
from datasets import load_dataset
from evidently import Report
from evidently.presets import (
    DataDriftPreset,
    TextEvals,
)
from evidently.ui.workspace import Workspace
from sqlalchemy import create_engine

DB_HOST = os.getenv("POSTGRES_SERVER", "localhost")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_NAME = os.getenv("POSTGRES_DB", "postgres")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
WORKSPACE_PATH = "/app/evidently_workspace"

try:
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    query = "SELECT description, label_id FROM review ORDER BY id DESC LIMIT 10000;"
    curr = pd.read_sql_query(query, engine)
except Exception:
    ws = Workspace.create(WORKSPACE_PATH)
    project = next((p for p in ws.list_projects() if p.name == "kinootziv_monitoring"), None)
    if not project:
        ws.create_project("kinootziv_monitoring")
    exit(0)

if curr.empty:
    ws = Workspace.create(WORKSPACE_PATH)
    project = next((p for p in ws.list_projects() if p.name == "kinootziv_monitoring"), None)
    if not project:
        ws.create_project("kinootziv_monitoring")
    exit(0)

curr.columns = ["text", "label"]

dataset = load_dataset("fklska/bert_sentiment_ds", split="train").shuffle(42).select(range(10000))
ref = pd.DataFrame(dataset)
ref = ref[["text", "label"]]

drift_report = Report(metrics=[DataDriftPreset(), TextEvals()])
drift_report.run(reference_data=ref, current_data=curr)

ws = Workspace.create(WORKSPACE_PATH)
project = next((p for p in ws.list_projects() if p.name == "kinootziv_monitoring"), None)
if not project:
    project = ws.create_project("kinootziv_monitoring")

ws.add_report(project.id, drift_report)
