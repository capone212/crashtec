from crashtec.db.schema.types import DBSchemaTypes

TASKS_TABLE ='tasks'
TASKS_DUMP_FILE_FIELD = 'dump_file_name'
_task = {
            TASKS_DUMP_FILE_FIELD : DBSchemaTypes.long_string()
        }

model = {TASKS_TABLE : _task,}