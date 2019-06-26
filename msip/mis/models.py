from django.db import models

# Create your models here.
TYPE_SETS = (
        ("1", "Learning"),
        ("2", "English"),
        ("3", "Research"),
    )


class Daytask(models.Model):
    dtid = models.AutoField(primary_key=True, default=None)
    type = models.CharField(max_length=1, choices=TYPE_SETS)
    content = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    task = models.ForeignKey("Task", to_field="tid", on_delete=models.CASCADE)


class Task(models.Model):
    tid = models.AutoField(primary_key=True, default=None)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=1, choices=TYPE_SETS)
    creator = models.CharField(max_length=255)
    createtime = models.DateField()
    stime = models.DateField()
    etime = models.DateField()
    content = models.CharField(max_length=255)
    state = models.CharField(max_length=255)


class FinishedTask(models.Model):
    ftid = models.AutoField(primary_key=True, default=None)
    passed_days = models.IntegerField()
    content = models.CharField(max_length=255)
    task = models.ForeignKey("Task", to_field="tid", on_delete=models.CASCADE)


class UnFinishedTask(models.Model):
    uftid = models.AutoField(primary_key=True, default=None)
    left_days = models.IntegerField()
    content = models.CharField(max_length=255)
    task = models.ForeignKey("Task", to_field="tid", on_delete=models.CASCADE)