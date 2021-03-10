from django.db import models

# Create your models here.

class HospitalData(models.Model):
    hospitalID = models.TextField(max_length=15, primary_key=True)
    hospitalName = models.TextField(max_length=30)
    hospitalAddress =  models.TextField(max_length=50)

    def __str__(self):
        return self.hospitalID + ' ' + self.hospitalName + ' ' + self.hospitalAddress

class PatientData(models.Model):
    patientID = models.TextField(max_length=15, primary_key=True)
    patientName = models.TextField(max_length=30)
    hospitalID =  models.ForeignKey(HospitalData, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.patientID + ' ' + self.patientName + ' ' + self.hospitalID.hospitalID

class SensorData(models.Model):
    sensorID = models.TextField(max_length=15, primary_key=True)
    sensorName = models.TextField(max_length=15)

    def __str__(self):
        return self.sensorID + ' ' + self.sensorName

class ECGData(models.Model):
    sensorID = models.ForeignKey(SensorData, on_delete=models.CASCADE)
    patientID = models.ForeignKey(PatientData, on_delete=models.CASCADE)
    time = models.DateTimeField()
    data = models.FloatField()

    def __str__(self):
        return self.sensorID.sensorID + ' ' + self.patientID.patientID + ' ' + str(self.time) + ' ' + str(self.data)