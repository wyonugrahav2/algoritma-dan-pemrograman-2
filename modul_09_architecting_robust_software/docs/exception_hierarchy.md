# Exception Hierarchy

```
AppException (base_exceptions.py)
│
├── ValidationError (validation_errors.py)
│   ├── InvalidInputError
│   ├── MissingFieldError
│   └── OutOfRangeError
│
└── ExecutionError (execution_errors.py)
    ├── OperationTimeoutError
    ├── ResourceUnavailableError
    ├── UnexpectedFailureError
    │
    ├── CircuitOpenError        (resilience/circuit_breaker.py)
    ├── RetryExhaustedError     (resilience/retry_handler.py)
    └── FallbackFailedError     (resilience/fallback_manager.py)
```

## Kontrak `AppException`

Setiap exception kustom membawa:

- `message`: penjelasan teknis untuk developer/log.
- `error_code`: kode standar (lihat `config/error_codes.py`) untuk pelacakan.
- `timestamp`: waktu kejadian (UTC, ISO-8601).
- `cause`: exception asal (opsional), untuk chaining.
- `to_dict()`: representasi terstruktur untuk crash report / audit log.

Dengan hirarki ini, kode pemanggil bisa menangani error secara presisi
(misalnya hanya menangkap `ValidationError`) tanpa perlu memeriksa jenis
string pesan secara manual.
