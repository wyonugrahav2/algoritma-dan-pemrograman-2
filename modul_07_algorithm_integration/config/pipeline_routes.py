"""
pipeline_routes.py
Pemetaan kombinasi strategi (route) siap pakai, misalnya:
    "clean_sort_search" -> Filter -> Quick Sort -> Binary Search

Route ini dipakai oleh CLI (main.py) agar pengguna cukup menyebut nama
route tanpa perlu menyusun pipeline manual lewat builder tiap kali.
"""

# Setiap route adalah daftar nama stage yang akan dipasang berurutan
# ke dalam PipelineBuilder. Nama-nama ini harus cocok dengan yang
# dikenali oleh builder.add_stage_by_name().
PIPELINE_ROUTES = {
    "clean_sort_search": [
        "filter:remove_invalid",
        "sort:quick",
        "search:binary",
    ],
    "clean_sort_only": [
        "filter:remove_invalid",
        "sort:quick",
    ],
    "sort_to_tree": [
        "filter:remove_invalid",
        "sort:merge",
        "adapt:array_to_tree",
    ],
    "dedupe_to_hash": [
        "filter:remove_invalid",
        "adapt:list_to_hash",
    ],
}


def resolve_route(route_name: str):
    """Mengembalikan daftar nama stage untuk sebuah route.

    Melempar KeyError dengan pesan yang jelas jika route tidak dikenal,
    supaya CLI bisa menampilkan pesan galat yang ramah pengguna.
    """
    if route_name not in PIPELINE_ROUTES:
        available = ", ".join(sorted(PIPELINE_ROUTES))
        raise KeyError(
            f"Route '{route_name}' tidak ditemukan. Pilihan yang tersedia: {available}"
        )
    return PIPELINE_ROUTES[route_name]
