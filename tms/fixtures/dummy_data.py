import random
projects = ['Ford', 'VW', 'Audi' ]
products = ['Focus', 'Polo', 'A6']
releases = ['1.5', '2.1', '3.0']
verdict = ['pass', 'fail', ' ']
def project(f):
    i = 1
    for p in projects:
        f.write('{"model":"tms.Project", "pk":%d, "fields":{"project_id":%d, "name":"%s" } },\n'%(i, i, p))
        i+=1

def product(f):
    i = 1
    for p in products:
        f.write('{"model":"tms.Product", "pk":%d, "fields":{"project":%d, "name":"%s" } },\n'%(i, i, p))
        i+=1

def release(f):
    i = 1
    j = 1
    for p in products:
        for r in releases:
            fw_ver = p+'_'+r
            f.write('{"model":"tms.Release", "pk":%d, "fields":{"product":%d, "rel_type":"nightly", "fw_version":"%s" } },\n'%(i, j, fw_ver))
            i+=1
        j+=1

def testcases(f):
    for i in range(1, 101):
        title = "dummy_testcase_" + str(i)
        tc_id = "TES-" + str(100 + i)
        f.write('{"model":"tms.Testcase", "pk":%d, "fields":{"tc_id":"%s", "title":"%s" } },\n'%(i, tc_id, title))

def testexecs(f):
    pk=1
    for j in range(1,4): # product
        for k in range(1, 4): #fw_rel
            title = "nightly test execution " + str(pk)
            f.write('{"model":"tms.testexec", "pk":%d, "fields":{"title": "%s", "dut":%d, "dut_fw":%d, "testsys_ver":"1.0.0", "testnode":"TEST-1", "td1": "td_2.6.17", "td2":"btd800_2.6.17" } },\n' %(pk, title, j, k))
            pk+=1
 
def testresults(f):
    pk = 1
    for i in range(1, 10):  # testexecs
        for j in range(1, 101): #testcase
            res = verdict[random.randint(0,2)]
            f.write('{"model":"tms.testresult", "pk":%d, "fields":{"testexec":%d, "testcase":%d, "result":"%s"}},\n' %(pk, i, j, res))
            pk+=1

if "__main__" == __name__: 
    f = open('dummy_data.json', 'w')
    f.write('[\n')
    
    project(f)
    product(f)
    release(f)
    testcases(f)
    testexecs(f)
    testresults(f)

    f.write(']')
    f.close()
