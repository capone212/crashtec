from crashtec.db.schema.types import DBSchemaTypes

# tasks table definition 
TASKS_TABLE ='tasks'

TASKS_AGENT_INSTANCE_FIELD = 'agent_instance_name'
TASKS_AGENT_CLASS_FIELD = 'agent_class_type'
TASKS_AGENTS_GROUP_ID = 'agent_group_id'
TASKS_STATUS_FIELD = 'status'
TASKS_PLATFORM_FIELD = 'platform'

_task = { 
            TASKS_AGENT_INSTANCE_FIELD : DBSchemaTypes.short_string(),
            TASKS_AGENT_CLASS_FIELD :  DBSchemaTypes.short_string(),
            TASKS_AGENTS_GROUP_ID : DBSchemaTypes.short_string(),
            TASKS_STATUS_FIELD : DBSchemaTypes.short_string(),
            TASKS_PLATFORM_FIELD : DBSchemaTypes.short_string()
        }

AGENTS_TABLE = 'agents'
AGENTS_CLASS_TYPE_FIELD = 'class_type'
AGENTS_INSTANCE_FIELD = 'instance_name'
AGENTS_REGISTRED_TIME_FIELD = 'registered_time'
AGENTS_KEEPALIVE_FIELD = 'last_keepalive'
AGENTS_GROUP_FIELD = 'group_id'

_agents = {
            AGENTS_CLASS_TYPE_FIELD : DBSchemaTypes.short_string(),
            AGENTS_INSTANCE_FIELD :  DBSchemaTypes.string(),
            AGENTS_REGISTRED_TIME_FIELD :  DBSchemaTypes.datetime(),
            AGENTS_KEEPALIVE_FIELD :  DBSchemaTypes.datetime(),
            AGENTS_GROUP_FIELD : DBSchemaTypes.short_string()
           }

model = {TASKS_TABLE : _task, AGENTS_TABLE : _agents}