from crashtec.db.schema.types import DBSchemaTypes

_task = {
            "dumpFileName" : DBSchemaTypes.long_string(), 
            "pubDate" : DBSchemaTypes.datetime(),
            "finishTime" : DBSchemaTypes.datetime(),
            "status" : DBSchemaTypes.short_string(),
            "analyseAgent" : DBSchemaTypes.string(),
            "user" : DBSchemaTypes.short_string()        
        }

model = {"task" : _task,}