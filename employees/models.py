from django.db import models
from django.contrib.auth.models import User
import uuid
def generate_employee_id():
    return f'EMP-{uuid.uuid4().hex[:8].upper()}'


class Department(models.Model):
    name=models.CharField(max_length=20,blank=False,unique=True)
    description=models.TextField()
    slug=models.SlugField(unique=True,blank=False)

    def __str__(self):
        return self.name
    

class JobTitle(models.Model):
    title=models.CharField(max_length=20)
    description=models.TextField()
    slug=models.SlugField(unique=True)

    def __str__(self):
        return self.title
    
class Employee(models.Model):
    GENDER_CHOICES=(
        ('Female','Female'),
        ('Male','Male'),

    )
    EMPLOYEE_TYPE_CHOICES=(
        ('parmenet','Permanent'),
        ('contract','Contract'),
        ('part time','Part Time'),
        ('intern','Intern'),

    )
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    gender=models.CharField(max_length=10,choices=GENDER_CHOICES)
    date_of_birth=models.DateField()
    contact=models.CharField(max_length=10)
    nin=models.CharField(max_length=16,blank=True)
    address=models.CharField(max_length=20)
    emergency_contact=models.CharField(max_length=10,blank=True)
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    job_title=models.ForeignKey(JobTitle,on_delete=models.CASCADE)
    employee_id=models.CharField(default=generate_employee_id())
    employee_type=models.CharField(max_length=10,choices=EMPLOYEE_TYPE_CHOICES)
    image=models.ImageField(upload_to='images/',blank=True,null=True)

    def __str__(self):
        return self.user.username
    

class Leave(models.Model):
    STATUS_CHOICES=(
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected'),
    )

    LEAVE_TYPE_CHOICES=[
        ('sick','Sick Leave'),
        ('annual','Annual Leave'),
        ('maternity','Maternity Leave'),
        ('paternity','Paternity Leave'),
        ('unpaid','Unpaid Leave'),
        ('casual', 'Casual Leave'),
    ]
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    leave_type=models.CharField(max_length=20,choices=LEAVE_TYPE_CHOICES,blank=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    reason=models.TextField()
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.employee.user.username} {self.leave_type} {self.status}'




class Account(models.Model):
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    account_number=models.CharField(max_length=20,unique=True)
    balance=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)

    def __str__(self):
        return f'{self.employee.user.username}'




class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES=[
        ('credit','Credit'),
        ('debit','Debit'),
    ]
    account=models.ForeignKey(Account,on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    transaction_type=models.CharField(max_length=10,choices=TRANSACTION_TYPE_CHOICES)
    reason=models.TextField()
    timesatmp=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.account.employee.user.username}'
    


    
class Payslip(models.Model):
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    basic_salary=models.DecimalField(max_digits=10,decimal_places=2)
    bonus=models.DecimalField(max_digits=10,decimal_places=2)
    deductions=models.DecimalField(max_digits=10,decimal_places=2)
    generated_on=models.DateTimeField(auto_now_add=True)
    month=models.DateField()
   

    def calculate_net_salary(self):
        return self.basic_salary + self.bonus - self.deductions 

    def __str__(self):
        return f'{self.employee.user.username} {self.month} - Net Salary: {self.calculate_net_salary()}'

class Attendance(models.Model):
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    date=models.DateField()
    check_in_time=models.TimeField()   
    check_out_time=models.TimeField()

    # @property
    # def username(self):
    #     return self.employee.user.username

    def __str__(self):
        return f'{self.employee.user.username} {self.date}'
class PerformanceReview(models.Model):
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    reviewer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reviewer')
    review_date=models.DateField()
    rating=models.PositiveIntegerField()

    def __str__(self):
        return f'{self.employee.user.username} {self.reviewer}'
    

class Document(models.Model):
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    file=models.FileField(upload_to='documents/')
    description=models.TextField()

    def __str__(self):
        return f'{self.employee.user.username} {self.file}'


class Audting(models.Model):
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    action=models.CharField(max_length=100)
    timestamp=models.DateTimeField(auto_now_add=True)
    details=models.TextField()

    def __str__(self):
        return f'{self.employee.user.username} - {self.action} at {self.timestamp}'
    
class Announcement(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    posted_by=models.ForeignKey(User,on_delete=models.CASCADE)
    posted_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title