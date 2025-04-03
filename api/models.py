from django.db import models
from django.db.models import Max
from django.contrib.auth.models import AbstractUser

class ChildRegistration(models.Model):
    schoolName = models.CharField(max_length=1500)
    patient_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    image = models.TextField()  # Store the GridFS file ID as a string

    def __str__(self):
        return self.name
    
class PediatricAssessment(models.Model):
    schoolName = models.CharField(max_length=1500)
    patient_id = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=50)
    gender = models.CharField(max_length=20)
    complaints = models.TextField(blank=True, null=True)
    pastAdmissions = models.TextField(blank=True, null=True)
    knownCase = models.CharField(max_length=255, blank=True, null=True)
    midArmCircumference  = models.CharField(max_length=255, blank=True, null=True)
    assessmentDate = models.CharField(max_length=50)
    selectedVisionAssessment= models.CharField(max_length=50)
    birthWeight = models.CharField(max_length=50)
    vaccinationStatus = models.JSONField(default=list)
    deficiencies= models.JSONField(default=list)
    headToToeExam = models.JSONField(default=list)
    calorieProteinGaps = models.JSONField(default=list)
    initialRecommendations = models.JSONField(default=list)
    finalOutcome = models.JSONField(default=list)
    
    
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


