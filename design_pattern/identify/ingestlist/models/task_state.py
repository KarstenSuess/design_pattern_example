from enum import Enum

class IngestListTaskState(Enum):
    Pending = 1
    Running = 2
    Completed = 3
    Failed = 4