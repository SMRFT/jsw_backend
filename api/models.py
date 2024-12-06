from django.db import models
from django.db.models import Max

# Create your models here.
class PediatricAssessment(models.Model):
    patient_id = models.CharField(max_length=20, unique=True, editable=False)
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=50)
    gender = models.CharField(max_length=20)
    address = models.TextField()
    complaints = models.TextField(blank=True, null=True)
    pastAdmissions = models.TextField(blank=True, null=True)
    knownCase = models.CharField(max_length=255, blank=True, null=True)
    midArmCircumference  = models.CharField(max_length=255, blank=True, null=True)
    assessmentDate = models.CharField(max_length=50)
    birthWeight = models.CharField(max_length=50)
    vaccinationStatus = models.JSONField(default=list)
    deficiencies= models.JSONField(default=list)
    headToToeExam = models.JSONField(default=list)
    calorieProteinGaps = models.JSONField(default=list)
    initialRecommendations = models.JSONField(default=list)
    finalOutcome = models.JSONField(default=list)
    def save(self, *args, **kwargs):
        if not self.patient_id:
            # Fetch the highest patient ID explicitly
            last_patient_id = PediatricAssessment.objects.aggregate(
                max_id=Max('patient_id')
            )['max_id']
            
            if last_patient_id:
                patient_number = int(last_patient_id[2:]) + 1
            else:
                patient_number = 1

            self.patient_id = f"SH{patient_number:03d}"  # Format the new ID
        super().save(*args, **kwargs)

    


from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class Doctor(AbstractUser):
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'mobile_number']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='doctor_groups',  # Add unique related_name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='doctor_user_permissions',  # Add unique related_name
        blank=True,
    )

    def __str__(self):
        return self.email



from django.db import models
from django.db import models

from django.db import models

class HeightClick(models.Model):
    patient_id = models.CharField(max_length=100)
    age = models.CharField(max_length=50)
    height = models.FloatField()
    status = models.CharField(max_length=50)
    class Meta:
        unique_together = ('patient_id', 'age', 'height')  # Optional: Ensure uniqueness across these fields.

    def __str__(self):
        return f"{self.patient_id} - {self.age} - {self.height}"



class WeightClick(models.Model):
    patient_id = models.CharField(max_length=100)
    age = models.CharField(max_length=50)
    weight = models.FloatField()
    status = models.CharField(max_length=50)

    class Meta:
        unique_together = ('patient_id', 'age', 'weight') 
    def __str__(self):
        return f"{self.patient_id} - {self.age} - {self.weight}"


class HeightandWeightClick(models.Model):
    patient_id = models.CharField(max_length=100,primary_key=True)
    age = models.CharField(max_length=50)
    heightandweight = models.FloatField()

    def __str__(self):
        return f"{self.patient_id} - {self.age} - {self.heightandweight}"
    
class TDSCClick(models.Model):
    patient_id = models.CharField(max_length=100)
    tdscpoint = models.CharField(max_length=50)
    tdscdescription = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.patient_id} - {self.age} - {self.tdscpoint}"


