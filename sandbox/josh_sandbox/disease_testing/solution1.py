"""
This file defines prototype code for multi-dispatch in the context of testing
a patient for multiple diseases.

The solution employed in this file takes advantage of special knowledge that
categorization methods are all named _categorize_<category_name>, e.g., _categorize_age(),
and dynamically builds up the method to call as a string.
"""
class Patient:
    def __init__(self,
                 age,
                 systolic_blood_pressure,
                 fasting_blood_sugar,
                 cholesterol
                 ):
        self.age = age
        self.systolic_blood_pressure = systolic_blood_pressure
        self.fasting_blood_sugar = fasting_blood_sugar
        self.cholesterol = cholesterol


class DiseaseStageBase:
    @classmethod
    def get_categorization_method_name(cls, category_name):
        return '_categorize_' + category_name

    def get_categorizer(self, category_name):
        """
        Return the method that categorizes the category named category_name for ourselves.
        :param category_name: A category name, e.g. 'age', 'blood_pressure'
        :return: the method that should be used for categorization.
        """
        return getattr(self, self.get_categorization_method_name(category_name))

    # This is the generic method that will handle categorization
    # for all subclasses.
    def categorize(self, category_name, patient):
        return self.get_categorizer(category_name)(patient)


class StrokeStageA(DiseaseStageBase):
    risk_factors = {'age', 'blood_pressure', 'cholesterol'}

    def _categorize_age(self, patient):
        return 0 if patient.age < 50 else 1

    def _categorize_blood_pressure(self, patient):
        return 0 if patient.systolic_blood_pressure < 120 else 1

    def _categorize_cholesterol(self, patient):
        return 0 if patient.cholesterol < 200 else 1


class DiabetesStageA(DiseaseStageBase):
    risk_factors = {'fasting_blood_sugar', 'blood_pressure'}

    def _categorize_fasting_blood_sugar(self, patient):
        return 0 if patient.fasting_blood_sugar < 100 else 1

    def _categorize_blood_pressure(self, patient):
        return 0 if patient.systolic_blood_pressure < 150 else 1


def test():
    patient = Patient(age = 40,
                      systolic_blood_pressure = 130,
                      fasting_blood_sugar = 90,
                      cholesterol = 210)
    disease_stages = [StrokeStageA(), DiabetesStageA()]

    for disease_stage in disease_stages:
        print()
        for risk_factor in disease_stage.risk_factors:
            category = disease_stage.categorize(risk_factor, patient)
            print("{disease_stage}, {risk_factor} -> {category}".format(disease_stage = disease_stage.__class__.__name__,
                                                                        risk_factor = risk_factor,
                                                                        category = category))

if __name__ == '__main__':
    test()