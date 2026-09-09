"""
test_pipeline_flow.py
Uji alur data dari Stage A (filter) ke Stage B (sort) ke Stage C (search),
memastikan payload berubah sesuai ekspektasi tiap tahap (End-to-End Test).
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pipeline.builder import PipelineBuilder


def test_filter_then_sort():
    data = [5, None, 3, "", 1, 4, 2]
    pipeline = PipelineBuilder().add_filter().add_sort("quick").build()
    context = pipeline.run(initial_payload=data)

    assert context.failed is False
    assert context.payload == [1, 2, 3, 4, 5]
    assert len(context.history) == 2
    assert all(log.success for log in context.history)


def test_filter_sort_search_found():
    data = [10, 3, None, 7, 1, "", 9]
    pipeline = (
        PipelineBuilder()
        .add_filter()
        .add_sort("quick")
        .add_search("binary")
        .build()
    )
    context = pipeline.run(initial_payload=data, metadata={"search_target": 7})

    assert context.failed is False
    assert context.payload == [1, 3, 7, 9, 10]
    assert context.metadata["search_result"] == context.payload.index(7)


def test_filter_sort_search_not_found():
    data = [10, 3, 7, 1, 9]
    pipeline = (
        PipelineBuilder()
        .add_filter()
        .add_sort("merge")
        .add_search("binary")
        .build()
    )
    context = pipeline.run(initial_payload=data, metadata={"search_target": 999})

    assert context.failed is False
    assert context.metadata["search_result"] is None


if __name__ == "__main__":
    test_filter_then_sort()
    test_filter_sort_search_found()
    test_filter_sort_search_not_found()
    print("Semua test_pipeline_flow.py PASSED")
