from django.urls import path,include
from .views import *


urlpatterns = [
   path('employees/',employees,name='employees'),
   path('payslip/',employee_payslip,name='employee-payslip'),
 
   path('attendance/',attendance_list,name='employee-attendance'),
 
   path('reviews/',employee_reviews,name='employee-reviews'),

   path('documents/',employee_documents,
   name='employee-documents'),

   path('audit/',create_audit_logs,name='employee-audit'),
   path('announcements/',announcements,name='announcements'),
   path('profile/',employee_profile,name='employee-profile'),
   path('employee-details/<int:pk>/',employee_details,name='employee-details'),
   path('request-leave/',employee_leave_request,name='employee-request-leave'),
   path('leave-approval/<int:pk>/', leave_approval, name='leave-approval'),

]
