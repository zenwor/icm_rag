# This script is being used as a part of JetBrains Internship Application Test Task.
# As such, it has not been modified. All the credits go to the authors.

# mypy: disable-error-code="call-arg"
# flake8: noqa

from abc import ABC, abstractmethod
from typing import List


class BaseChunker(ABC):
    @abstractmethod
    def split_text(self, text: str) -> List[str]:
        pass
