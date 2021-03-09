from django.shortcuts import render

# Create your views here.
def index(request):
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
    template = loader.get_template('monitor/index.html')
    return HttpResponse(template.render(context, request))
    """
    return render(request, 'monitor/index.html', context)

