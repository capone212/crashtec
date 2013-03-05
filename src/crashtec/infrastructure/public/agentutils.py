'''
Created on 20.02.2013

@author: anzor.apshev
'''
from crashtec.db.provider import routines as dbroutines
from crashtec.db.provider import filter as dbfilters
from crashtec.infrastructure.dbmodel import *  
import datetime

GROUP_ID_UNSET = str()

# Create short name alias
_f = dbfilters.FieldFilterFactory

def register_agent(class_type, instance_name, group_id = GROUP_ID_UNSET):
    cursor = dbroutines.select_from(AGENTS_TABLE, filter = _f(AGENTS_INSTANCE_FIELD) == instance_name)
    record = cursor.fetch_one()
    is_exist = True
    if not record:
        record = dbroutines.Record()
        record[AGENTS_INSTANCE_FIELD] = instance_name
        is_exist = False
    record[AGENTS_CLASS_TYPE_FIELD] = class_type
    record[AGENTS_REGISTRED_TIME_FIELD] = datetime.datetime.now()
    record[AGENTS_KEEPALIVE_FIELD] = datetime.datetime.now()
    record[AGENTS_GROUP_FIELD] = group_id
    if is_exist:
        dbroutines.update_record(AGENTS_TABLE, record)
    else:      
        dbroutines.create_new_record(AGENTS_TABLE, record)

def send_keepalive_message(instance_name):
    record = {AGENTS_INSTANCE_FIELD : instance_name,  AGENTS_KEEPALIVE_FIELD: datetime.datetime.now()}
    dbroutines.update_record(AGENTS_TABLE, record, key_field = AGENTS_INSTANCE_FIELD)
    pass
        
#register_agent('sample_class', 'sample_instance@someserver')
#send_keepalive_message('sample_instance@someserver')