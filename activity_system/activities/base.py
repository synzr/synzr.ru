from abc import ABC, abstractmethod
from ..activity_result import ActivityResult


class BaseActivity(ABC):
    @abstractmethod
    def get_current_activity(self) -> ActivityResult:
        raise NotImplementedError()

