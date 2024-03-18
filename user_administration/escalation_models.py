from django.contrib.auth.models import models
from django.core.validators import MinLengthValidator


class Role(models.Model):
    role = models.CharField(max_length=20, validators=[MinLengthValidator(4)], primary_key=True)

    def __str__(self):
        return f'{self.role}'


class EscalationStructure(models.Model):
    class Meta:
        verbose_name_plural = 'EscalationStructure'
        constraints = [
            # The role must be unique w.r.t id
            models.UniqueConstraint(fields=['id', 'role'], name='unique_id_role')
        ]
    id = models.IntegerField(primary_key=True)
    role = models.ForeignKey(to=Role, to_field='role', on_delete=models.CASCADE)
    student_relation_identifier = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.role_id}'
