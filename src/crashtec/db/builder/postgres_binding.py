from crashtec.db.schema.types import DBSchemaTypes

EXPECTED_RESULT = {'task': {'finishTime': 'datetime', 'status': 'short_string', 'analyseAgent': 'string', 
                                    'pubDate': 'datetime', 'dumpFileName': 'long_string', 'user_name': 'short_string', 
                                    'logFile': 'long_string', 'resultFile': 'long_string'}}

#CREATE TABLE films (
#    code        char(5) CONSTRAINT firstkey PRIMARY KEY,
#    title       varchar(40) NOT NULL,
#    did         integer NOT NULL,
#    date_prod   date,
#    kind        varchar(10),
#    len         interval hour to minute
#);

TYPES_MAPPING = { 
    DBSchemaTypes.int() : 'integer',
    DBSchemaTypes.bool() : 'boolean',
    DBSchemaTypes.float() : 'real',
    DBSchemaTypes.datetime() : 'timestamp',
    DBSchemaTypes.short_string() : 'varchar(32)',
    DBSchemaTypes.string() : 'varchar(256)',
    DBSchemaTypes.long_string() : 'varchar(1024)',
    DBSchemaTypes.autoincrement() : 'serial PRIMARY KEY'
}

def generate_table_sql(table_name, fields):
    fields_sql = str()
    # generate table fields_sql schema
    for field_name in fields.keys():
        if fields_sql:
            fields_sql += ",\n"
        type = fields[field_name]
        fields_sql += " %s %s" % (field_name, TYPES_MAPPING[type])
    fields_sql = "CREATE TABLE %s (\n%s\n);" % (table_name, fields_sql)
    return fields_sql

def test(input_dict):
    for table_name in input_dict.keys() :
        print generate_table_sql(table_name, input_dict[table_name])
    print "-"*60
        
    
#test(EXPECTED_RESULT)