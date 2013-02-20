'''
Created on 20.02.2013

@author: anzor.apshev
'''
from crashtec.db.provider import routines as dbroutines
from crashtec.db.provider import filter as dbfilters
from crashtec.infrastructure.dbmodel import *  

# Create short name alias
_f = dbfilters.FieldFilterFactory

def register_agent(class_type, instance_name):
    cursor = dbroutines.select_from(AGENTS_TABLE, filter = _f(AGNETS_INSTANCE_FIELD) == instance_name)
    record = cursor.fetch_one()
    if record:
        print '-'*50
        dbroutines.update_record(AGENTS_TABLE, record)
        #todo: update
    else:
        new_record = dbroutines.Record();
        new_record[AGNETS_CLASS_TYPE_FIELD] = instance_name
        new_record[AGNETS_INSTANCE_FIELD] = class_type
        dbroutines.create_new_record(AGENTS_TABLE, new_record)
        
        
register_agent('sample_class', 'sample_instance@someserver')