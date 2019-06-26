# MISP
个人任务管理系统（MISP）

这次个人作业的选题是一个个人任务管理系统开发。我假设了有三个任务类型，包括英语，学习，研究。每个任务类型下的任务是可以量化的，每个任务的格式可以统一为：从xxx时间到xxx时间，完成xxx篇/小时xxx。如“在2019年6月24日到2019年7月14日完成200篇托福阅读”，“在2019年6月24日到2019年7月14日完成20篇论文阅读”。系统预期实现任务添加，任务进度显示，任务删除，当天所需完成任务分配，任务完成分析等功能。

系统概述：
系统的目的是帮助个人管理日常生活中的各项任务，如科研，学习等，类似一个个人版的多项目管理系统，能够告诉用户在当天需要完成什么具体任务，当用户完成后可以点击已完成，这样该任务的进度就会得到修改，或者用户没有完成当天任务，系统会根据剩余任务量对接下来的时间每天的任务量进行重新分配。用户可以提前添加任务，如在21号添加24号才开始的任务，这时任务的状态是未开始，一般用户会在当天设置一个任务，这时任务状态为未完成。一个任务结束有两种情况一种是在规定时间完成任务，任务状态变为已完成。另一种是在规定时间内没有完成任务，任务状态变为已结束，未完成。

系统功能：
任务添加：
允许用户输入任务名称，任务类型，任务量，任务创建人，任务创建时间，任务开始时间，任务结束时间，任务状态等任务信息。
当天任务分配：
为用户计算当天需要完成各项进行任务的具体工作量。
任务状态自动修改：
一个任务有多种状态，如“未开始”，“未完成”，“已完成”，“已结束，未完成”，系统会根据时间，任务完成情况对任务的状态进行自动修改。
任务列表显示：
显示所有任务，包括当前任务和历史任务。
任务完成分析：
显示当前任务和历史任务完成进度。
删除任务：删除历史任务和当前任务。

数据库设计:
任务数据表
任务数据表包括任务id，任务名，任务类型（1,2,3分别表示学习，英语，科研），创建者，创建时间，开始时间，结束时间，任务内容，任务状态。

当日任务数据表
当日任务数据表包括id，任务类型，当天任务内容，当天任务状态，任务id

已完成数据表
已完成数据表包括id，已过去天数，已完成内容，任务id

未完成数据表
未完成数据表包括id，剩余天数，剩余内容，任务id


后台处理
添加任务：
添加新的任务，任务表更新，剩余任务表更新，完成任务表更新，如果是一开始任务，当日任务表更新，如果是未开始任务，当日任务表则不更新。
首页当日任务显示：
显示今日任务需要完成的任务，这里需要检查未开始任务中是否有今日开始任务，如果有的话就需要将该任务状态进行修改，变为“未完成”，然后添加进当日任务表中。这个页面会自动检索当日任务表中的数据然后显示在页面中。我们这里的任务都是可以量化的，后台会首先检索剩余任务量，使用正则表达式检索出任务量数字，然后与剩余天数进行计算，得到当日任务量。
删除任务：
删除任务数据库中的任务，任务表跟新，每日任务表更新，完成任务表更新，未完成任务更新。总之把各个表中与该任务有关的记录全部删除。
任务进度显示：
从已完成任务表中取出任务，然后将各个任务的已完成量除以总任务量即可得到任务进度。


开发环境：
系统的开发环境是基于Django框架，前端是个人手写html，CSS代码得到，所有显得有些简陋，数据库则选择了wamp集成环境中的MySQL数据库。

