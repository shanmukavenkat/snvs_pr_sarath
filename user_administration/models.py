import django.apps
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.utils.translation import gettext as _
from PIL import Image
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation
from complaint_administration.models.complaint_models import Complaint
from user_administration.escalation_models import Role


# Create your models here.

class CustomUser(AbstractUser):
    role = models.ForeignKey(to=Role, to_field='role', on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=100, primary_key=True, editable=True, validators=[MinLengthValidator(5)])
    image = models.ImageField(upload_to='profile_pics/', blank=True)
    password = models.CharField(max_length=128)
    complaint = GenericRelation(Complaint)
    # Specify unique related names for the groups and user_permissions fields
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='custom_users',  # Change the related name to 'custom_users'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_users',  # Change the related name to 'custom_users'
    )

    def __str__(self):
        return f'{self.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.role == 'admin':
            self.is_staff = True

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)


class Branch(models.Model):
    branch = models.CharField(max_length=255, primary_key=True)
    REQUIRED_FIELDS = ['branch']

    class Meta:
        verbose_name_plural = 'Branches'

    def __str__(self):
        return f'{self.branch}'


class Class(models.Model):
    branch = models.ForeignKey(Branch, to_field='branch', on_delete=models.CASCADE)
    section = models.CharField(max_length=255, null=True, blank=True)

    REQUIRED_FIELDS = ['branch', 'section']

    class Meta:
        verbose_name_plural = 'Classes'
        constraints = [
            models.UniqueConstraint(fields=['branch', 'section'],
                                    name='unique_branch_section'),
            models.UniqueConstraint(fields=['branch'], condition=models.Q(section__isnull=True), name='unique_branch')
        ]

    def __str__(self):
        return f'{self.branch}  -  {self.section}'


# class Staff(models.Model):
#     user = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE,
#                                 related_name='staff_user')
#     branch = models.ForeignKey(to=Branch, to_field='branch', editable=True, validators=[MinLengthValidator(6)],
#                                on_delete=models.CASCADE, blank=True, null=True)
#
#     class Meta:
#         verbose_name_plural = 'Staff'
#
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         if self.user.role_id == 'class_teacher':
#             pass
#
#     def __str__(self):
#         return f'{self.user.username} - {self.branch}'

class Counsellor(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='counsellor_user')
    complaints = GenericRelation(Complaint, related_name='counsellor_complaints',
                                 related_query_name='counsellor_complaints')
    branch = models.ForeignKey(Branch, to_field='branch', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'


class Student(models.Modedl):
    id = models.PositiveIntegerField(primary_key=True)
    user = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE,
                                related_name='student_user')
    roll_no = models.CharField(max_length=100, unique=True,
                               validators=[MinLengthValidator(10), MaxLengthValidator(10)])
    branch = models.ForeignKey(to=Branch, to_field='branch', editable=True, validators=[MinLengthValidator(6)],
                               on_delete=models.CASCADE)
    year = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], editable=True)
    counsellor = models.ForeignKey(to=Counsellor, on_delete=models.CASCADE, blank=True, null=True)
    class_room = models.ForeignKey(Class, on_delete=models.CASCADE)
    complaints = GenericRelation(to=Complaint, related_name='student_complaints',
                                 related_query_name='student_complaints')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Guard for student role
        if self.user.role_id != 'Student':
            raise ValidationError('The user is already a Student')

        student = Group.objects.get(name='student')
        self.user.groups.add(student)

    def __str__(self):
        return f'{self.user.username} - {self.roll_no}'


# class StudentClass(models.Model):
#     student = models.OneToOneField(CustomUser, on_delete=models.CASCADE, to_field='username', primary_key=True)
#     student_class = models.ForeignKey(Class, on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name_plural = 'StudentClasses'
#         constraints = [
#             models.UniqueConstraint(fields=['student', 'student_class'], name='unique_class_student'),
#         ]


class ClassTeacher(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, blank=False)
    class_room = models.ForeignKey(to=Class, on_delete=models.CASCADE, blank=False)
    complaints = GenericRelation(Complaint, related_name='class_teacher_complaints',
                                 related_query_name='class_teacher_complaints')
    branch = models.ForeignKey(to=Branch, to_field='branch', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'


class HeadOfDepartment(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, blank=False, null=False)
    branch = models.ForeignKey(to=Branch, on_delete=models.CASCADE, blank=False)
    complaints = GenericRelation(Complaint, related_name='hod_complaints', related_query_name='hod_complaints')

    class Meta:
        verbose_name_plural = 'Head Of Department'

    def __str__(self):
        return f'{self.user.username}'
# class UserRole(models.Model):
#     user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
#     role = models.ForeignKey(to=Role, to_field='role', on_delete=models.CASCADE, blank=True, null=True)
