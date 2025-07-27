from .models import *
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .serializers import *
from rest_framework.permissions import IsAuthenticated,IsAdminUser

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def employees(request):
    if request.method=='GET':
        employees=Employee.objects.all()
        serializers=EmployeeSerializer(employees, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    elif request.method=='POST':
        serializers = EmployeeSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)   
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def employee_payslip(request):
    if request.method == 'GET':
        if request.user.is_staff:
            payslip=Payslip.objects.all().order_by('-month')
        else:
            try:
                employee=Employee.objects.get(user=request.user)
                payslip=Payslip.objects.filter(employee=employee).order_by('-month')
            except Employee.DoesNotExist:
                return Response({'error':'Employee not found'},status=status.HTTP_404_NOT_FOUND)
        serializer=PayslipSerializer(payslip,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    elif request.method == 'POST':
        if not request.user.is_staff:
            return Response({'detail': 'Only admins can create payslips'}, status=status.HTTP_403_FORBIDDEN)

        serializer = PayslipSerializer(data=request.data)
        if serializer.is_valid():
            payslip = serializer.save()

            # Calculate net salary
            net_salary = payslip.calculate_net_salary()

            try:
                account = Account.objects.get(employee=payslip.employee)
                account.balance += net_salary
                account.save()

                Transaction.objects.create(
                    account=account,
                    amount=net_salary,
                    transaction_type='credit',
                    reason=f'Salary for {payslip.month.strftime("%B %Y")}'
                )

            except Account.DoesNotExist:
                return Response({'error': 'Account not found for the employee'}, status=status.HTTP_404_NOT_FOUND)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def attendance_list(request):
    if request.method=='GET':
        attendance=Attendance.objects.all()
        serializers=AttendanceSerializer(attendance,many=True)
        return Response({'data':serializers.data},status=status.HTTP_200_OK)
    if request.method=='POST':
        if not request.user.is_staff:
            return Response({'detail':'Only admins can create attendance list'},status=status.HTTP_403_FORBIDDEN)
        serializers=AttendanceSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])  
@permission_classes([IsAuthenticated])
def employee_reviews(request):
    if request.method == 'GET':
        try:
            employee=Employee.objects.get(user=request.user)
            reviews=PerformanceReview.objects.filter(employee=employee).order_by('-review-date')
            serializers=PerformanceReviewSerializer(reviews, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)  


    elif request.method=='POST':
        if not request.user.is_staff:
            return Response({'detail': 'Only admins can create performance reviews'}, status=status.HTTP_403_FORBIDDEN)
        serializers = PerformanceReviewSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def employee_documents(request):
    try:
        employee=Employee.objects.get(user=request.user)
        if request.method=='GET':
            documents=Document.objects.filter(employee=employee)
            serializers=DocumentSerializer(documents,many=True
            )
            return Response(serializers.data, status=status.HTTP_200_OK)
        elif request.method=='POST':
            data=request.data.copy()
            data['employee']=employee.id
            serializers=DocumentSerializer(data=data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    except Employee.DoesNotExist:
        return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)



    
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def create_audit_logs(request):
    if request.method=='GET':
        if request.user.is_staff:
           audits=Audting.objects.all().order_by('-timestamp')
        else:
            employee=Employee.objects.get(user=request.user)
            audits=Audting.objects.filter(employee=employee).order_by('timestamp')
        serializers=AudtingSerializer(audits,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    elif request.method=='POST':
        serializers=AudtingSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def announcements(request):
    if request.method=='GET':
        announcements=Announcement.objects.all().order_by('-posted_at')
        serializers=AnnouncementSerializer(announcements, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    elif request.method=='POST':
        if not request.user.is_staff:
            return Response({'detail':'Not authorized.'},status=status.HTTP_400_BAD_REQUEST)
        announcements=Announcement.objects.all()
        serializers=AnnouncementSerializer(data=request.data)
        if serializers.is_valid():
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_profile(request):
    try:
        employee=Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        return Response({'error':'Employee not found'},status=status.HTTP_404_NOT_FOUND)
    
    serializers=EmployeeSerializer(employee)
    return Response(serializers.data,status=status.HTTP_200_OK)
    

@api_view(['GET', 'PUT','DELETE'])
@permission_classes([IsAuthenticated,IsAdminUser])   
def employee_details(request,pk):
    try:
        employee=Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        serializers=EmployeeSerializer(employee)
        return Response(serializers.data,status=status.HTTP_200_OK)
    elif request.method=='PUT':
        data=request.data.copy()
        user_data = data.pop('user', None)
        if user_data and isinstance(user_data,dict):
            user=employee.user
            for attr,value in user_data.items():
                setattr(user,attr,value)
                try:
                    user.full_clean()
                    user.save()
                except Exception as e:
                    return Response({'user':str(e)},status=status.HTTP_400_BAD_REQUEST)
        serializers=EmployeeSerializer(employee,data=data,partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        employee.delete()
        return Response({'message': 'Employee deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
         
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def employee_leave_request(request):
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        leaves=Leave.objects.filter(employee=employee).order_by('-start_date')
        serializers = LeaveSerializer(leaves, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
       
        serializer = LeaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee=employee)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def leave_approval(request,pk):
    try:
        leave=Leave.objects.get(pk=pk)
    except Leave.DoesNotExist:
        return Response({'error':'Leave request not found'},status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        serializers=LeaveSerializer(leave)
        return Response(serializers.data, status=status.HTTP_200_OK)
    elif request.method=='PUT':
        data=request.data
        status_update=data.get('status')
        if status_update not in ['approved','rejected']:
            return Response({'error':'Invalid status. Must be "approved"  of "rejected"'},status=status.HTTP_400_BAD_REQUEST)
        leave.status=status_update
        leave.save()
        serializers=LeaveSerializer(leave)
        return Response(serializers.data, status=status.HTTP_200_OK)
    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated,IsAdminUser])

def admin_manage_accounts(request):
    if request.method=='GET':
        accounts=Account.objects.all()
        serializers=AccountSerializer(accounts,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    elif request.method=='POST':
        serializers=AccountSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_account_details(request):
    try:
        employee=Employee.objects.get(user=request.user)
        account=Account.objects.filter(employee=employee)
        serializers=AccountSerializer(account)
        return Response(serializers.data,status=status.HTTP_200_OK)
    except Employee.DoesNotExist:
        return Response({'error':'Employee not found'},status=status.HTTP_404_NOT_FOUND)
    except Account.DoesNotExist:
        return Response({'error':'Account not found'},status=status.HTTP_404_NOT_FOUND)