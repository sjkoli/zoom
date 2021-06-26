from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.core import serializers
from tms.utils import MyJSONEncoder
import json


# Create your views here.
def index(request):
    data  = TestResult.objects.filter(testexec__dut__name="Focus")
    print(data)
    print(data[0].result)
    return render(request, 'tms/index.html', {'data': data[0]})

def get_all_products(request):
    qs = Product.objects.select_related().all()
    raw_data = serializers.serialize('python', qs, use_natural_foreign_keys=True)
    return HttpResponse(json.dumps(raw_data, cls=MyJSONEncoder), content_type='application/json')
    
def get_releases(request, pk):
    #last 50 releases are enough
    qs = Release.objects.filter(product=pk)
    raw_data = serializers.serialize('python', qs, use_natural_foreign_keys=True)
    return HttpResponse(json.dumps(raw_data, cls=MyJSONEncoder), content_type='application/json')
    
def get_testresults(request):
    fw= request.GET.get('dut_fw', '')
    print(fw)
    qs = TestResult.objects.filter(testexec__dut_fw=1)
    raw_data = serializers.serialize('python', qs, use_natural_foreign_keys=True)
    return HttpResponse(json.dumps(raw_data, cls=MyJSONEncoder), content_type='application/json')
    