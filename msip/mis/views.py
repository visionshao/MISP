from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from .models import *
import datetime
import time
import re
import math
# Create your views here.


def Caltime(date1, date2):
    # %Y-%m-%d为日期格式，其中的-可以用其他代替或者不写，但是要统一，同理后面的时分秒也一样；可以只计算日期，不计算时间。
    date1 = time.strptime(date1, "%Y-%m-%d")
    date2 = time.strptime(date2, "%Y-%m-%d")
    # 根据上面需要计算日期还是日期时间，来确定需要几个数组段。下标0表示年，小标1表示月，依次类推...
    date1 = datetime.datetime(date1[0], date1[1], date1[2])
    date2 = datetime.datetime(date2[0], date2[1], date2[2])
    # 返回两个变量相差的值，就是相差天数
    return date2-date1


def getNumFromString(s):
    return eval(s[:len(s)-1])


def index(request):
    return HttpResponse("This is vision's MISP")


def home(request):


    todaytime = str(datetime.date.today())
    tasks = Task.objects.all()
    for task in tasks:
        # 当前日期距离任务开始日期的天数
        dis2stime = Caltime(str(task.stime), todaytime).days
        # 任务结束日期距离当前日期的天数
        dis2etime = Caltime(todaytime, str(task.etime)).days
        # 未开始到未完成刷新
        if dis2stime >= 0 and task.state == "未开始":
            daytask = Daytask()
            daytask.state = "未完成"
            daytask.task = task
            unfinishedtask = UnFinishedTask.objects.get(task=task.tid)
            left_content = unfinishedtask.content
            left_num = getNumFromString(left_content)
            day_num = math.ceil(left_num / unfinishedtask.left_days)
            daytask.content = str(left_content).replace(str(left_num), str(day_num))
            daytask.type = task.type
            daytask.save()
        # 其他任务也需要判断刷新

    tasks = Daytask.objects.all()
    return render(request, "mis/home.html", {"tasks": tasks})


def showAddPage(request):
    return render(request, "mis/add.html")


def add(request):
    """
    添加任务
    :param request:
    :return:
    """
    if request.POST:
        # 向任务表添加数据
        task = Task()
        task.name = request.POST["name"]
        task.type = request.POST["type"]
        task.creator = request.POST['creator']
        task.createtime = request.POST['createtime']
        task.stime = request.POST['stime']
        task.etime = request.POST['etime']
        task.content = request.POST['content']
        task.state = request.POST['state']


        # 天数计算
        todaytime = str(datetime.date.today())
        # 当前日期距离任务开始日期的天数
        dis2stime = Caltime(task.stime, todaytime).days
        # 任务结束日期距离当前日期的天数
        dis2etime = Caltime(todaytime, task.etime).days


        # 向完成任务表添加数据
        finished_task = FinishedTask()

        finished_task.content = str(request.POST['content']).replace(str(getNumFromString(str(request.POST['content']))), "0")
        # 如果任务还没开始，则没过去天数
        if dis2stime < 0:
            finished_task.passed_days = 0
            task.state = "未开始"
        # 如果任务已经开始
        else:
            finished_task.passed_days = dis2stime

        task.save()
        finished_task.task = task
        finished_task.save()

        # 向剩余任务表添加数据
        unfinished_task = UnFinishedTask()
        unfinished_task.task = task
        unfinished_task.content = task.content
        # 如果任务没开始
        if dis2stime < 0:
            unfinished_task.left_days = Caltime(task.stime, task.etime).days + 1
        # 如果任务开始
        else:
            unfinished_task.left_days = dis2etime + 1

        unfinished_task.save()


        # 向每日任务表添加数据
        # 如果当前任务未开始,则不存在每日任务
        if dis2stime < 0:
            return render(request, "mis/added.html")
        # 如果当前任务已经开始,创建每日任务，注意使用剩余天数
        else:
            dtask = Daytask()
            dtask.state = "未完成"
            dtask.name = request.POST["name"]
            dtask.type = request.POST["type"]
            temp_content = str(request.POST['content'])
            all_content = getNumFromString(temp_content)
            day_content = math.ceil(all_content / unfinished_task.left_days)    # 向上取整
            dtask.content = temp_content.replace(str(all_content), str(day_content))
            dtask.task = task
            dtask.save()
            return render(request, "mis/added.html")


