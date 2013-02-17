from crashtec.db.schema.types import DBSchemaTypes

_task = { 
            'agent_instance_name' : DBSchemaTypes.short_string(),
            'agent_class_type' :  DBSchemaTypes.short_string(),
            'status' : DBSchemaTypes.short_string()        
        }

model = {"tasks" : _task,}