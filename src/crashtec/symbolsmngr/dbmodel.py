'''
Created on 14.03.2013

@author: capone
'''
from crashtec.db.schema.types import DBSchemaTypes


TASKS_TABLE ='tasks'
TASKS_DUMP_FILE_FIELD = 'dump_file_name'
_task = {
            TASKS_DUMP_FILE_FIELD : DBSchemaTypes.long_string()
        } 
 
#------------------------------------------------------------    
SYMBOLS_TABLE = 'binary_symbols'
SYMBOLS_URL = 'url'
SYMBOLS_LOCAL_DIR = 'lical_dir_path'
SYMBOLD_TRANSACTION_ID = 'symsrv_transaction_id'
_symbols = {
                SYMBOLS_URL : DBSchemaTypes.long_string(),
                SYMBOLS_LOCAL_DIR : DBSchemaTypes.long_string(),
                SYMBOLD_TRANSACTION_ID :  DBSchemaTypes.short_string()
           }

#------------------------------------------------------------
PRODUCTS_TABLE = 'products'
PRODUCTS_PRODUCT_ID = 'product_id'
PRODUCTS_NAME = 'product_name'
_products = {
                PRODUCTS_PRODUCT_ID : DBSchemaTypes.short_string(),
                PRODUCTS_NAME : DBSchemaTypes.string() 
             }

#------------------------------------------------------------
BRANCHES_TABLE = 'product_branches'
BRANCHES_PRODUCT_ID = 'product_id'
BRANCHES_BRANCH_ID = 'branch_id'
BRANCHES_BRANCH_NAME = 'branch_name'
_branches = {
                BRANCHES_PRODUCT_ID : DBSchemaTypes.short_string(),
                BRANCHES_BRANCH_ID : DBSchemaTypes.short_string(),
                BRANCHES_BRANCH_NAME : DBSchemaTypes.string(),
             }

#---------------------------------------------------------------
IMAGES2PROD = 'imagename2products'
IMAGES2PROD_PRODUCT_ID = 'product_id'
IMAGES2PROD_RE_IMAGENAME = 're_imagename'
_products2imagename = {
                       IMAGES2PROD_RE_IMAGENAME : DBSchemaTypes.long_string(),
                        IMAGES2PROD_PRODUCT_ID : DBSchemaTypes.short_string()
                       }

#---------------------------------------------------------------
VERSIONS2BRANCHES = 'imageversions2branches'
VERSIONS2BRANCHES_RE_VERSION = 're_image_version'
VERSIONS2BRANCHES_BRANCH_ID = 'branch_id'
VERSIONS2BRANCHES_PRODUCT_ID = 'product_id'

_versions2branches = {
                        VERSIONS2BRANCHES_RE_VERSION : DBSchemaTypes.long_string(),
                        VERSIONS2BRANCHES_BRANCH_ID : DBSchemaTypes.short_string(),
                        VERSIONS2BRANCHES_PRODUCT_ID : DBSchemaTypes.short_string() 
                     }

#---------------------------------------------------------------
BRANCHES2BINARY = 'branches2binary'
BRANCHES2BINARY_BRANCH_ID = 'branch_id'
BRANCHES2BINARY_BINARY_URL = 're_binary_url'
_branches2binary = {
                        BRANCHES2BINARY_BRANCH_ID : DBSchemaTypes.short_string(),
                        BRANCHES2BINARY_BINARY_URL : DBSchemaTypes.long_string()
                    }


#---------------------------------------------------------------
model = {
            SYMBOLS_TABLE : _symbols,
            TASKS_TABLE : _task, 
            PRODUCTS_TABLE : _products,
            BRANCHES_TABLE : _branches,
            IMAGES2PROD : _products2imagename,
            VERSIONS2BRANCHES : _versions2branches,
            BRANCHES2BINARY : _branches2binary
         }