# 展示未完成任务
def showTask(request):
    unfinishedtasks = UnFinishedTask.objects.all()
    return render(request, "mis/show.html", {"items": unfinishedtasks})


# 完成每日任务
def finishedDay(request, tid):

    todaytime = str(datetime.date.today())
    task = Task.objects.get(tid=tid)
    # 当前日期距离任务开始日期的天数
    dis2stime = Caltime(str(task.stime), todaytime).days
    # 任务结束日期距离当前日期的天数
    dis2etime = Caltime(todaytime, str(task.etime)).days

    # 获取每日任务对象，更新状态
    daytask = Daytask.objects.get(task=tid)
    daynum = getNumFromString(str(daytask.content))
    daytask.state = "已完成"

    # 获取已完成任务对象
    fitask = FinishedTask.objects.get(task=tid)
    old_unnum = getNumFromString(str(fitask.content))
    new_unnum = old_unnum + daynum
    fitask.passed_days = dis2stime
    fitask.content = str(fitask.content).replace(str(old_unnum), str(new_unnum))
    fitask.save()

    # 获取未完成任务对象，减少任务
    untask = UnFinishedTask.objects.get(task=tid)
    old_unnum = getNumFromString(str(untask.content))
    new_unnum = old_unnum - daynum

    # 如果总任务在规定时间内完成：
    if new_unnum <= 0 and dis2etime >= 0:
        # 更新总任务状态
        task.state = "已完成"
        # 删除每日任务
        daytask.delete()
        # 保存总任务状态
        task.save()
        untask.left_days = dis2etime + 1
        untask.content = str(untask.content).replace(str(old_unnum), str(new_unnum))
        untask.save()
        return home(request)
    #  如果没在规定天数内完成，任务状态为已结束，未完成
    elif new_unnum > 0 and dis2etime < 0:
        # 更新总任务状态
        task.state = "已结束，未完成"
        # 删除每日任务
        daytask.delete()
        # 保存总任务状态
        task.save()
        # 更新未完成任务
        untask.left_days = dis2etime + 1
        untask.content = str(untask.content).replace(str(old_unnum), str(new_unnum))
        untask.save()
        return home(request)
    # 如果还在进行
    else:
        # 更新总任务状态
        task.state = "未完成"
        # 求剩余天数
        untask.left_days = dis2etime + 1
        untask.content = str(untask.content).replace(str(old_unnum), str(new_unnum))
        untask.save()
        daytask.content = str(daytask.content).replace(str(getNumFromString(daytask.content)), str(math.ceil(getNumFromString(untask.content) / untask.left_days)))
        daytask.save()
        return home(request)


def delete(request, tid):
    Task.objects.get(tid=tid).delete()
    # 级联删除
    # Daytask.objects.get(task=tid).delete()
    # UnFinishedTask.objects.get(task=tid).delete()
    # FinishedTask.objects.get(task=tid).delete()
    return showTask(request)


def analysis(request):
    fitasks = FinishedTask.objects.all()
    results = []

    class Item:

        def __init__(self, name, type, content, finished):
            self.name = name
            self.type = type
            self.content = content
            self.finished = finished

    for item in fitasks:

        name = item.task.name
        type = item.task.type
        content = item.task.content
        finished = round((getNumFromString(item.content) / getNumFromString(item.task.content)), 4) * 100
        temp = Item(name, type, content, finished)
        results.append(temp)

    return render(request, "mis/analysis.html", {"results": results})


def fresh(request):
    # 未开始到未完成
    todaytime = str(datetime.date.today())
    tasks = Task.objects.all()
    for task in tasks:
        # 当前日期距离任务开始日期的天数
        dis2stime = Caltime(str(task.stime), todaytime).days
        # 任务结束日期距离当前日期的天数
        dis2etime = Caltime(todaytime, str(task.etime)).days

        if dis2stime >= 0:
            daytask = Daytask()
            daytask.state = "未完成"
            daytask.task = task
            daytask.content



