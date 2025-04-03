from django.urls import path
from . import views

urlpatterns = [
path("child-registration/", views.ChildRegistrationView.as_view(), name="child-registration"),
path("child-data/", views.ChildDataView.as_view(), name="child-data"),
path('media/<str:image_id>/', views.serve_image, name='serve_image'),
path('vaccination_status/<str:school_name>/<str:patient_id>/', views.get_vaccination_status, name='vaccination_status'),
path("pediatricAssessment/", views.pediatricAssessment, name="pediatricAssessment"),
path('generate-patient-id/', views.generate_patient_id, name='generate-patient-id'),
path("get-data/",views.get_assessment_data,name="get-data"),
path('generateFinalReport/<str:patient_id>/', views.getPediatricReport, name="generateFinalReport"),
path('patient-get/', views.get_patient_details, name='get_patient_details'),
path('register/', views.RegisterDoctorView.as_view(), name='register'),
path('login/', views.LoginDoctorView, name='login'),
path('save-clicked-point/', views.save_clicked_point, name='save_clicked_point'),
path('get-graph-data/<str:patient_id>/', views.get_graph_data, name='get_graph_data'),
path('weight-click/', views.save_weightclicked_point, name='weight-click'),
path('get-weight-graph-data/<str:patient_id>/',  views.get_weightgraph_data, name='get-weight-graph-data'),
path('delete-clicked-point/', views.delete_clicked_point, name='delete'),
path('delete-clicked-point-weight/', views.delete_clicked_weight, name='delete'),
path("tdscclicked_point/", views.tdscclicked_point, name="tdscclicked_point"),
path("get_tdscclicked_point/<str:patient_id>/", views.get_tdscclicked_point, name="get_tdscclicked_point"),
]