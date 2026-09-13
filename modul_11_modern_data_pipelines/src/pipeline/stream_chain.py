"""
stream_chain.py
Mensejajarkan fungsi-fungsi generator secara bersambung (Yield Pipeline).
Ini adalah inti dari pendekatan Lazy Evaluation: tidak ada tahap yang
mengeksekusi apa pun sampai konsumen terakhir (sink) mulai menarik data.
"""

from typing import Iterator, Callable, List, Dict, Any


Stage = Callable[[Iterator[Dict[str, Any]]], Iterator[Dict[str, Any]]]


class StreamChain:
    """
    Menyusun beberapa stage generator menjadi satu pipeline tunggal.

    Contoh:
        chain = StreamChain(source_iterator)
        chain.add_stage(cleanser.process)
        chain.add_stage(enricher.process)
        for record in chain.run():
            ...
    """

    def __init__(self, source: Iterator[Dict[str, Any]]):
        self._source = source
        self._stages: List[Stage] = []

    def add_stage(self, stage: Stage) -> "StreamChain":
        """Menambahkan satu tahap pemrosesan (harus berupa generator/iterable)."""
        self._stages.append(stage)
        return self

    def run(self) -> Iterator[Dict[str, Any]]:
        """
        Merangkai seluruh stage menjadi satu iterator akhir.
        Tidak ada komputasi terjadi di sini — baru dieksekusi saat
        di-iterasi oleh pemanggil (sink/consumer), sesuai prinsip
        Lazy Evaluation.
        """
        current = self._source
        for stage in self._stages:
            current = stage(current)
        return current

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        return self.run()
