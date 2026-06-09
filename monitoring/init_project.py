from evidently.renderers.html_widgets import WidgetSize
from evidently.ui.dashboards import (
    DashboardPanelCounter,
    DashboardPanelPlot,
    PanelValue,
    PlotType,
    ReportFilter,
)
from evidently.ui.workspace import RemoteWorkspace

URL = "http://evidently-service.kinootziv-app.svc.cluster.local:9999"
ws = RemoteWorkspace(URL)

project = ws.create_project("BERT Data Drift")
project.description = "Мониторинг отклонения данных"

project.dashboard.add_panel(
    DashboardPanelCounter(
        title="Всего отчетов",
        filter=ReportFilter(metadata_values={}, tag_values=[]),
        value=PanelValue.COUNTER,
        size=WidgetSize.HALF,
    )
)

project.dashboard.add_panel(
    DashboardPanelPlot(
        title="Доля дрейфующих признаков",
        filter=ReportFilter(metadata_values={}, tag_values=[]),
        metric_id="DatasetDriftMetric",
        metric_fingerprint=None,
        metric_args={},
        value=PanelValue.metric_value("share_of_drifted_columns"),
        plot_type=PlotType.LINE,
        size=WidgetSize.FULL,
    )
)

project.save()
