from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Max
from pymongo import MongoClient
from django.http import JsonResponse
import json
from django.http import HttpResponse, Http404
from django.conf import settings
from gridfs import GridFS
from bson import ObjectId
from .models import ChildRegistration
from .Serializers import ChildRegistrationSerializer

class ChildRegistrationView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # MongoDB Configuration
        client = MongoClient("mongodb://3.109.210.34:27017/")
        db = client['jsw']
        fs = GridFS(db)
        data = request.data

        # Save image to GridFS
        image = data.get('image')
        if image:
            file_id = fs.put(image, filename=image.name)
            data['image'] = str(file_id)  # Save the file ID as a string in the database

        serializer = ChildRegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Patient registered successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    def get(self, request, *args, **kwargs):
        school_name = request.query_params.get('schoolName')
        if not school_name:
            return Response({"error": "School name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        children = ChildRegistration.objects.filter(schoolName=school_name)
        serializer = ChildRegistrationSerializer(children, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChildRegistration


class ChildDataView(APIView): 
    def get(self, request, *args, **kwargs):
        # Fetch patient_id from query parameters
        patient_id = request.query_params.get('patient_id')

        if patient_id:
            # Get specific child by patient_id
            try:
                child = ChildRegistration.objects.get(patient_id=patient_id)
                serializer = ChildRegistrationSerializer(child)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ChildRegistration.DoesNotExist:
                return Response({"message": "No data found for the given patient_id"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Fetch all data from ChildRegistration
            children = ChildRegistration.objects.all()
            serializer = ChildRegistrationSerializer(children, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


    

@api_view(['GET'])
def get_vaccination_status(request, school_name, patient_id):
    try:
        assessment = PediatricAssessment.objects.filter(
            schoolName=school_name, 
            patient_id=patient_id
        ).order_by('-assessmentDate').first()
        
        if assessment:
            return Response({
                'vaccinationStatus': assessment.vaccinationStatus.split(',') if assessment.vaccinationStatus else [],
                'message': 'Vaccination status retrieved successfully.'
            }, status=200)
        else:
            return Response({
                'vaccinationStatus': [],
                'message': 'No vaccination status found for this patient.'
            }, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
        

from .Serializers import PediatricAssessmentSerializer
@api_view(['POST'])
def pediatricAssessment(request):
    if request.method == 'POST':
        # Check if patient_id exists in the request data
        patient_id = request.data.get('patient_id', None)
        
        if patient_id:
            # Check if this patient already exists
            existing_patient = PediatricAssessment.objects.filter(patient_id=patient_id).first()
            if existing_patient:
                # If the patient exists, don't generate a new ID and save the new data
                serializer = PediatricAssessmentSerializer(existing_patient, data=request.data, partial=True)
            else:
                # If no patient exists with this ID, generate a new patient ID
                serializer = PediatricAssessmentSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Data submitted successfully!"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Patient ID is required."}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def getPediatricReport(request, patient_id):
    try:
        # Fetch all assessments for the given patient_id
        assessments = PediatricAssessment.objects.filter(patient_id=patient_id)
        
        if not assessments.exists():
            return Response({"message": "No records found for this patient ID."}, status=status.HTTP_404_NOT_FOUND)

        # Initialize an empty dictionary to compile the data
        compiled_data = {
            "patient_id": patient_id,
            "name": assessments[0].name,
            "age": assessments[0].age,
            "gender": assessments[0].gender,
            "schoolName": assessments[0].schoolName,
            "assessmentDates": [],
            "complaints": [],
            "pastAdmissions": [],
            "knownCase": assessments[0].knownCase,
            "midArmCircumference": [],
            "selectedVisionAssessments": [],
            "birthWeight": assessments[0].birthWeight,
            "vaccinationStatus": [],
            "deficiencies": [],
            "headToToeExam": [],
            "calorieProteinGaps": [],
            "initialRecommendations": [],
            "finalOutcome": [],
        }

        # Consolidate data
        for assessment in assessments:
            compiled_data["assessmentDates"].append(assessment.assessmentDate)
            compiled_data["complaints"].extend(assessment.complaints.split(',') if assessment.complaints else [])
            compiled_data["pastAdmissions"].extend(assessment.pastAdmissions.split(',') if assessment.pastAdmissions else [])
            compiled_data["midArmCircumference"].append(assessment.midArmCircumference)
            compiled_data["selectedVisionAssessments"].append(assessment.selectedVisionAssessment)
            compiled_data["vaccinationStatus"].extend(assessment.vaccinationStatus)
            compiled_data["deficiencies"].extend(assessment.deficiencies)
            compiled_data["headToToeExam"].extend(assessment.headToToeExam)
            compiled_data["calorieProteinGaps"].extend(assessment.calorieProteinGaps)
            compiled_data["initialRecommendations"].extend(assessment.initialRecommendations)
            compiled_data["finalOutcome"].extend(assessment.finalOutcome)

        # Remove duplicates
        for key in ["complaints", "pastAdmissions", "vaccinationStatus", "deficiencies", "headToToeExam", "calorieProteinGaps", "initialRecommendations", "finalOutcome"]:
            compiled_data[key] = list(set(compiled_data[key]))

        return Response(compiled_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        

from .models import ChildRegistration
@api_view(['GET'])
def generate_patient_id(request):
    # Fetch the highest patient ID explicitly
    last_patient_id = ChildRegistration.objects.aggregate(
        max_id=Max('patient_id')  # Use Max from django.db.models
    )['max_id']
    
    if last_patient_id:
        patient_number = int(last_patient_id[2:]) + 1  # Extract the numeric part and increment
    else:
        patient_number = 1

    patient_id = f"SH{patient_number:03d}"  # Format the new ID
    return Response({"patient_id": patient_id})
    

from .models import PediatricAssessment
@api_view(['GET'])
def get_patient_details(request):
    patient_id = request.query_params.get('patient_id', None)
    name = request.query_params.get('name', None)
    
    if patient_id:
        # Fetch the first match for patient_id (if multiple patients exist with the same ID)
        patient = PediatricAssessment.objects.filter(patient_id=patient_id).first()
        if patient:
            patients = [patient]  # Wrap in a list to make it serializable
        else:
            patients = []
    elif name and len(name) >= 4:
        # Fetch partial matches for name with at least 4 letters
        patients = PediatricAssessment.objects.filter(name__icontains=name)
    else:
        # Return an empty queryset if no valid query parameter is provided
        patients = PediatricAssessment.objects.none()
    
    serializer = PediatricAssessmentSerializer(patients, many=True)
    return Response(serializer.data)


from .models import Doctor
from .Serializers import DoctorSerializer
class RegisterDoctorView(APIView):
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Doctor registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    
def serve_image(request, image_id):
    # MongoDB Configuration
    client = MongoClient("mongodb://3.109.210.34:27017/")
    db = client['jsw']
    fs = GridFS(db)
    try:
        # Convert the image_id from string to ObjectId
        file_id = ObjectId(image_id)

        # Fetch the file from GridFS
        file = fs.get(file_id)

        # Return the file as a response
        response = HttpResponse(file.read(), content_type='image/jpeg')
        response['Content-Disposition'] = f'inline; filename={file.filename}'
        return response

    except Exception as e:
        # Return a 404 error if the image is not found
        raise Http404(f"Image not found: {str(e)}")
from .models import HeightClick
from .Serializers import HeightClickSerializer
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


from .Serializers import WeightClickSerializer
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


from .Serializers import HeightandWeightClickSerializer
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
        deleted_count, _ = WeightClick.objects.filter(
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
    data = TDSCClick.objects.filter(patient_id=patient_id).values("tdscpoint",'tdscdescription')
    return Response(list(data))