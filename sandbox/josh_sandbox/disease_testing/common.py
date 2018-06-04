"""
This file defines the class Patient.
"""
class Patient:
    def __init__(self,
                 age,
                 systolic_blood_pressure,
                 fasting_blood_sugar,
                 cholesterol,
                 blood_viscosity
                 ):
        self.age = age
        self.systolic_blood_pressure = systolic_blood_pressure
        self.fasting_blood_sugar = fasting_blood_sugar
        self.cholesterol = cholesterol
        self.blood_viscosity = blood_viscosity


def test(disease_stages):
    patient = Patient(age = 40,
                      systolic_blood_pressure = 130,
                      blood_viscosity = 2.8,
                      fasting_blood_sugar = 90,
                      cholesterol = 210)

    for disease_stage in disease_stages:
        print()
        for risk_factor, method in disease_stage.categorizers:
            category = method(patient)
            print("{disease_stage}, {risk_factor} -> {category}".format(disease_stage = disease_stage.__class__.__name__,
                                                                        risk_factor = risk_factor,
                                                                        category = category))