from django.shortcuts import render
from .models import HospitalData
from django.http import HttpResponse

# Create your views here.
def Index(request):
    hospitals = HospitalData.objects.all()
    """
    Index = '<h1>Welcome to ECG-Monitoring System</h1>'
    for hospital in hospitals:
        url = '/monitor/' + str(hospital.hospitalID) + '/'
        Index += '<a href =" ' + url + '">' + hospital.hospitalName + '</a><br>'
    return HttpResponse(Index)
    """
    context = {
        'hospitals': hospitals,
    }
    """
    template = loader.get_template('Monitor/index.html')
    return HttpResponse(template.render(context, request))
    """
    return render(request, 'Monitor/Index.html', context)

# Data Entry
def hospitalDataEntry(request):
    hospitalInstance = HospitalData.objects.create(hospitalID = "HTZ12", hospitalName = "Max Hospital", hospitalAddress = "Main Town, Tezpur, Assam-784028")
    p = HospitalData(hospitalID = "HTZ10", hospitalName = "GNRC Hospital", hospitalAddress = "Main Town, Tezpur, Assam-784028")
    p.save()
    return HttpResponse("<h1>Hospital Data inserted successfully!</h1>")
