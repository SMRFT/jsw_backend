
from rest_framework import serializers
from bson import ObjectId
class ObjectIdField(serializers.Field):
    def to_representation(self, value):
        return str(value)
    def to_internal_value(self, data):
        return ObjectId(data)
    

from .models import ChildRegistration
class ChildRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildRegistration
        fields = '__all__'


from .models import PediatricAssessment
class PediatricAssessmentSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    class Meta:
        model = PediatricAssessment
        fields = "__all__"


from .models import Doctor
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'email', 'username', 'mobile_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        doctor = Doctor(
            email=validated_data['email'],
            username=validated_data['username'],
            mobile_number=validated_data['mobile_number'],
        )
        doctor.set_password(validated_data['password'])
        doctor.save()
        return doctor


from .models import HeightClick
class HeightClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeightClick
        fields = ['patient_id', 'age', 'height','status']


from .models import WeightClick
class WeightClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightClick
        fields = ['patient_id', 'age', 'weight','status']


from .models import HeightandWeightClick
class HeightandWeightClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeightandWeightClick
        fields = ['patient_id', 'age', 'heightandweight']

from .models import TDSCClick
class TDSCClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = TDSCClick
        fields = ['patient_id', 'tdscpoint', 'tdscdescription']

