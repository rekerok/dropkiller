from .swapper import Swapper
from .odos import Odos
from .one_inch import One_Inch

dex_swap = {
    "odos": Odos,
    "1inch": One_Inch,
}