from crashtec.db.schema.types import DBSchemaTypes

TASKS_TABLE ='tasks'
TASKS_DUMP_FILE_FIELD = 'dump_file_name'
TASKS_PROBLEM_ID = 'problem_id'
TASKS_PLATFORM_FIELD = 'platform' 

_task = {
            TASKS_DUMP_FILE_FIELD : DBSchemaTypes.long_string(),
            TASKS_PROBLEM_ID : DBSchemaTypes.short_string(),
            TASKS_PLATFORM_FIELD : DBSchemaTypes.short_string()
        } 

model = {"task" : _task,}