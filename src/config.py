from typing import Tuple

# nn params
INPUT_LAYER_LEN: int = 20
LAYERS: Tuple[Tuple[int, int]] = ((INPUT_LAYER_LEN, 1),)

# learn/predicate
LEARN_TIMES: int = 300
PREDICT_STEPS: int = 30
