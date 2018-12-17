from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', False)
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('用户名'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    current_user = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    # 姓名
    real_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_student = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(
        _('permission'),
        default=False,
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    # 性别
    gender = models.TextField(blank=True)
    # 民族
    nationality = models.TextField(blank=True)
    # 生源地
    born_in = models.TextField(blank=True)
    # 身份证号
    id_number = models.TextField(blank=True)
    # 学号
    student_id = models.TextField(blank=True)
    # 入学时间
    entrance_time = models.TextField(blank=True)
    # 毕业时间
    graduate_time = models.TextField(blank=True)
    # 专业
    major = models.TextField(blank=True)
    # 组别
    group_name = models.TextField(blank=True)
    # 导师
    tutor = models.TextField(blank=True)
    # 银行名称
    bank_name = models.TextField(blank=True)
    # 银行卡号
    bank_id = models.TextField(blank=True)
    # 电话号码
    phone_number = models.TextField(blank=True)
    # email
    email = models.TextField(blank=True)
    # 毕业学校
    past_school = models.TextField(blank=True)
    # 原单位
    past_unit = models.TextField(blank=True)
    # 论文得分
    thesis_defense_score = models.TextField(blank=True)
    # 论文题目
    degree_paper = models.TextField(blank=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)


    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     """Send an email to this user."""
    #     send_mail(subject, message, from_email, [self.email], **kwargs)


# 课表
class TimeTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 班级名称
    class_name = models.TextField()
    # 教师名称
    teacher_name = models.TextField()
    # 开始周
    week_start = models.IntegerField()
    # 结束周
    week_end = models.IntegerField()
    # 星期
    day = models.IntegerField()
    # 大节
    class_number = models.IntegerField()
    # 上课地点
    class_location = models.TextField()


# 资产
class Asset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.TextField()
    name = models.TextField()
    model = models.TextField()
    manufacturer = models.TextField()
    number = models.TextField()
    parameter = models.TextField()
    buying_date = models.DateField()
    storing_place = models.TextField()
