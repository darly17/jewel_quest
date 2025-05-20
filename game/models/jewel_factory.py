from typing import List, Dict, Tuple, Optional, Any
from .jewel import *

class JewelFactory:
    def __init__(self, jewels_config: List[Dict]):
        self.jewels_config = jewels_config
        self.type_count = len(jewels_config)

    def create_jewel(self, jewel_type: int, x: int, y: int) -> Jewel:
        if not 0 <= jewel_type < self.type_count:
            raise ValueError(f"Invalid jewel type: {jewel_type}")
        return Jewel(jewel_type, x, y, self.jewels_config[jewel_type])

    def create_random_jewel(self, x: int, y: int) -> Jewel:
        return self.create_jewel(random.randint(0, self.type_count - 1), x, y)