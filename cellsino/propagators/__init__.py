from .pp_rytov import Rytov
from .pp_projection import Projection

dictionary = {
    "projection": Projection,
    "rytov": Rytov,
}

available = sorted(dictionary.keys())
