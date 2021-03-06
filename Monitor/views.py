from django.shortcuts import render
from .models import HospitalData, PatientData, SensorData, ECGData
from django.http import HttpResponse, Http404, StreamingHttpResponse
import json
from django.core import serializers
from math import floor
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import logInForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#Global Variables
sampleRate = 250
samples = 4
total = samples * sampleRate

# Create your views here.
#Index is the Home Page View
@login_required(login_url='/Monitor/logIn')
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
@login_required(login_url='/Monitor/logIn')
def hospitalDataEntry(request):
    hospitalInstance = HospitalData.objects.create(hospitalID = "HTZ12", hospitalName = "Max Hospital", hospitalAddress = "Main Town, Tezpur, Assam-784028")
    p = HospitalData(hospitalID = "HTZ10", hospitalName = "GNRC Hospital", hospitalAddress = "Main Town, Tezpur, Assam-784028")
    p.save()
    return HttpResponse("<h1>Hospital Data inserted successfully!</h1>")

@login_required(login_url='/Monitor/logIn')
def patientDataEntry(request):
    hospital = HospitalData.objects.filter(hospitalID = "HTZ12")[0]
    patientInstance = PatientData.objects.create(patientID = "PTZ202102270001", patientName = "Ankumoni Hazarika", hospitalID = hospital)
    p = PatientData(patientID = "PTZ202102270002", patientName = "Partha Pratim Churi", hospitalID = hospital)
    p.save()
    return HttpResponse("<h1>Patient Data inserted successfully!</h1>")

@login_required(login_url='/Monitor/logIn')
def sensorDataEntry(request):
    for j in range(1, 3, 1):
        sensorInstance = SensorData.objects.create(sensorID="HTZ12S00" + str(j), sensorName="ECG00" + str(j))
    return HttpResponse("<h1>Sensor Data inserted successfully!</h1>")

@login_required(login_url='/Monitor/logIn')
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
@login_required(login_url='/Monitor/logIn')
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

@login_required(login_url='/Monitor/logIn')
def patientDetails(request, pID):
    patient = PatientData.objects.filter(patientID = pID)[0]
    """
    #Method 1
    Index = '<h1>Patient Details: <a href ="/Monitor/">Home</a></h1>\
            <h2>Patient ID: ' + patient.patientID + ' | Patient Name: ' + patient.patientName + ' | Hospital ID: ' + patient.hospitalID.hospitalID + '</h2>\
            <br><h1>ECG Data</h1>'
    return HttpResponse(Index)
    """
    #Method 2
    context = {
        'patient': patient,
        'pID': pID
    }
    render(request, 'Monitor/patientDetails.html', context)
    return ecgDetails(request, pID, patient)

@login_required(login_url='/Monitor/logIn')
def ecgDetails(request, pID, patient):
    ecgDatas = ECGData.objects.all()#.order_by('-time')[:10]
    patients = PatientData.objects.all()
    if not ecgDatas:
        raise Http404("Aw! It's an error.")
    else:
        ecgFiltered = ecgDatas.filter(patientID = patient)
        currentSamples = floor(ecgFiltered.count() / sampleRate)
        if ecgFiltered.count() < sampleRate:
            currentSamples = 1
        json_serializer = serializers.get_serializer("json")()
        print(currentSamples, ecgFiltered.count())
        ecg = json_serializer.serialize(ecgFiltered.order_by('time')[(currentSamples - 1) * sampleRate : ecgFiltered.count()], ensure_ascii=False)
        #ecg = json_serializer.serialize(ecgDatas.order_by('time')[3500 : 3750], ensure_ascii=False)
        #ecg = json_serializer.serialize(ecgDatas.order_by('-time')[:10], ensure_ascii=False)
        context = {
            'ECG': ecgFiltered.order_by('-time')[0 : (currentSamples - 1) * sampleRate],
            #'ecgDatas': ecgDatas[3500 : 3750],
            'ecg': ecg,
            'pID': pID,
            'patient': patient,
            'patients': patients,
            'sampleRate': sampleRate,
            'samples': samples,
            'currentSamples': currentSamples
        }
        return render(request, 'Monitor/ecgDetails.html', context)
    def contextTransfer():
        return context

