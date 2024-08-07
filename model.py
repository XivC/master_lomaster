import dataclasses
import uuid


@dataclasses.dataclass
class Abit:
    uid: str
    avg_diploma_score: float


@dataclasses.dataclass
class ProgramAbit:
    abit: Abit
    priority: int
    place: int
    score: float
    are_originals_passed: bool

    def __gt__(self, other):
        return self.place > other.place

    def __ge__(self, other):
        return self.place >= other.place

    def __lt__(self, other):
        return self.place < other.place

    def __le__(self, other):
        return self.place <= other.place


@dataclasses.dataclass
class Program:
    direction_title: str
    abits: list[ProgramAbit]
    budget_places: int
    title: str
    competitive_group_id: int
