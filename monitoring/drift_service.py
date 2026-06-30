import pandas as pd
from datasets import load_dataset
from evidently.presets import (
    DataDriftPreset,
    TargetDriftPreset,
    TextEvals,
)
from evidently.report import Report
from evidently.ui.workspace import Workspace

CURR_PATH = "/app/logs/current_production.csv"
WORKSPACE_PATH = "/app/evidently_workspace"

dataset = load_dataset("fklska/bert_sentiment_ds", split="train")
ref = pd.DataFrame(dataset)

curr = pd.read_csv(CURR_PATH)

ref = ref[["text", "label"]]
curr = curr[["text", "label"]]

drift_report = Report(metrics=[DataDriftPreset(), TargetDriftPreset(), TextEvals()])

drift_report.run(reference_data=ref, current_data=curr)

ws = Workspace.create(WORKSPACE_PATH)
project = ws.get_project("kinootziv_monitoring")
if not project:
    project = ws.create_project("kinootziv_monitoring")

ws.add_report(project.id, drift_report)
