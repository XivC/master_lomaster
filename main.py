from model import *
from repository import *

programs_repository: ProgramsRepository = JsonProgramsRepository(db_path='database__1723029208')
abits = programs_repository.read_program_abits(1914)
abits = [
    abit for abit in abits if abit.priority <= 3
                              and (abit.are_originals_passed or abit.abit.uid == "15929946835")
]

for idx, abit in enumerate(abits):
    if abit.abit.uid == "15929946835":
        print(idx, abit)