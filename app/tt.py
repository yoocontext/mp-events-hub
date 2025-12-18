from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Father(ABC):
    _events: list[str] = field(default_factory=list)

    def apply(self, t: str):
        self._events.append(t)
        self.when(t=t)

    @abstractmethod
    def when(self, t: str):
        ...


class Soon(Father):
    def when(self, t: str):
        print(t)



t = Soon()


t.apply("bob")
print(t._events)

