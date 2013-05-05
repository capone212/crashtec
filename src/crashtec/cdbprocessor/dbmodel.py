from crashtec.db.schema.types import DBSchemaTypes

TASKS_TABLE ='tasks'
TASKS_DUMP_FILE_FIELD = 'dump_file_name'
TASKS_PROBLEM_ID = 'problem_id'
TASKS_PLATFORM_FIELD = 'platform'
TASKS_PROBLEM_CLASS = 'problem_class'
TASKS_SYMBOL_NAME = 'symbol_name'
TASKS_FAIL_IMAGE = 'failure_image_name'
TASKS_FAILURE_BUCKET_ID = 'failure_bucket_id'

_task = {
            TASKS_DUMP_FILE_FIELD : DBSchemaTypes.long_string(),
            TASKS_PROBLEM_ID : DBSchemaTypes.short_string(),
            TASKS_PLATFORM_FIELD : DBSchemaTypes.short_string(),
            TASKS_PROBLEM_CLASS: DBSchemaTypes.short_string(),
            TASKS_SYMBOL_NAME : DBSchemaTypes.long_string(),
            TASKS_FAIL_IMAGE : DBSchemaTypes.short_string(),
            TASKS_FAILURE_BUCKET_ID : DBSchemaTypes.long_string()
        } 

RAWRESULTS_TABLE = 'raw_results'
RAWRESULTS_TASK_ID = 'task_id'
RAWRESULTS_DBG_OUTPUT = 'debugger_output'

_raw_results = {
                RAWRESULTS_TASK_ID : DBSchemaTypes.int(),
                RAWRESULTS_DBG_OUTPUT : DBSchemaTypes.text_file()
               }
 

model = {TASKS_TABLE:_task, RAWRESULTS_TABLE:_raw_results}