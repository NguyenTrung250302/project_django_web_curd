from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from .models import EventProgram, Task, Location

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Tên người dùng hoặc mật khẩu không chính xác.')
    
    return render(request, 'quan_ly_van_nghe/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Kiểm tra các điều kiện đầu vào
        if not username or not password or not confirm_password:
            messages.error(request, 'Vui lòng điền đầy đủ thông tin.')
            return render(request, 'quan_ly_van_nghe/register.html')

        if password != confirm_password:
            messages.error(request, 'Mật khẩu và xác nhận mật khẩu không khớp.')
            return render(request, 'quan_ly_van_nghe/register.html')

        # Kiểm tra tên người dùng đã tồn tại hay chưa
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Tên người dùng đã tồn tại.')
            return render(request, 'quan_ly_van_nghe/register.html')

        # Tạo người dùng mới
        User.objects.create_user(username=username, password=password)
    
        return redirect('login')  # Sau khi đăng ký thành công, chuyển tới trang chính
    
    return render(request, 'quan_ly_van_nghe/register.html')

# -------------------------------------------------------------------------------------------------
@login_required
def home_view(request):
    return render(request, 'quan_ly_van_nghe/home.html')

# -------------------------------------------------------------------------------------------------

# View cho trang quản lý chương trình
@login_required
def event_programs_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        events = EventProgram.objects.filter(name__icontains=search_query)
    else:
        events = EventProgram.objects.all()

    return render(request, 'quan_ly_van_nghe/event/event_list.html', {'events': events})

# View cho trang tạo chương trình mới
@login_required
def create_event_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        location_name = request.POST.get('location')  # Nhận giá trị nhập từ input location
        status = request.POST.get('status')

        # Kiểm tra nếu địa điểm đã tồn tại trong cơ sở dữ liệu, nếu không thì tạo mới
        location = Location.objects.get_or_create(name=location_name)

        # Lưu chương trình vào cơ sở dữ liệu
        event = EventProgram(
            name=name,
            start_date=start_date,
            end_date=end_date,
            location=location,
            status=status
        )
        event.save()

        return redirect('event_programs')  # Đổi thành URL của danh sách chương trình

    return render(request, 'quan_ly_van_nghe/event/create_event.html')

# View cho trang chỉnh sửa chương trình
@login_required
def edit_event_view(request, event_id):
    event = get_object_or_404(EventProgram, id=event_id)
    
    if request.method == 'POST':
        # Nhận dữ liệu từ form
        name = request.POST.get('name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        location_name = request.POST.get('location')  # Địa điểm nhập vào từ form
        status = request.POST.get('status')

        # Kiểm tra và cập nhật địa điểm
        location = Location.objects.get_or_create(name=location_name)

        # Cập nhật thông tin chương trình
        event.name = name
        event.start_date = start_date
        event.end_date = end_date
        event.location = location
        event.status = status
        event.save()

        return redirect('event_program_list')

    return render(request, 'quan_ly_van_nghe/event/edit_event.html', {'event': event})

# View cho trang xóa chương trình
def delete_event_view(request, event_id):
    event = get_object_or_404(EventProgram, id=event_id)
    event.delete()
    return redirect('event_programs')

# ---------------------------------------------------------------------------------------------------
# View cho trang quản lý Tiết mục
@login_required
def task_list_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        tasks = Task.objects.filter(name__icontains=search_query)
    else:
        tasks = Task.objects.all()
    return render(request, 'quan_ly_van_nghe/tasks/task_list.html', {'tasks': tasks, 'search_query': search_query})

@login_required
def create_task(request):
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        name = request.POST.get('name')
        event_id = request.POST.get('event')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')

        # Kiểm tra xem các giá trị có hợp lệ không
        if not name or not event_id or not deadline:
            return HttpResponse("Dữ liệu không hợp lệ", status=400)

        # Lấy đối tượng EventProgram từ ID
        try:
            event = EventProgram.objects.get(id=event_id)
        except EventProgram.DoesNotExist:
            return HttpResponse("Chương trình không tồn tại", status=404)

        # Tạo Tiết mục mới
        task = Task(
            name=name,
            event=event,
            description=description,
            deadline=deadline  # deadline sẽ chỉ chứa ngày
        )
        task.save()

        # Chuyển hướng về trang danh sách Tiết mục
        return redirect('task_list')

    # Lấy tất cả các chương trình để hiển thị trong dropdown
    events = EventProgram.objects.all()

    # Hiển thị form
    return render(request, 'quan_ly_van_nghe/tasks/create_task.html', {'events': events})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        task.name = request.POST.get('name')
        task.description = request.POST.get('description')
        task.deadline = request.POST.get('deadline')

        task.save()  # Lưu thay đổi vào cơ sở dữ liệu

        return redirect('task_list')  # Sau khi sửa, điều hướng đến danh sách Tiết mục
    
    events = EventProgram.objects.all()  # Lấy danh sách chương trình để chọn
    return render(request, 'quan_ly_van_nghe/tasks/edit_task.html', {'task': task, 'events': events})

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')