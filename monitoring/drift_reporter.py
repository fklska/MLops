import pandas as pd
from evidently.metric_preset import DataDriftPreset
from evidently.report import Report
from evidently.ui.workspace import RemoteWorkspace


def collect_and_send_drift(reference_path: str, current_df: pd.DataFrame):
    reference_df = pd.read_parquet(reference_path)

    drift_report = Report(metrics=[DataDriftPreset()])
    drift_report.run(reference_data=reference_df, current_data=current_df)

    URL = "http://evidently-service.kinootziv-app.svc.cluster.local:9999"
    ws = RemoteWorkspace(URL)

    projects = ws.list_projects()
    target_project = None
    for p in projects:
        if p.name == "BERT Data Drift":
            target_project = p
            break

    if target_project:
        ws.add_report(target_project.id, drift_report)