@login_required(login_url='/Monitor/logIn')
def conciseTable(request, pID):
    ecgDatas = ECGData.objects.all()#.order_by('-time')[:10]
    patients = PatientData.objects.all()
    patient = PatientData.objects.filter(patientID = pID)[0]
    if not ecgDatas:
        raise Http404("Aw! It's an error.")
    else:
        ecgFiltered = ecgDatas.filter(patientID = patient)
        currentSamples = floor(ecgFiltered.count() / sampleRate)
        if ecgFiltered.count() < sampleRate:
            currentSamples = 1
        json_serializer = serializers.get_serializer("json")()
        print(currentSamples, ecgFiltered.count())
        ecg = json_serializer.serialize(ecgFiltered.order_by('time')[(currentSamples - 1) * sampleRate : ecgFiltered.count()], ensure_ascii=False)
        #ecg = json_serializer.serialize(ecgDatas.order_by('time')[3500 : 3750], ensure_ascii=False)
        #ecg = json_serializer.serialize(ecgDatas.order_by('-time')[:10], ensure_ascii=False)
        context = {
            'ECG': ecgFiltered.order_by('-time')[0 : (currentSamples - 1) * sampleRate],
            #'ecgDatas': ecgDatas[3500 : 3750],
            'pID': pID,
            'patient': patient,
            'patients': patients,
            'sampleRate': sampleRate,
            'samples': samples,
            'currentSamples': currentSamples
        }

        return render(request, 'Monitor/conciseTable.html', context)

@login_required(login_url='/Monitor/logIn')
def sample(request, pID):
    ecgDatas = ECGData.objects.all()#.order_by('-time')[:10]
    patients = PatientData.objects.all()
    patient = PatientData.objects.filter(patientID = pID)[0]
    if not ecgDatas:
        raise Http404("Aw! It's an error.")
    else:
        ecgFiltered = ecgDatas.filter(patientID = patient)
        currentSamples = floor(ecgFiltered.count() / sampleRate)
        if ecgFiltered.count() < sampleRate:
            currentSamples = 1
        print(currentSamples, ecgFiltered.count())
        ecg = ecgFiltered.order_by('time')[(currentSamples - 1) * sampleRate : ecgFiltered.count()]
        sensor = ecg[0].sensorID.sensorID
        data = []
        for row in ecg:
            row = {'sensorID':sensor, 'patientID': pID, 'time': row.time, 'data': row.data}
            data.append(row)

        return JsonResponse(data, safe=False)
        """json_serializer = serializers.get_serializer("json")()
        ecg = json_serializer.serialize(ecgFiltered.order_by('time')[(currentSamples - 1) * sampleRate : ecgFiltered.count()], ensure_ascii=False)
        context = {
            'ecg': ecg,
            'pID': pID,
            'patient': patient,
            'patients': patients,
            'sampleRate': sampleRate,
            'samples': samples,
            'currentSamples': currentSamples
        }
        return render(request, 'Monitor/chart.html', context)"""

@login_required(login_url='/Monitor/logIn')
def sampleAll(request, pID):
    ecgDatas = ECGData.objects.all()#.order_by('-time')[:10]
    patients = PatientData.objects.all()
    patient = PatientData.objects.filter(patientID = pID)[0]
    if not ecgDatas:
        raise Http404("Aw! It's an error.")
    else:
        ecgFiltered = ecgDatas.filter(patientID = patient)
        currentSamples = floor(ecgFiltered.count() / sampleRate)
        if ecgFiltered.count() < sampleRate:
            currentSamples = 1
        print(currentSamples, ecgFiltered.count())
        ecg = ecgFiltered.order_by('time')[ : ecgFiltered.count()]
        sensor = ecg[0].sensorID.sensorID
        data = []
        for row in ecg:
            row = {'sensorID':sensor, 'patientID': pID, 'time': row.time, 'data': row.data}
            data.append(row)

        return JsonResponse(data, safe=False)
        """json_serializer = serializers.get_serializer("json")()
        ecg = json_serializer.serialize(ecgFiltered.order_by('time')[(currentSamples - 1) * sampleRate : ecgFiltered.count()], ensure_ascii=False)
        context = {
            'ecg': ecg,
            'pID': pID,
            'patient': patient,
            'patients': patients,
            'sampleRate': sampleRate,
            'samples': samples,
            'currentSamples': currentSamples
        }
        return render(request, 'Monitor/chart.html', context)"""

