from crashtec.db.schema.types import DBSchemaTypes

TASKS_TABLE ='tasks'
TASKS_DUMP_FILE_FIELD = 'dump_file_name'
TASKS_PROBLEM_ID = 'problem_id'

_task = {
            TASKS_DUMP_FILE_FIELD : DBSchemaTypes.long_string(),
            TASKS_PROBLEM_ID : DBSchemaTypes.short_string()
        }

model = {TASKS_TABLE : _task,}