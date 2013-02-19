from crashtec.db.schema.types import DBSchemaTypes

# tasks table definition 
TASKS_TABLE ='tasks'

AGENT_INSTANCE_FIELD = 'agent_instance_name'
AGENT_CLASS_FIELD = 'agent_class_type'
STATUS_FIELD = 'status'

_task = { 
            AGENT_INSTANCE_FIELD : DBSchemaTypes.short_string(),
            AGENT_CLASS_FIELD :  DBSchemaTypes.short_string(),
            STATUS_FIELD : DBSchemaTypes.short_string()        
        }


model = {TASKS_TABLE : _task,}