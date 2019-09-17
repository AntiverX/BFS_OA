# from django.db import models
# from user_info.models import User
#
#
# # 目标
# class Target(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     term = models.TextField()
#     time = models.DateField()
#     expected_result = models.TextField()
#     time_consumed = models.TextField()
#     content = models.TextField()
#     end_of_term_summary = models.TextField()
#     semester = models.TextField(null=True)
#
#
# # 计划
# class Plan(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     type = models.CharField(max_length=32)
#     plan_name = models.CharField(max_length=32)
#     plan_result = models.TextField()
#     is_reviewed = models.BooleanField()
#     head_person = models.CharField(max_length=32)
#     affiliated_person = models.TextField()
#     planed_time = models.IntegerField()
#     planed_start_time = models.DateField()
#     planed_end_time = models.DateField()
#     actual_time = models.IntegerField(null=True)
#     actual_start_time = models.DateField(null=True)
#     actual_end_time = models.DateField(null=True)
#     advanced_postponed_time = models.IntegerField()
#     remark = models.TextField()
#
#
# # 周报
# class WeeklySummary(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     week = models.IntegerField(default=0)
#     submit_time = models.DateTimeField(auto_now=True)
#     average_work_hour = models.TextField()
#     absent_hour = models.TextField()
#     real_name = models.CharField(max_length=150)
#     this_week_task = models.TextField()
#     next_week_task = models.TextField()
#     is_present = models.BooleanField(default=False)  # 到场
#     is_absent = models.BooleanField(default=False)  # 未到
#     is_left = models.BooleanField(default=False)  # 请假
#
#
# # 会议记录
# class MeetingRecord(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     real_name = models.TextField(blank=True)
#     date = models.DateField()
#     time = models.TimeField()
#     cost_time = models.IntegerField()
#     place = models.CharField(max_length=50)
#     theme = models.TextField()
#     theme_content = models.TextField()
#     remark = models.TextField(null=True)
#
#
# # 工作总结
# class WorkSummary(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     date = models.DateTimeField()
#     type = models.CharField(max_length=32)
#     summary = models.TextField()
#     average_time = models.CharField(max_length=32)
#     all_days = models.IntegerField()
#     man_day = models.TextField(null=True)
#     total_man_day = models.TextField(null=True)
#     natural_day = models.TextField(null=True)
#     remark = models.TextField(null=True)
#
#
# # 工作成果
# class WorkAchievement(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     real_name = models.TextField(blank=True)
#     date = models.DateField()
#     semester = models.TextField()
#     achievement_name = models.TextField()
#     man_day = models.IntegerField()
#     major_contributor = models.TextField()
#     is_finished = models.TextField()
#     paper_published = models.TextField(blank=True)
#     paper_contributed = models.TextField(blank=True)
#     patent_published = models.TextField(blank=True)
#     patent_contributed = models.TextField(blank=True)
#     software_published = models.TextField(blank=True)
#     software_contributed = models.TextField(blank=True)
#     application_composed = models.TextField(blank=True)
#     document_composed = models.TextField(blank=True)
#     software_finished = models.TextField(blank=True)
#     document_summary = models.TextField(blank=True)
#     help_freshmen = models.TextField(blank=True)
#     departure = models.TextField(blank=True)
#     comment = models.TextField(blank=True)
#
#
# # 业绩量化
# class AchievementQuantization(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     real_name = models.TextField(blank=True)
#     # 填写日期
#     date = models.DateField()
#     # 学期
#     semester = models.TextField()
#     # 发表学术论文数量
#     paper_published = models.TextField(blank=True)
#     # 投稿学术论文数量
#     paper_contributed = models.TextField(blank=True)
#     # 获批专利
#     patent_published = models.TextField(blank=True)
#     # 申请专利
#     patent_contributed = models.TextField(blank=True)
#     # 获批软件著作权
#     software_published = models.TextField(blank=True)
#     # 申请软件著作权
#     software_contributed = models.TextField(blank=True)
#     # 撰写申请书
#     application_composed = models.TextField(blank=True)
#     # 撰写项目验收文档
#     document_composed = models.TextField(blank=True)
#     # 完成原型或应用系统
#     software_finished = models.TextField(blank=True)
#     # 获奖数量
#     reward = models.TextField(blank=True)
#     # 学术报告次数
#     scholar_report_times = models.TextField(blank=True)
#     # 学期平均日工作时间
#     average_work_hour = models.TextField(blank=True)
#     # 竞赛出题
#     proposition = models.TextField(blank=True)
#     # 组织竞赛
#     competition_organized = models.TextField(blank=True)
#     # 未参加学术报告次
#     absent_times_for_scholar_report = models.TextField(blank=True)
#     # 未参加学术报告评分次数
#     absent_times_for_ranking = models.TextField(blank=True)
#
#
# # 工作量认定
# class AchievementQuantizationConfirmation(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     real_name = models.TextField(blank=True)
#     # 填写日期
#     date = models.DateField()
#     # 大类
#     primary_classification = models.TextField()
#     # 小类
#     secondary_classification = models.TextField()
#     # 编号（小类）
#     number = models.TextField(blank=True)
#     # 完成类型（独立、合作人数/占比）
#     completion_type = models.TextField()
#     # 人日
#     man_days = models.TextField()
#     # 级别
#     level = models.TextField()
#     # 有形工作结果
#     tangible_work = models.TextField()
#     # 备注
#     remark = models.TextField(blank=True)
#     # 组内认定
#     group_confirmation = models.TextField(blank=True)
#     # 导师认定
#     tutor_confirmation = models.TextField(blank=True)
#
#
# # 学术报告
# class ScholarReport(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     real_name = models.TextField(blank=True)
#     # 开始时间
#     start_time = models.DateTimeField()
#     # 持续时间
#     duration = models.TextField()
#     # 分数
#     grade = models.TextField()
#     # 是否归档
#     is_archived = models.TextField()
#     # 报告名称
#     report_title = models.TextField()
#     # 提问人
#     questioner = models.TextField()
#     # 问题描述
#     question = models.TextField()
#     # 回答情况
#     reply_status = models.TextField()
#     # 问题相关的建议
#     remark = models.TextField(blank=True)
#
#
# # 学术论文
# class Paper(models.Model):
#     # 用户
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     # 姓名
#     real_name = models.TextField(blank=True)
#     # 负责人
#     person_in_charge = models.TextField(blank=True)
#     # 论文名称
#     title = models.TextField()
#     # 作者
#     author = models.TextField()
#     # 以下内容为json格式
#     # 投稿时间
#     contribution_date = models.TextField(blank=True)
#     # 录用时间
#     acceptance_date = models.TextField(blank=True)
#     # 发票提交
#     invoice_submitted = models.TextField(default=True)
#     # 电子版（终稿）提交
#     final_version_submitted = models.TextField(default=True)
#     # 刊物领取和提交
#     journal_received_and_submitted = models.TextField(default=True)
#     # 期刊名称
#     journal_name = models.TextField(blank=True)
#     # 发表年卷期页码
#     paper_location = models.TextField(blank=True)
#     # 检索SCI、EI
#     indexed_by = models.TextField(blank=True)
#     # 备注
#     remark = models.TextField(blank=True)
#
#
# # 获奖
# class Award(models.Model):
#     # 用户
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     # 姓名
#     real_name = models.TextField(blank=True)
#     # 扫描件
#     scanned_version = models.BooleanField(default=False)
#     # 级别量化
#     award_place_quantization = models.TextField()
#     # 获奖级别
#     award_place = models.TextField()
#     # 获奖名称
#     award_name = models.TextField()
#     # 获奖类别
#     award_type = models.TextField()
#     # 级别
#     award_level = models.TextField()
#     # 评奖单位
#     award_sponsor = models.TextField()
#     # 署名及次序
#     awarded_staff_with_order = models.TextField()
#     # 获奖时间
#     award_date = models.DateField()
#     # 署名次序
#     award_order = models.TextField()
#     # 奖金
#     award_money = models.TextField()
#     # 备注
#     remark = models.DateField(blank=True)
#
#
# # 专利
# class Patent(models.Model):
#     # 用户
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     # 姓名
#     real_name = models.TextField(blank=True)
#     # 组名
#     group_name = models.TextField()
#     # 类型
#     type = models.TextField()
#     # 名称
#     name = models.TextField()
#     # 版本号
#     version = models.TextField()
#     # 申请日期
#     application_date = models.DateField()
#     # 授权公告日
#     announcement_date = models.DateField()
#     # 专利号
#     patent_number = models.TextField()
#     # 获得人
#     author = models.TextField()
#     # 署名次序
#     author_order = models.TextField()
#     # 著作权人
#     copyright_owner = models.TextField()
#     # 批准单位
#     authorization_unit = models.TextField()
#     # 日期
#     date = models.DateField(auto_now=True)
#     # 摘要
#     abstract = models.TextField()
#
#
# # 软件著作权
# class Software(models.Model):
#     # 用户
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     # 姓名
#     real_name = models.TextField(blank=True)
#     # 组名
#     group_name = models.TextField()
#     # 类型
#     type = models.TextField()
#     # 名称
#     name = models.TextField()
#     # 版本号
#     version = models.TextField()
#     # 开发完成日
#     finish_date = models.DateField()
#     # 首次发表日
#     announcement_date = models.DateField()
#     # 软件著作权号
#     software_number = models.TextField()
#     # 获得人
#     author = models.TextField()
#     # 署名次序
#     author_order = models.TextField()
#     # 著作权人
#     copyright_owner = models.TextField()
#     # 批准单位
#     authorization_unit = models.TextField()
#     # 日期
#     date = models.DateField(auto_now=True)