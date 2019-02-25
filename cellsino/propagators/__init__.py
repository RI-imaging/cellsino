from .pp_rytov import Rytov
from .pp_projection import Projection

prop_dict = {
    "projection": Projection,
    "rytov": Rytov,
}

available = sorted(prop_dict.keys())
