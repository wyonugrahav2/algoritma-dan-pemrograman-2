"""
pipeline_configs.py
Mendefinisikan skema data dan aturan transformasi yang dapat digunakan
oleh stream_chain untuk memvalidasi serta memproses tiap baris data.
"""

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional


@dataclass
class FieldSchema:
    """Skema satu kolom/field dalam sebuah rekaman data."""
    name: str
    dtype: type = str
    required: bool = True
    default: Optional[object] = None


@dataclass
class PipelineSchema:
    """Kumpulan FieldSchema yang merepresentasikan struktur satu record."""
    fields: List[FieldSchema] = field(default_factory=list)

    def field_names(self) -> List[str]:
        return [f.name for f in self.fields]

    def as_dict(self) -> Dict[str, FieldSchema]:
        return {f.name: f for f in self.fields}


# Skema contoh default — dapat digantikan sesuai kebutuhan dataset nyata
DEFAULT_SCHEMA = PipelineSchema(
    fields=[
        FieldSchema(name="id", dtype=str, required=True),
        FieldSchema(name="value", dtype=float, required=False, default=0.0),
        FieldSchema(name="category", dtype=str, required=False, default="unknown"),
    ]
)


# Registry aturan transformasi: nama -> fungsi transformasi(record) -> record
TransformFn = Callable[[dict], dict]

TRANSFORM_REGISTRY: Dict[str, TransformFn] = {}


def register_transform(name: str):
    """Decorator untuk mendaftarkan fungsi transformasi ke registry global."""
    def decorator(fn: TransformFn) -> TransformFn:
        TRANSFORM_REGISTRY[name] = fn
        return fn
    return decorator


@register_transform("strip_strings")
def strip_strings(record: dict) -> dict:
    return {
        k: (v.strip() if isinstance(v, str) else v)
        for k, v in record.items()
    }


@register_transform("lowercase_keys")
def lowercase_keys(record: dict) -> dict:
    return {k.lower(): v for k, v in record.items()}
