from typing import List

# nn layers
LAYERS: List[int] = [50, 50, 1]

# nn input-output
INPUT_LAYER_LEN: int = LAYERS[0]
assert LAYERS[-1] == 1

# learn/predicate
LEARN_TIMES: int = 100
PREDICT_STEPS: int = 30
