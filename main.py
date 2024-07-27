from model import *
from repository import *

programs_repository: ProgramsRepository = JsonProgramsRepository(db_path='<db_path>')
programs = programs_repository.read_programs()
print(programs)