from model import *
import mapping
import json
from abc import ABC, abstractmethod


class ProgramsRepository(ABC):
    @abstractmethod
    def read_program_abits(self, competitive_group_id: int) -> list[ProgramAbit]:
        pass

    @abstractmethod
    def read_programs(self) -> list[Program]:
        pass


class JsonProgramsRepository(ProgramsRepository):
    def __init__(self, db_path: str) -> None:
        super().__init__()
        self.db_path = db_path

    def read_program_abits(self, competitive_group_id: int) -> list[ProgramAbit]:
        with open(f'{self.db_path}/{competitive_group_id}.json', 'r') as group_file:
            group_json = json.load(group_file)
            return list(
                map(
                    lambda item: mapping.program_abit_from_json(item[1], item[0]),
                    enumerate(group_json)
                ),
            )
        
    def read_programs(self) -> list[Program]:
        with open(f'{self.db_path}/programs.json', 'r') as programs_file:
            programs_json = json.load(programs_file)
            return list(
                map(
                    lambda item: mapping.program_from_json(
                        item,
                        abits=lambda id: self.read_program_abits(id)
                    ),
                    programs_json
                )
            )
