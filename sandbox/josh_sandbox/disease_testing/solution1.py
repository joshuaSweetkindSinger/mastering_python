"""
This file defines prototype code for multi-dispatch in the context of testing
a patient for multiple diseases.

The solution employed in this file takes advantage of special knowledge that
categorization methods are all named _categorize_<category_name>, e.g., _categorize_age(),
and dynamically builds up the method to call as a string.
"""
class Patient:
    def __init__(self, age, systolic_blood_pressure):
        self.age = age
        self.systolic_blood_pressure = systolic_blood_pressure


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


class HeartAttackStageA(DiseaseStageBase):
    def _categorize_age(self, patient):
        return 0 if patient.age < 50 else 1

    def _categorize_blood_pressure(self, patient):
        return 0 if patient.systolic_blood_pressure < 120 else 1


class DiabetesStageA(DiseaseStageBase):
    def _categorize_age(self, patient):
        return 0 if patient.age < 30 else 1

    def _categorize_blood_pressure(self, patient):
        return 0 if patient.systolic_blood_pressure < 150 else 1


def test():
    patient = Patient(age = 40, systolic_blood_pressure = 130)
    heart_attack_stage_a = HeartAttackStageA()
    diabetes_stage_a = DiabetesStageA()

    # Here we run the tests. All the disease-stage objects are sent a categorize() message.
    print("heart attack, age ->",            heart_attack_stage_a.categorize('age', patient))
    print("diabetes, age ->",                diabetes_stage_a.categorize('age', patient))
    print("heart attack, blood pressure ->", heart_attack_stage_a.categorize('blood_pressure', patient))
    print("diabetes, blood pressure ->",     diabetes_stage_a.categorize('blood_pressure', patient))


if __name__ == '__main__':
    test()