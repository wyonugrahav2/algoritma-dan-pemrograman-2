"""
main.py
Entry Point (Orchestrator utama) sistem Advanced IPO CLI.
Menghubungkan Input Layer -> Process Layer -> Output Layer
tanpa mencampur logika bisnis dengan mekanisme I/O.
"""

import sys

from src.domain.exceptions import IPOBaseException
from src.infrastructure.logger import get_logger
from src.input_layer.cli_readers import read_cli_arguments, read_interactive_input, read_from_string
from src.input_layer.parsers import parse_to_float
from src.domain.models import ExportRequest
from src.output_layer.exporters import export_report
from src.output_layer.presenters import print_report
from src.process_layer.ipo_engine import IPOEngine

logger = get_logger(__name__)


def collect_values(args) -> list:
    """Mengumpulkan daftar RawInput dari CLI flag atau input interaktif."""
    raw_inputs = []

    if args.values:
        raw_inputs.append(read_from_string(args.values, source="cli_flag"))
        # --values menerima format "1,2,3" -> diparsing langsung sebagai list
        from src.input_layer.parsers import parse_to_list
        validated = parse_to_list(raw_inputs[0])
        return validated.value

    print("Mode interaktif. Masukkan nilai numerik satu per satu.")
    print("Ketik 'selesai' untuk mengakhiri input.\n")

    values = []
    while True:
        raw = read_interactive_input(prompt=f"Nilai #{len(values) + 1} (atau 'selesai'): ")
        if raw.raw_value.strip().lower() == "selesai":
            break
        try:
            validated = parse_to_float(raw)
            values.append(validated.value)
        except IPOBaseException as exc:
            print(f"  Input tidak valid: {exc}")

    return values


def main() -> int:
    """Titik masuk utama aplikasi."""
    args = read_cli_arguments()
    logger.info("Sistem Advanced IPO CLI dimulai.")

    try:
        values = collect_values(args)
        if not values:
            print("Tidak ada data untuk diproses. Program dihentikan.")
            return 1

        engine = IPOEngine()
        report = engine.process_numeric_dataset(values)

        print_report(report, output_format=args.format)

        if args.export:
            file_format = args.export.rsplit(".", 1)[-1] if "." in args.export else "json"
            request = ExportRequest(
                file_format=file_format,
                destination_path=args.export,
                payload=None,
            )
            saved_path = export_report(request, report)
            print(f"\nHasil berhasil diekspor ke: {saved_path}")

        logger.info("Sistem Advanced IPO CLI selesai dengan sukses.")
        return 0

    except IPOBaseException as exc:
        logger.error(f"Terjadi kegagalan domain IPO: {exc}")
        print(f"\n[ERROR] {exc}")
        return 1
    except KeyboardInterrupt:
        print("\nDibatalkan oleh pengguna.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
