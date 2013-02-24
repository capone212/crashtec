'''
Created on 20.02.2013

@author: anzor.apshev
'''
from crashtec.db.provider import routines as dbroutines
from crashtec.db.provider import filter as dbfilters
from crashtec.infrastructure.dbmodel import *  
import datetime

# Create short name alias
_f = dbfilters.FieldFilterFactory

def register_agent(class_type, instance_name):
    cursor = dbroutines.select_from(AGENTS_TABLE, filter = _f(AGNETS_INSTANCE_FIELD) == instance_name)
    record = cursor.fetch_one()
    is_exist = True
    if not record:
        record = dbroutines.Record()
        record[AGNETS_INSTANCE_FIELD] = instance_name
        is_exist = False
    record[AGNETS_CLASS_TYPE_FIELD] = class_type
    record[AGNETS_REGISTRED_TIME_FIELD] = datetime.datetime.now()
    record[AGNETS_KEEPALIVE_FIELD] = datetime.datetime.now()
    if is_exist:
        dbroutines.update_record(AGENTS_TABLE, record)
    else:      
        dbroutines.create_new_record(AGENTS_TABLE, record)

def send_keepalive_message(instance_name):
    record = {AGNETS_INSTANCE_FIELD : instance_name,  AGNETS_KEEPALIVE_FIELD: datetime.datetime.now()}
    dbroutines.update_record(AGENTS_TABLE, record, key_field = AGNETS_INSTANCE_FIELD)
    pass
        
#register_agent('sample_class', 'sample_instance@someserver')
#send_keepalive_message('sample_instance@someserver')