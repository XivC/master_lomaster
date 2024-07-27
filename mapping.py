from typing import Callable, List
from model import *


def abit_from_json(json) -> Abit:
    return Abit(
        uid=json['uid'],
        avg_diploma_score=json['diploma_score'],
    )


def program_abit_from_json(json, index: int) -> ProgramAbit:
    return ProgramAbit(
        place=index,
        abit=abit_from_json(json),
        priority=json['priority'],
        score=json['score'],
        are_originals_passed=json['are_originals_passed'],
    )


def program_from_json(
        json,
        abits: Callable[[int], List[ProgramAbit]]
    ) -> Program:
    competitive_group_id = json['competitive_group_id']
    return Program(
        direction_title=json['direction_title'],
        abits=abits(competitive_group_id),
        budget_places=json['budget_min'],
        title=json['direction_title'],
        competitive_group_id=competitive_group_id,
    )