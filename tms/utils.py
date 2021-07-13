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
            self.cssClass = "index-col"
        else:
            self.name = name
            self.cssClass = cssClass
        self.field = field
        self.width = width
        self.minWidth = minWidth
        self.resizable = resizable
        self.selectable = selectable
        self.sortable = sortable
        

    
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

def normalize_data_without_id(raw_data):
    data = []
    for d in raw_data:
        p = d['fields']
        data.append(p)
    return data

def normalize(data):
    res = []
    i=1
    for k, v in data.items():
        v['id'] = i
        res.append(v)
        i=i+1
    return res

def normalize_col(data):
    res = []
    for k, v in data.items():
        x = ColDef(k, v['name'], v['id'])
        res.append(x)
    return res

def merge(query_data, join_on, index, value):
    
    res = {}
    res['data'] = {}
    res['columns'] ={"id": {"name": "S.N.", "id": "id"},
                    join_on :{"name": join_on, "id": join_on }
                    }
    for d  in query_data:
        for key in d:
           res = transform(d[key], join_on, index, value, res['data'], res['columns'])
    
    res['data'] = normalize(res['data'])
    res['columns'] = normalize_col(res['columns'])

    return res
        

def transform(query_data, join_on, index, value, data, columns):
    res = {}
    for d in query_data:
        suffix = d[index]
        key = d[join_on]
        data[key] = data.get(key, {})

        for k, v in d.items():
            id = k+"__%s"%suffix
            if k == index:
                continue
            elif k == join_on: 
               data[key][k]=v
            elif k == value:
                data[key][id] = v 
                columns[id] = { "name": "%s"%suffix, "id": id}
            else:
                data[key][id] = v
                # only results columns not any other. 
                    

    res['columns'] = columns
    res['data'] = data   
    return res
