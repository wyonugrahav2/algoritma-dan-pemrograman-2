"""
builder.py
Menerapkan Fluent Builder Pattern untuk memudahkan penyusunan rantai
eksekusi algoritma secara dinamis dan fleksibel melalui kodingan yang
mudah dibaca, misalnya:

    pipeline = (
        PipelineBuilder()
        .add_filter()
        .add_sort("quick")
        .add_search("binary")
        .build()
    )
"""

from typing import Any, Callable, List, Tuple

from src.components.filter_component import remove_invalid
from src.components.sorter_component import quick_sort_stage, merge_sort_stage
from src.components.searcher_component import binary_search_stage
from src.adapters.array_to_tree import array_to_tree_stage
from src.adapters.list_to_hash import list_to_hash_stage
from src.pipeline.runner import PipelineRunner

# Setiap stage function punya signature: fn(context) -> (context, message)
Stage = Callable[[Any], Tuple[Any, str]]

_STAGE_REGISTRY = {
    "filter:remove_invalid": remove_invalid,
    "sort:quick": quick_sort_stage,
    "sort:merge": merge_sort_stage,
    "search:binary": binary_search_stage,
    "adapt:array_to_tree": array_to_tree_stage,
    "adapt:list_to_hash": list_to_hash_stage,
}


class PipelineBuilder:
    """Membangun daftar stage secara fluent, lalu menghasilkan PipelineRunner."""

    def __init__(self):
        self._stages: List[Tuple[str, Stage]] = []

    def add_filter(self) -> "PipelineBuilder":
        self._stages.append(("filter:remove_invalid", remove_invalid))
        return self

    def add_sort(self, strategy: str = "quick") -> "PipelineBuilder":
        key = f"sort:{strategy}"
        if key not in _STAGE_REGISTRY:
            raise ValueError(f"Strategi sort '{strategy}' tidak dikenal.")
        self._stages.append((key, _STAGE_REGISTRY[key]))
        return self

    def add_search(self, strategy: str = "binary") -> "PipelineBuilder":
        key = f"search:{strategy}"
        if key not in _STAGE_REGISTRY:
            raise ValueError(f"Strategi search '{strategy}' tidak dikenal.")
        self._stages.append((key, _STAGE_REGISTRY[key]))
        return self

    def add_adapter(self, adapter_name: str) -> "PipelineBuilder":
        key = f"adapt:{adapter_name}"
        if key not in _STAGE_REGISTRY:
            raise ValueError(f"Adapter '{adapter_name}' tidak dikenal.")
        self._stages.append((key, _STAGE_REGISTRY[key]))
        return self

    def add_stage_by_name(self, stage_key: str) -> "PipelineBuilder":
        """Menambahkan stage berdasarkan key registry, dipakai saat
        menyusun pipeline dari config/pipeline_routes.py.
        """
        if stage_key not in _STAGE_REGISTRY:
            available = ", ".join(sorted(_STAGE_REGISTRY))
            raise ValueError(
                f"Stage '{stage_key}' tidak dikenal. Stage tersedia: {available}"
            )
        self._stages.append((stage_key, _STAGE_REGISTRY[stage_key]))
        return self

    def build(self, stop_on_failure: bool = True) -> PipelineRunner:
        if not self._stages:
            raise ValueError("Pipeline kosong: tambahkan minimal satu stage sebelum build().")
        return PipelineRunner(stages=list(self._stages), stop_on_failure=stop_on_failure)


def build_from_route(route_stage_names: List[str], stop_on_failure: bool = True) -> PipelineRunner:
    """Helper untuk membangun pipeline langsung dari daftar nama stage
    (biasanya berasal dari config.pipeline_routes.resolve_route()).
    """
    builder = PipelineBuilder()
    for stage_name in route_stage_names:
        builder.add_stage_by_name(stage_name)
    return builder.build(stop_on_failure=stop_on_failure)
