from tms.fixtures.dummy_data import product, testcases, testresults
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.core import serializers
from tms.utils import MyJSONEncoder, get_grid_cols_def, normalize, prepare_response, debug_info
import json
from django.apps import apps
from django.db.models import F

# Create your views here.
def index(request):
    return render(request, 'tms/index.html')

def get_all_products(request):
    qs = Product.objects.select_related().all()
    raw_data = serializers.serialize('python', qs, use_natural_foreign_keys=True)
    data = normalize(raw_data)
    return HttpResponse(json.dumps(data, cls=MyJSONEncoder), content_type='application/json')
    
def get_releases(request, pk):
    # @TODO: last 50 releases are enough ? 
    qs = Release.objects.filter(product=pk)
    raw_data = serializers.serialize('python', qs, use_natural_foreign_keys=True)
    data = normalize(raw_data)
    return HttpResponse(json.dumps(data, cls=MyJSONEncoder), content_type='application/json')
    
def get_testresults(request):
    response = {}
    query_data = []
    query_string = request.GET.get('fws', '')
    fws = query_string.split(',')
    debug_info(fws)
    """
    model = apps.get_model('tms', 'TestResult')
    qs = TestResult.objects.filter(testexec__dut_fw__in=fws).select_related('testexec')
    raw_data = serializers.serialize('python', qs, use_natural_foreign_keys=True)
    columns = get_grid_cols_def(model)
    data = normalize(raw_data, include_id=False)
    response['data']=data
    response['columns']= columns
    """
    for fw in fws:
        qs = TestResult.objects.filter(
            testexec__dut_fw=fw).select_related().values('result', 'testnode').annotate(
                test_id=F('testcase__tc_id'), fw_ver=F('testexec__dut_fw__fw_version'))        
        query_data.append({fw:list(qs)})

    debug_info(query_data)
    
    response = prepare_response(query_data, join_on="test_id", index="fw_ver", value="result")
    debug_info(response)
    
    return HttpResponse(json.dumps(response, cls=MyJSONEncoder), content_type='application/json')

