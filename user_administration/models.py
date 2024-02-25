from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.utils.translation import gettext as _
from PIL import Image


# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True, editable=True, validators=[MinLengthValidator(5)])
    roll_no = models.CharField(max_length=100, unique=True, primary_key=True,
                               validators=[MinLengthValidator(10), MaxLengthValidator(10)])
    branch = models.CharField(max_length=100, editable=True, validators=[MinLengthValidator(6)])
    year = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], editable=True)
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg', blank=True)
    password = models.CharField(max_length=128)
    REQUIRED_FIELDS = ['roll_no', 'branch', 'year']

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
        return f'{self.username} - {self.roll_no}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Adding new custom user to the student group
        student_group = Group.objects.get(name='student')
        self.groups.add(student_group)

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
