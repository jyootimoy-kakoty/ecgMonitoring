from django.shortcuts import render
from .models import HospitalData, PatientData, SensorData, ECGData
from django.http import HttpResponse

#Global Variables
sampleRate = 250
samples = 15
total = samples * sampleRate

# Create your views here.
#Index is the Home Page View
def Index(request):
    hospitals = HospitalData.objects.all()
    """
    #Method 1
    Index = '<h1>Welcome to ECG-Monitoring System</h1>'
    for hospital in hospitals:
        url = '/monitor/' + str(hospital.hospitalID) + '/'
        Index += '<a href =" ' + url + '">' + hospital.hospitalName + '</a><br>'
    return HttpResponse(Index)
    """
    """
    #Method 2
    context = {
        'hospitals': hospitals,
    }
    template = loader.get_template('Monitor/index.html')
    return HttpResponse(template.render(context, request))
    """
    #Method 3
    context = {
        'hospitals': hospitals,
    }
    return render(request, 'Monitor/Index.html', context)

# Data Entry for all DB Models/Tables
def hospitalDataEntry(request):
    hospitalInstance = HospitalData.objects.create(hospitalID = "HTZ12", hospitalName = "Max Hospital", hospitalAddress = "Main Town, Tezpur, Assam-784028")
    p = HospitalData(hospitalID = "HTZ10", hospitalName = "GNRC Hospital", hospitalAddress = "Main Town, Tezpur, Assam-784028")
    p.save()
    return HttpResponse("<h1>Hospital Data inserted successfully!</h1>")

def patientDataEntry(request):
    hospital = HospitalData.objects.filter(hospitalID = "HTZ12")[0]
    patientInstance = PatientData.objects.create(patientID = "PTZ202102270001", patientName = "Ankumoni Hazarika", hospitalID = hospital)
    p = PatientData(patientID = "PTZ202102270002", patientName = "Partha Pratim Churi", hospitalID = hospital)
    p.save()
    return HttpResponse("<h1>Patient Data inserted successfully!</h1>")

def sensorDataEntry(request):
    for j in range(1, 3, 1):
        sensorInstance = SensorData.objects.create(sensorID="HTZ12S00" + str(j), sensorName="ECG00" + str(j))
    return HttpResponse("<h1>Sensor Data inserted successfully!</h1>")

def ecgDataEntry(request):
    import pytz
    import datetime
    import random
    patients = PatientData.objects.all()
    sensors = SensorData.objects.all()
    IST = pytz.timezone('Asia/Kolkata')
    j = 0
    for patient in patients:
        if j < patients.count():
            for i in range(0, sampleRate, 1):
                ecgInstance = ECGData.objects.create(sensorID=sensors[j], patientID = patient, time = datetime.datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S.%f"), data = random.uniform(0, 1023))
        j += 1
    return HttpResponse("<h1>ECG Data inserted successfully!</h1>")

#Detail Views: Expand Index and respective following pages one by one in hierarchy
def hospitalDetails(request, hID):
    hospital = HospitalData.objects.filter(hospitalID = hID)[0]
    patients = PatientData.objects.all()
    """
    #Method 1
    Index = '<h1>Hospital Details: <a href ="/Monitor/">Home</a></h1>\
            <h2> Hospital ID: ' + hospital.hospitalID + ' | Hospital Name: ' + hospital.hospitalName + ' | Address: ' + hospital.hospitalAddress + '</h2> <br><h1>Patient Database</h1>'
    for patient in patients:
        if patient.hospitalID.hospitalID == hID:
            url = '/Monitor/' + str(patient.patientID) + '/'
            Index += '<a href =" ' + url + '">' + patient.patientName + '</a><br>'
    return HttpResponse(Index)
    """
    #Method 2
    context = {
        'hospital': hospital,
        'patients': patients,
        'hID': hID
    }
    return render(request, 'Monitor/hospitalDetails.html', context)
    #pattern = PatientData.objects.filter(patientName__startswith = 'Anku')[0];
    #return HttpResponse("<h2>"" + str(hospital.hospitalID) + " " + str(hospital.hospitalName) + " " + str(hospital.hospitalAddress) + "</h2>")
