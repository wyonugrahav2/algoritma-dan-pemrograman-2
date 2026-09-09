"""
test_failure_recovery.py
Uji rollback jika salah satu stage gagal/error: pipeline harus berhenti
(stop_on_failure=True) dan mempertahankan payload terakhir yang valid,
atau melanjutkan dengan payload apa adanya jika stop_on_failure=False.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pipeline.builder import PipelineBuilder
from src.pipeline.runner import PipelineRunner


def _always_fails_stage(context):
    raise RuntimeError("Simulasi kegagalan stage sengaja untuk pengujian")


def test_pipeline_stops_on_failure_by_default():
    builder = PipelineBuilder().add_filter()
    # Sisipkan stage buatan yang pasti gagal, lalu stage sort setelahnya.
    builder._stages.append(("simulated:fail", _always_fails_stage))
    builder.add_sort("quick")

    pipeline = builder.build(stop_on_failure=True)
    context = pipeline.run(initial_payload=[3, 1, 2])

    assert context.failed is True
    # Stage sort setelah kegagalan seharusnya TIDAK dijalankan.
    executed_stages = [log.stage_name for log in context.history]
    assert "sort:quick" not in executed_stages
    assert executed_stages[-1] == "simulated:fail"


def test_pipeline_continues_when_configured():
    builder = PipelineBuilder().add_filter()
    builder._stages.append(("simulated:fail", _always_fails_stage))
    builder.add_sort("quick")

    pipeline = builder.build(stop_on_failure=False)
    context = pipeline.run(initial_payload=[3, 1, 2])

    assert context.failed is True  # tercatat gagal...
    executed_stages = [log.stage_name for log in context.history]
    # ...tapi tetap lanjut mengeksekusi stage berikutnya.
    assert "sort:quick" in executed_stages


if __name__ == "__main__":
    test_pipeline_stops_on_failure_by_default()
    test_pipeline_continues_when_configured()
    print("Semua test_failure_recovery.py PASSED")
