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
    # TODO User表需要添加额外的信息，如新生基础信息
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
    password = models.CharField(max_length=128)
    real_name = models.CharField(_, max_length=30, blank=True)
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

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     """Send an email to this user."""
    #     send_mail(subject, message, from_email, [self.email], **kwargs)


class MettingRecord(models.Model):
    # TODO 会议记录及template编写
    pass


class Target(models.Model):
    user_id = models.IntegerField()
    term = models.CharField(max_length=32)
    time = models.DateTimeField(auto_now=True)
    expected_result = models.CharField(max_length=32)
    time_consumed = models.IntegerField()
    content = models.TextField()
    end_of_term_summary = models.TextField()


class Plan(models.Model):
    user_id = models.IntegerField()
    type = models.CharField(max_length=32)
    plan_name = models.CharField(max_length=32)
    plan_result = models.TextField()
    is_reviewed = models.BooleanField()
    head_person = models.CharField(max_length=32)
    affiliated_person = models.TextField()
    planed_time = models.IntegerField()
    planed_start_time = models.DateField()
    planed_end_time = models.DateField()
    actual_time = models.IntegerField()
    actual_start_time = models.DateField()
    actual_end_time = models.DateField()
    advanced_postponed_time = models.IntegerField()
    remark = models.TextField()


class WorkSummary(models.Model):
    user_id = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=32)
    summary = models.TextField()
    average_time = models.CharField(max_length=32)
    man_day = models.IntegerField()
    natural_day = models.IntegerField()
    remark = models.TextField()


class TimeTable(models.Model):
    user_id = models.IntegerField()
    date = models.DateField()
    monday = models.TextField()
    tuesday = models.TextField()
    wednesday = models.TextField()
    thursday = models.TextField()
    friday = models.TextField()
    saturday = models.TextField()
    sunday = models.TextField()


class weekly_summary(models.Model):
    # TODO 把周报model移到user_info里
    real_name = models.CharField(max_length=150)
    this_week_task = models.TextField()
    next_week_task = models.TextField()
    submit_time = models.DateTimeField(auto_now=True)
    week = models.IntegerField(default=0)
    is_present = models.BooleanField(default=False)
    is_absent = models.BooleanField(default=False)
    is_left = models.BooleanField(default=False)
