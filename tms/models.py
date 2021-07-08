from django.db import models


class Project(models.Model):
    project_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)

    def natural_key(self):
        return self.name

    def __str__(self):
        return self.name

class Product(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def natural_key(self):
        return self.name

    def __str__(self):
        return self.name
    
class Release(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rel_type = models.CharField(max_length=20, default="unknown")  # nightly or RC
    fw_version = models.CharField(max_length=30)

    def natural_key(self):
        return self.product

    def __str__(self):
        return self.fw_version


class Testcase(models.Model):
    tc_id = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=250)

    def natural_key(self):
        return self.tc_id

    def __str__(self):
        return self.tc_id

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def natural_key(self):
        return self.name

    def __str__(self):
        return self.name

class TestcaseTagging(models.Model):
    testcase = models.ForeignKey(Testcase, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

""" 
class TestSuite(models.Model):
    name = models.CharField(max_length=200)
    path = models.FilePathField(max_length=400, allow_folders=True, allow_files=False)

 """
class TestExec(models.Model):
    title = models.CharField(max_length=250)
    dut = models.ForeignKey(Product, on_delete=models.CASCADE)
    dut_fw = models.ForeignKey(Release, on_delete=models.CASCADE)
    testsys_ver = models.CharField(max_length=50)  # robotaf tag or master
    td1 = models.CharField(max_length=100, blank=True, null=True)  # product_name_with_fw_version
    td2 = models.CharField(max_length=100, blank=True, null=True)  # product_name_with_fw_version
    
    """
    def natural_key(self):
        return "dut_fw:%s, testsys_ver:%s"%(self.dut_fw, self.testsys_ver)
    """
    def __str__(self):
        return self.title

class TestExecTagging(models.Model):
    testexec = models.ForeignKey(TestExec, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class Defect(models.Model):
    testcase = models.ForeignKey(Testcase, on_delete=models.CASCADE)
    issue_id = models.CharField(max_length=20) 
    comments = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def natural_key(self):
        return self.issue_id
    
    def __str__(self):
        return self.issue_id

class TestResult(models.Model):
    testexec = models.ForeignKey(TestExec, on_delete=models.CASCADE)
    testcase = models.ForeignKey(Testcase, on_delete=models.CASCADE)
    testnode = models.CharField(max_length=50)
    result = models.CharField(max_length=20)
    