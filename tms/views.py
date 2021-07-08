from tms.fixtures.dummy_data import product, testresults
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.core import serializers
from tms.utils import MyJSONEncoder, get_grid_cols_def, normalize_data
import json
from django.apps import apps

# Create your views here.
def index(request):
    
    return render(request, 'tms/index.html')

def get_all_products(request):
    qs = Product.objects.select_related().all()
    raw_data = serializers.serialize('python', qs, use_natural_foreign_keys=True)
    data = normalize_data(raw_data)
    return HttpResponse(json.dumps(data, cls=MyJSONEncoder), content_type='application/json')
    
def get_releases(request, pk):
    # @TODO: last 50 releases are enough ? 
    qs = Release.objects.filter(product=pk)
    raw_data = serializers.serialize('python', qs, use_natural_foreign_keys=True)
    data = normalize_data(raw_data)
    return HttpResponse(json.dumps(data, cls=MyJSONEncoder), content_type='application/json')
    
def get_testresults(request):
    
    response = {}
    query_string = request.GET.get('fws', '')
    fws = query_string.split(',')
    print(fws)
    model = apps.get_model('tms', 'TestResult')
    qs = TestResult.objects.filter(testexec__dut_fw__in=fws)
    raw_data = serializers.serialize('python', qs, use_natural_foreign_keys=True)
    
    columns = get_grid_cols_def(model)
    
    data = normalize_data(raw_data)
    print(data)
    response['data']=data
    response['columns']= columns
        
    return HttpResponse(json.dumps(response, cls=MyJSONEncoder), content_type='application/json')

