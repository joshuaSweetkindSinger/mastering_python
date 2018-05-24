"""
This file defines prototype code for multi-dispatch in the context of testing
a patient for multiple diseases.

This solution caches the categorization methods in a dict. They can have any names and
need not follow a naming convention. However, the downside is that each new categorization
method must be hand-added to the categorization method dictionary.
"""
# =============================================================================
#                     Base Classes
# =============================================================================
class Patient:
    def __init__(self, age, systolic_blood_pressure):
        self.age = age
        self.systolic_blood_pressure = systolic_blood_pressure


class DiseaseStageBase:
    def __init__(self):
        self._categorizer_dict = {} # Map category names to bound methods


    def set_categorizer(self, category_name, m):
        """
        Set the bound method m to be the categorization method
        for the category named category_name.
        :param category_name: The name of the category, e.g. 'age', 'blood_pressure'
        :param m: The method to be added.
        :return: m
        """
        self._categorizer_dict[category_name] = m
        return m


    def get_categorizer(self, category_name):
        """
        Return the method that categorizes the category named category_name for ourselves.
        :param category_name: A category name, e.g. 'age', 'blood_pressure'
        :return: the method that should be used for categorization.
        """
        return self._categorizer_dict[category_name]


    # This is the generic method that will handle categorization
    # for all subclasses.
    def categorize(self, category_name, patient):
        return self.get_categorizer(category_name)(patient)


# =============================================================================
#                     Heart Attack Stage A
# =============================================================================
class HeartAttackStageA(DiseaseStageBase):
    def __init__(self):
        super().__init__()

        # All categorizers need to be initialized here.
        # If a new one is ever added, then it needs to be added here too.
        self.set_categorizer('age', self._categorize_age)
        self.set_categorizer('blood_pressure', self._cat_blood_pressure)

    def _categorize_age(self, patient):
        return 0 if patient.age < 50 else 1

    def _cat_blood_pressure(self, patient):
        return 0 if patient.systolic_blood_pressure < 120 else 1



# =============================================================================
#                     Diabetes Stage A
# =============================================================================
class DiabetesStageA(DiseaseStageBase):
    def __init__(self):
        super().__init__()

        # All categorizers need to be initialized here.
        # If a new one is ever added, then it needs to be added here too.
        self.set_categorizer('age', self._categorize_patient_age)
        self.set_categorizer('blood_pressure', self._categorize_bp)

    def _categorize_patient_age(self, patient):
        return 0 if patient.age < 30 else 1

    def _categorize_bp(self, patient):
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