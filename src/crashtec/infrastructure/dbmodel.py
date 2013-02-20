from crashtec.db.schema.types import DBSchemaTypes

# tasks table definition 
TASKS_TABLE ='tasks'

TASKS_AGENT_INSTANCE_FIELD = 'agent_instance_name'
TASKS_AGENT_CLASS_FIELD = 'agent_class_type'
TASKS_STATUS_FIELD = 'status'

_task = { 
            TASKS_AGENT_INSTANCE_FIELD : DBSchemaTypes.short_string(),
            TASKS_AGENT_CLASS_FIELD :  DBSchemaTypes.short_string(),
            TASKS_STATUS_FIELD : DBSchemaTypes.short_string()        
        }



AGENTS_TABLE = 'agents'
AGNETS_CLASS_TYPE_FIELD = 'class_type'
AGNETS_INSTANCE_FIELD = 'instance_name'
_agents = {
            AGNETS_CLASS_TYPE_FIELD : DBSchemaTypes.short_string(),
            AGNETS_INSTANCE_FIELD :  DBSchemaTypes.short_string()  
           }




model = {TASKS_TABLE : _task, AGENTS_TABLE : _agents}