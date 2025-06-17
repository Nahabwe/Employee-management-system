from django.contrib import admin
from .models import *

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'department', 'job_title', 'employee_type']
    list_filter = ['gender', 'employee_type', 'department']
    search_fields = ['user__username', 'employee_id', 'contact', 'nin']
    ordering = ['user__username']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ['employee', 'leave_type', 'status', 'start_date', 'end_date']
    list_filter = ['status', 'leave_type']
    search_fields = ['employee__user__username', 'reason']
    ordering = ['-created_at']

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['employee', 'account_number', 'balance']
    search_fields = ['employee__user__username', 'account_number']
    ordering = ['employee']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'transaction_type', 'amount', 'timesatmp']
    list_filter = ['transaction_type']
    search_fields = ['account__account_number', 'reason']
    ordering = ['-timesatmp']

@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ['employee', 'month', 'basic_salary', 'bonus', 'deductions', 'calculate_net_salary']
    search_fields = ['employee__user__username']
    ordering = ['-month']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'check_in_time', 'check_out_time']
    list_filter = ['date']
    search_fields = ['employee__user__username']

@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ['employee', 'reviewer', 'review_date', 'rating']
    list_filter = ['review_date']
    search_fields = ['employee__user__username', 'reviewer__username']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['employee', 'file', 'description']
    search_fields = ['employee__user__username', 'description']

@admin.register(Audting)
class AudtingAdmin(admin.ModelAdmin):
    list_display = ['employee', 'action', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['employee__user__username', 'action']

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'posted_by', 'posted_at']
    search_fields = ['title', 'content', 'posted_by__username']
    ordering = ['-posted_at']
