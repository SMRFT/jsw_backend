from django.urls import path
from . import views
from .views import RegisterDoctorView, LoginDoctorView,WeightClick,get_weightgraph_data,delete_clicked_point,HeightandWeightClick,delete_clicked_weight



urlpatterns = [
path("pediatricAssessment/", views.pediatricAssessment, name="pediatricAssessment"),
path("get-data/",views.get_assessment_data,name="get-data"),
path('generate-patient-id/', views.generate_patient_id, name='generate-patient-id'),
path('patient-get/', views.get_patient_details, name='get_patient_details'),
path('register/', RegisterDoctorView.as_view(), name='register'),
path('login/', LoginDoctorView, name='login'),
path('save-clicked-point/', views.save_clicked_point, name='save_clicked_point'),
path('get-graph-data/<str:patient_id>/', views.get_graph_data, name='get_graph_data'),
path('weight-click/', views.save_weightclicked_point, name='weight-click'),
path('get-weight-graph-data/<str:patient_id>/',  views.get_weightgraph_data, name='get-weight-graph-data'),
path('delete-clicked-point/', views.delete_clicked_point, name='delete'),
path('delete-clicked-point-weight/', views.delete_clicked_weight, name='delete'),
path('height-and-weight-click/', views.HeightandWeightClick, name='height-and-weight-click'),
path("tdscclicked_point/", views.tdscclicked_point, name="tdscclicked_point"),
path("get_tdscclicked_point/<str:patient_id>/", views.get_tdscclicked_point, name="get_tdscclicked_point"),
]