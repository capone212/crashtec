from crashtec.db.schema.types import DBSchemaTypes

_task = {
            "dumpFileName" : DBSchemaTypes.long_string(), 
            "pubDate" : DBSchemaTypes.datetime(),
            "finishTime" : DBSchemaTypes.datetime(),
            "logFile" : DBSchemaTypes.long_string(),
            "resultFile" : DBSchemaTypes.long_string(),        
        }

model = {"task" : _task,}