@login_required(login_url='/Monitor/logIn')
def chart(request, pID):
    ecgDatas = ECGData.objects.all()#.order_by('-time')[:10]
    patients = PatientData.objects.all()
    patient = PatientData.objects.filter(patientID = pID)[0]
    if not ecgDatas:
        raise Http404("Aw! It's an error.")
    else:
        ecgFiltered = ecgDatas.filter(patientID = patient)
        currentSamples = floor(ecgFiltered.count() / sampleRate)
        if ecgFiltered.count() < sampleRate:
            currentSamples = 1
        print(currentSamples, ecgFiltered.count())
        ecg = ecgFiltered.order_by('time')[(currentSamples - 1) * sampleRate : ecgFiltered.count()]
        json_serializer = serializers.get_serializer("json")()
        ecg = json_serializer.serialize(ecgFiltered.order_by('time')[(currentSamples - 1) * sampleRate : ecgFiltered.count()], ensure_ascii=False)
        context = {
            'ecg': ecg,
            'pID': pID,
            'patient': patient,
            'patients': patients,
            'sampleRate': sampleRate,
            'samples': samples,
            'currentSamples': currentSamples
        }
        return render(request, 'Monitor/chart.html', context)

@login_required(login_url='/Monitor/logIn')
def completeTable(request, pID):
    patient = PatientData.objects.filter(patientID = pID)[0]
    patients = PatientData.objects.all()
    ecgDatas = ECGData.objects.all()#.order_by('-time')[:10]
    if not ecgDatas:
        raise Http404("Aw! It's an error.")
    else:
        ecgFiltered = ecgDatas.filter(patientID = patient)
        currentSamples = floor(ecgFiltered.count() / sampleRate)
        if ecgFiltered.count() < sampleRate:
            currentSamples = 1
        #json_serializer = serializers.get_serializer("json")()
        print(currentSamples, ecgFiltered.count())
        #ecg = json_serializer.serialize(ecgFiltered.order_by('time')[ : ecgFiltered.count()], ensure_ascii=False)
        
        context = {
            #'ecgDatas': ecgDatas[(samples - 1) * sampleRate : samples * sampleRate],
            #'ecgDatas': ecgDatas[3500 : 3750],
            'ECG': ecgFiltered.order_by('-time')[0 : ecgFiltered.count()],
            'pID': pID,
            'patient': patient,
            'patients': patients,
            'sampleRate': sampleRate,
            'samples': samples
        }
        return render(request, 'Monitor/completeTable.html', context)

#Data Entry and Delete by POST Request Handling
@login_required(login_url='/Monitor/logIn')
def deleteOldData():
    count = ECGData.objects.count()
    #print(count)
    if count not in range (0, total):
        #toDelete = ECGData.objects.all()[0 : sampleRate]
        #toDelete.delete()
        ECGData.objects.filter(id__in=list(ECGData.objects.values_list('pk', flat=True)[:sampleRate])).delete()
        count = ECGData.objects.count()
        #print(count)
        deleteOldData()
    print(ECGData.objects.count())
    return

@login_required(login_url='/Monitor/logIn')
def RPIPush(request):
    #return StreamingHttpResponse('RPI POST Request Successful!')
    if request.method=='POST':
            deleteOldData()
            patients = PatientData.objects.all()
            sensors = SensorData.objects.all()
            #received_json_data=json.loads(request.POST['data'])
            received = json.loads(request.body)
            #print(received['ECGData'][0]['sensorID'], received['ECGData'][1])
            for i in sensors:
                if i.sensorID == received['ECGData'][0]['sensorID']:
                    sensor = i
            for i in patients:
                if i.patientID == received['ECGData'][0]['patientID']:
                    patient = i
            j = 0
            for row in received['ECGData']:
                #print(received['ECGData'][j])
                ECGData.objects.create(sensorID = sensor, patientID = patient, time = row['time'], data = row['data'])
                j += 1
            
            j = 0
            return StreamingHttpResponse('RPI POST Request Successful!: ')# + str(received))
    return StreamingHttpResponse('Error: GET Request')

#user Authentication & LogIn
class logInForm(View):
    form_class = logInForm
    template = 'Monitor/logInForm.html'
    print('hi from logIn: class')
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template, {'form': form})
    def post(self, request):
        print('hi from logIn: POST')
        print(request.POST)
        form = self.form_class(request.POST)
        #print(form)
        """
        if form.is_valid():
            print('form is valid')
            user = form.save(commit=False)
            #cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #username = form.get('username', False)#['username']
            password = form.get('password', False)#['password']
            user.set_password(password)
            user.save()
            print('user: ' + user)
        """
        username = request.POST['username']
        password = request.POST['password']
        print('username: ' + username)# + 'password: ' + password)
        #authentication
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('Index')
        return render(request, self.template, {'form': form})

def logOut(request):
    logout(request)
    # Redirect to a success page.
    return redirect('/Monitor/logIn')