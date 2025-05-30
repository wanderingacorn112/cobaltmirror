"""Top‑level package for the Cobalt Mirror enrichment layer."""
from importlib.metadata import version

__all__ = [
    "build_pipeline",
    "geocode_place",
    "normalise_times",
    "link_entities",
]

__version__ = version("cobaltmirror-enrichment")

from .nlp_pipeline import build_pipeline  # noqa: E402
from .geocode import geocode_place        # noqa: E402
from .temporal import normalise_times     # noqa: E402
from .linker import link_entities         # noqa: E402