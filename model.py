import dataclasses
import uuid


@dataclasses.dataclass
class Abit:
    uid: str
    avg_diploma_score: float
    score: float


@dataclasses.dataclass
class ProgramAbit:
    abit: Abit
    priority: int
    place: int
    are_originals_passed: bool


@dataclasses.dataclass
class Program:
    direction_title: str
    abits: list[ProgramAbit]
    budget_places: int
    title: str
    competitive_group_id: int
