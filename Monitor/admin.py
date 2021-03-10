from django.contrib import admin
from .models import HospitalData, PatientData, SensorData, ECGData

# Register your models here.
admin.site.register(HospitalData)
admin.site.register(PatientData)
admin.site.register(SensorData)
admin.site.register(ECGData)