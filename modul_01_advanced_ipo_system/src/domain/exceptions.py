"""
exceptions.py
Hirarki custom exception untuk domain logika IPO.
Setiap layer melempar exception spesifik agar penanganan galat presisi.
"""

from config.constants import ErrorCode


class IPOBaseException(Exception):
    """Exception dasar untuk seluruh sistem IPO."""

    def __init__(self, message: str, error_code: ErrorCode = None):
        self.message = message
        self.error_code = error_code
        super().__init__(f"[{error_code.value if error_code else 'E0000'}] {message}")


# --- Input Layer Exceptions ---

class InputValidationError(IPOBaseException):
    """Dilempar saat data masukan gagal lolos validasi."""

    def __init__(self, message: str):
        super().__init__(message, ErrorCode.INVALID_INPUT_TYPE)


class ValueOutOfRangeError(IPOBaseException):
    """Dilempar saat nilai masukan berada di luar batas ambang batas."""

    def __init__(self, message: str):
        super().__init__(message, ErrorCode.VALUE_OUT_OF_RANGE)


class EmptyInputError(IPOBaseException):
    """Dilempar saat masukan kosong atau hanya berisi whitespace."""

    def __init__(self, message: str = "Input tidak boleh kosong."):
        super().__init__(message, ErrorCode.EMPTY_INPUT)


class ParsingError(IPOBaseException):
    """Dilempar saat konversi string ke tipe data terstruktur gagal."""

    def __init__(self, message: str):
        super().__init__(message, ErrorCode.PARSING_FAILED)


# --- Process Layer Exceptions ---

class ProcessExecutionError(IPOBaseException):
    """Dilempar saat terjadi kegagalan pada saat eksekusi proses bisnis."""

    def __init__(self, message: str):
        super().__init__(message, ErrorCode.PROCESS_FAILURE)


class PipelineBrokenError(IPOBaseException):
    """Dilempar saat salah satu tahap pipeline gagal dan mematahkan rantai."""

    def __init__(self, message: str):
        super().__init__(message, ErrorCode.PIPELINE_BROKEN)


# --- Output Layer Exceptions ---

class ExportError(IPOBaseException):
    """Dilempar saat penyimpanan hasil ke berkas eksternal gagal."""

    def __init__(self, message: str):
        super().__init__(message, ErrorCode.EXPORT_FAILED)


class UnsupportedFormatError(IPOBaseException):
    """Dilempar saat format ekspor/tampilan yang diminta tidak didukung."""

    def __init__(self, message: str):
        super().__init__(message, ErrorCode.UNSUPPORTED_FORMAT)
