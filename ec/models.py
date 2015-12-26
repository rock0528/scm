from django.db import models

class EC_Host(models.Model):
    host_name = models.CharField(max_length = 100, blank = False, null = False)
    user = models.CharField(max_length = 10, blank = False, null = False)
    password = models.CharField(max_length = 10, blank = False, null = False)

class EC_Project(models.Model):
    CHOICES_CASETYPE = (
            (0, 'src'),
            (1, 'data')
        )
    project_name = models.CharField(max_length = 100, blank = False, null = False)
    project_type = models.IntegerField(default = 1, choices=CHOICES_CASETYPE)

class EC_Schedule_Backup(models.Model):
    host = models.ForeignKey(EC_Host,related_name='schedule_host')
    project = models.ForeignKey(EC_Project,related_name='schedule_project')
    is_restore = models.BooleanField(default=False)
    backup_time = models.DateTimeField()

class EC_Schedule(models.Model):
    backup = models.ForeignKey(EC_Schedule_Backup,related_name='schedule_backup')
    schedule_name = models.CharField(max_length = 100, blank = False, null = False)
    schedule_enable = models.CharField(max_length = 10, blank = False, null = False)
