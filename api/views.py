from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.http import require_http_methods
# Create your views here.
from .Serializers import PediatricAssessmentSerializer
@api_view(['POST'])
def pediatricAssessment(request):
    if request.method == 'POST':
        serializer = PediatricAssessmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Data submitted successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection


@csrf_exempt
def get_assessment_data(request):
    client = MongoClient("mongodb://3.109.210.34:27017/")  # Update with your MongoDB connection string
    db = client["jsw"]  # Replace with your database name
    collection = db["api_pediatricassessment"]  # Replace with your collection name
    if request.method == "GET":
        try:
            # Query MongoDB for all documents
            data = list(collection.find({}))  # Fetch all documents
            
            # Serialize the data
            for item in data:
                item["_id"] = str(item["_id"])  # Convert ObjectId to string
            
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Max

from django.db.models import Max
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PediatricAssessment

@api_view(['GET'])
def generate_patient_id(request):
    # Fetch the highest patient ID explicitly
    last_patient_id = PediatricAssessment.objects.aggregate(
        max_id=Max('patient_id')  # Use Max from django.db.models
    )['max_id']
    
    if last_patient_id:
        patient_number = int(last_patient_id[2:]) + 1  # Extract the numeric part and increment
    else:
        patient_number = 1

    patient_id = f"SH{patient_number:03d}"  # Format the new ID
    return Response({"patient_id": patient_id})


# @csrf_exempt
# @api_view(['POST'])
# def register(request):
#     serializer = PediatricAssessmentSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def get_patient_details(request):
#     patient_id = request.GET.get('patient_id')
#     patientname = request.GET.get('patientname')

#     if patient_id:
#         patient = Patient.objects.filter(patient_id=patient_id).first()
#     elif patientname:
#         patient = Patient.objects.filter(patientname=patientname).first()
#     else:
#         return JsonResponse({'error': 'Please provide either patient_id or patientname'}, status=400)

#     if patient:
#         patient_data = {
#             'patient_id': patient.patient_id,
#             'patientname': patient.patientname,
#             'age': patient.age,
#             'gender': patient.gender,
#             'address':patient.address

#         }
#         return JsonResponse(patient_data)
#     else:
#         return JsonResponse({'error': 'Patient not found'}, status=404)
    


@api_view(['GET'])
def get_patient_details(request):
    patient_id = request.query_params.get('patient_id', None)
    name = request.query_params.get('name', None)
    
    if patient_id:
        # Fetch exact match for patient_id
        patients = PediatricAssessment.objects.filter(patient_id=patient_id)
    elif name and len(name) >= 4:
        # Fetch partial matches for name with at least 4 letters
        patients = PediatricAssessment.objects.filter(name__icontains=name)
    else:
        # Return an empty queryset if no valid query parameter is provided
        patients = PediatricAssessment.objects.none()
    
    serializer = PediatricAssessmentSerializer(patients, many=True)
    return Response(serializer.data)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Doctor
from .Serializers import DoctorSerializer
from django.contrib.auth import authenticate

class RegisterDoctorView(APIView):
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Doctor registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LoginDoctorView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         # Try to authenticate using email as username
#         doctor = authenticate(request, username=email, password=password)

#         if doctor:
#             return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
#         return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)



from django.contrib.auth.hashers import check_password
@csrf_exempt
@api_view(['POST'])
def LoginDoctorView(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        # Find the user by email
        user = Doctor.objects.get(email=email)
        # Check if the password matches
        if check_password(password, user.password):
            # If password matches, login is successful
            return JsonResponse({'message': 'Login successful!'}, status=status.HTTP_200_OK)
        else:
            # If password doesn't match
            return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Doctor.DoesNotExist:
        # If user with given email does not exist
        return JsonResponse({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import HeightClick,WeightClick,HeightandWeightClick
from .Serializers import HeightClickSerializer,WeightClickSerializer,HeightandWeightClickSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def save_clicked_point(request):
    patient_id = request.data.get('patient_id')
    age = request.data.get('age')
    height = request.data.get('height')

    if not patient_id or not age or not height:
        return Response({"error": "Missing data"}, status=400)

    # Save the clicked data into the database
    serializer = HeightClickSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Data saved successfully"}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def save_weightclicked_point(request):
    patient_id = request.data.get('patient_id')
    age = request.data.get('age')
    weight = request.data.get('weight')

    if not patient_id or not age or not weight:
        return Response({"error": "Missing data"}, status=400)

    # Save the clicked data into the database
    serializer = WeightClickSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Data saved successfully"}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def save_Heightandweight_point(request):
    patient_id = request.data.get('patient_id')
    age = request.data.get('age')
    height = request.data.get('height')

    if not patient_id or not age or not height:
        return Response({"error": "Missing data"}, status=400)

    # Save the clicked data into the database
    serializer = HeightandWeightClickSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Data saved successfully"}, status=201)
    return Response(serializer.errors, status=400)



@api_view(['GET'])
def get_graph_data(request, patient_id):
    # Get all the data for the specified patient
    data = HeightClick.objects.filter(patient_id=patient_id)
    serializer = HeightClickSerializer(data, many=True)
    return Response(serializer.data)


from django.http import JsonResponse
import json


@api_view(['DELETE'])
def delete_clicked_point(request):
    try:
        data = json.loads(request.body)
        patient_id = data.get('patient_id')
        age = data.get('age')
        height = data.get('height')

        # Validate input data
        if not patient_id or not age or not height:
            return JsonResponse({"error": "Invalid data"}, status=400)

        # Filter and delete by patient_id, age, and height
        deleted_count, _ = HeightClick.objects.filter(
            patient_id=patient_id,
            age=str(age),
            height=float(height)
        ).delete()

        if deleted_count > 0:
            return JsonResponse({"message": "Point deleted successfully"}, status=200)
        else:
            return JsonResponse({"error": "Point not found"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


from django.http import JsonResponse
from rest_framework.decorators import api_view
import json
from .models import WeightClick  # Replace with the correct model name for weight clicks

@api_view(['DELETE'])
def delete_clicked_weight(request):
    try:
        data = json.loads(request.body)
        patient_id = data.get('patient_id')
        age = data.get('age')
        weight = data.get('weight')


        if not patient_id or not age or not weight:
            return JsonResponse({"error": "Invalid data"}, status=400)
        # Filter and delete by patient_id, age, and weight
        deleted_count, _ = HeightClick.objects.filter(
            patient_id=patient_id,
            age=str(age),
            weight=float(weight)
        ).delete()
        if deleted_count > 0:
            return JsonResponse({"message": "Point deleted successfully"}, status=200)
        else:
            return JsonResponse({"error": "Point not found"}, status=404)
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['GET'])
def get_weightgraph_data(request, patient_id):
    # Get all the data for the specified patient
    data = WeightClick.objects.filter(patient_id=patient_id)
    serializer = WeightClickSerializer(data, many=True)
    return Response(serializer.data)


from .models import TDSCClick
from .Serializers import TDSCClickSerializer
@api_view(['POST'])
def tdscclicked_point(request):
    patient_id = request.data.get('patient_id')
    tdscpoint = request.data.get('tdscpoint')
    if not patient_id  or not tdscpoint:
        return Response({"error": "Missing data"}, status=400)
    # Save the clicked data into the database
    serializer = TDSCClickSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Data saved successfully"}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_tdscclicked_point(request, patient_id):
    data = TDSCClick.objects.filter(patient_id=patient_id).values("tdscpoint")
    return Response(list(data))