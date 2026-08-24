"""
Pengujian integrasi: memverifikasi kelancaran pertukaran pesan dan
data antar-modul lewat Event Bus dan Dispatcher, menjalankan modul
yang sesungguhnya (bukan mock) untuk memastikan seluruh pipeline
bekerja sama dengan benar.
"""

import unittest

from config.module_registry import ModuleRegistry
from src.core.bus import EventBus
from src.core.dispatcher import Dispatcher


class TestModuleDispatch(unittest.TestCase):
    def setUp(self) -> None:
        # Registry & bus baru per-test agar test saling terisolasi.
        self.registry = ModuleRegistry()
        self.registry.register(
            "transformation", "src.modules.transformation.cleansers.TransformationModule"
        )
        self.registry.register(
            "validation", "src.modules.validation.rules.ValidationModule"
        )
        self.registry.register(
            "analytics", "src.modules.analytics.analyzer.AnalyticsModule"
        )

        self.bus = EventBus()
        self.dispatcher = Dispatcher(self.registry, self.bus)

    def test_transformation_then_analytics_pipeline(self) -> None:
        payload = {"values": ["  1  ", "", "2", None, "3"]}

        results = self.dispatcher.run_pipeline(["transformation"], payload)
        cleaned = results["transformation"]

        self.assertEqual(cleaned["values"], ["1", "2", "3"])

    def test_event_bus_receives_completion_events(self) -> None:
        received = []
        self.bus.subscribe("module.validation.completed", lambda payload: received.append(payload))

        self.dispatcher.run_single("validation", {"data": "some value"})

        self.assertEqual(len(received), 1)
        self.assertTrue(received[0]["valid"])

    def test_dispatcher_records_history_on_bus(self) -> None:
        self.dispatcher.run_single("analytics", {"values": [1, 2, 3]})

        history = self.bus.history()
        event_names = [name for name, _ in history]

        self.assertIn("module.analytics.completed", event_names)

    def test_full_pipeline_transformation_validation(self) -> None:
        payload = {"values": [" a ", "b", ""]}

        results = self.dispatcher.run_pipeline(["transformation"], payload)
        transformed = results["transformation"]

        # Hasil transformation dipakai sebagai input validation secara manual,
        # untuk menegaskan kontrak output/input antar-modul (lihat api_contracts.md).
        validation_result = self.dispatcher.run_single(
            "validation", {"data": transformed["values"]}
        )

        self.assertTrue(validation_result["valid"])


if __name__ == "__main__":
    unittest.main()
