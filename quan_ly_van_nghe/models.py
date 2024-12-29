from django.db import models

# Địa điểm tổ chức
class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)

    def __str__(self):
        return self.name


# Chương trình văn nghệ
class EventProgram(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        max_length=50,
        choices=[('planned', 'Lên kế hoạch'), ('ongoing', 'Đang diễn ra'), ('completed', 'Kết thúc')],
        default='planned'
    )


    def __str__(self):
        return self.name


# Nhiệm vụ/tiết mục trong chương trình
class Task(models.Model):
    event = models.ForeignKey(EventProgram, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True) 
    deadline = models.DateField()

    def __str__(self):
        return self.name
