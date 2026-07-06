from django.db import models
from django.conf import settings

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')

    due_date = models.DateField() 
    tags = models.JSONField(default=list, blank=True)
    
    position = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['position']

    def save(self, *args, **kwargs):
        if not self.id and self.position == 0:
            last_task = Task.objects.filter(
                user=self.user,
                due_date=self.due_date,
                status=self.status
            ).order_by('-position').first()
            
            if last_task:
                self.position = last_task.position + 1
            else:
                self.position = 0 
                
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title