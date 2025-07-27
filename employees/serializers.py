from django.contrib.auth.models import User
from .models import *
from rest_framework import serializers

class UsernameRelatedField(serializers.RelatedField):
    def to_representation(self,value):
        return value.user.username
    def to_internal_value(self, data):
        try:
            return Employee.objects.get(user__username=data)
        except Employee.DoesNotExist:
            raise serializers.ValidationError('Employee with this username does not exist')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','first_name','last_name']


class EmployeeSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    department=serializers.SlugRelatedField(slug_field='name',queryset=Department.objects.all())
    job_title=serializers.SlugRelatedField(slug_field='title',queryset=JobTitle.objects.all())

    class Meta:
        model=Employee
        fields=['id','user','gender', 'department','job_title','date_of_birth','contact','nin','address','emergency_contact','employee_id','employee_type','image']

    def create(self, validated_data):
        user_data=validated_data.pop('user')
        user=User(
            username=user_data['username'],
            email=user_data.get('email',''),
            first_name=user_data.get('first_name',''),
            last_name=user_data.get('last_name',''),
        )
        user.set_password('1234')  
        user.save()
        employee=Employee.objects.create(user=user,**validated_data)
        return employee
    
class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=Leave
        fields='__all__'
        read_only_fields=['employee','status']



class AttendanceSerializer(serializers.ModelSerializer):
    employee=UsernameRelatedField(queryset=Employee.objects.all())
    class Meta:
        model=Attendance
        fields='__all__'


class PerformanceReviewSerializer(serializers.ModelSerializer):
    employee=UsernameRelatedField(queryset=Employee.objects.all())
    reviewer=serializers.SlugRelatedField(slug_field='username',queryset=User.objects.all())
    class Meta:
        model=PerformanceReview
        fields='__all__'


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Document
        fields='__all__'


class AudtingSerializer(serializers.ModelSerializer):
    employee=UsernameRelatedField(queryset=Employee.objects.all())
    class Meta:
        model=Audting
        fields='__all__'

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model=Announcement
        fields='__all__'


class AccountSerializer(serializers.ModelSerializer):
    employee=UsernameRelatedField(queryset=Employee.objects.all())
    employee_name=serializers.CharField(source='employee.user.username',read_only=True)
    class Meta:
        model=Account
        fields=['id','employee','employee_name','account_number','balance']
        read_only_fields=['employee_name','balance']



class TransactionSerializer(serializers.ModelSerializer):
    employee_name=serializers.CharField(source='account.employee.user.username',read_only=True)
    account=serializers.SlugRelatedField(slug_field='account_number',queryset=Account.objects.all())

    class Meta:
        model = Transaction
        fields = ['id', 'account', 'employee_name', 'amount', 'transaction_type', 'reason', 'timestamp']
        read_only_fields = ['timestamp', 'employee_name']


class PayslipSerializer(serializers.ModelSerializer):
    employee=UsernameRelatedField(queryset=Employee.objects.all())
    net_salary=serializers.SerializerMethodField()
    employee_name=serializers.CharField(source='employee.user.username',read_only=True)
    class Meta:
        model=Payslip
        fields = ['id', 'employee', 'employee_name', 'basic_salary', 'bonus', 'deductions', 'month', 'generated_on', 'net_salary']
        read_only_fields = ['generated_on', 'net_salary', 'employee_name']

    def get_net_salary(self, obj):
        return obj.basic_salary + obj.bonus - obj.deductions