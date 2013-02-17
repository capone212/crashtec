from crashtec.db.schema.types import DBSchemaTypes

_task = {
            'dump_file_name' : DBSchemaTypes.long_string()
        }

model = {"tasks" : _task,}