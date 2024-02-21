from dataclasses import dataclass

@dataclass
class CollatedMetrics:
    cpu: int
    requested_cpu: int