from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Project)
admin.site.register(Product)
admin.site.register(Release)
admin.site.register(Testcase)
admin.site.register(Tag)

class TestExecAdmin(admin.ModelAdmin):
    list_display = ('title', 'dut', 'dut_fw', 'testsys_ver', 'td1', 'td2')

admin.site.register(TestExec, TestExecAdmin)

admin.site.register(Defect)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('testexec', 'testcase', 'result')
    
admin.site.register(TestResult, TestResultAdmin)
