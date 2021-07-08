from django.db.models.base import ModelBase
from django.db.models import Model
import json
import datetime
import decimal

class ColDef():
    
    def __init__(self, idx, name, field, width=120, minWidth=50, 
                 resizable=True, selectable= True, sortable= True, cssClass= None):
        self.id = idx
        if name.upper() == 'ID':
            self.name = 'S.N.'
        else:
            self.name = name    
        self.field = field
        self.width = width
        self.minWidth = minWidth
        self.resizable = resizable
        self.selectable = selectable
        self.sortable = sortable
        self.cssClass = cssClass

    
class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S") #return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d") #return obj.isoformat()
        elif isinstance(obj, decimal.Decimal):  # isinstance() is better than type(), because it handles inheritance
            return str(obj)
        elif isinstance(obj, ColDef):
            return obj.__dict__
        else:
            return super(MyJSONEncoder, self).default(obj)
        
def get_fields_name(obj):
    fields = []
    if isinstance(obj, Model):
        for key in obj._meta.fields:
            if key.name == 'id': continue
            fields.append(key.name)
    elif isinstance(obj, ModelBase):
        for key in obj._meta.fields:
            if key.name == 'id': continue
            fields.append(key.name)
    return fields

def get_grid_cols_def(obj):
    columns = []
    if isinstance(obj, ModelBase):
        for key in obj._meta.fields:
            x = ColDef(key.name, key.name, key.name)
            columns.append(x)
    elif isinstance(obj, Model):
        for key in obj._meta.fields:
            if key.name == 'id': continue
            x = ColDef(key.name, key.name, key.name)
            columns.append(x)
    elif isinstance(obj, list):
        for key in obj:
            x = ColDef(key, key, key)
            columns.append(x)
    #return json.dumps(columns, cls=MyJSONEncoder)
    return columns

def normalize_data(raw_data):
    data = []
    for d in raw_data:
        p = d['fields']
        p['id'] = d['pk']
        data.append(p)
    return data