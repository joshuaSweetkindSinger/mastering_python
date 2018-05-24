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

    # This method is not needed by the implementation, but I add it for completeness.
    def get_categorizer(self, category_name):
        """
        Return the method that categorizes the category named category_name for ourselves.
        :param category_name: A category name, e.g. 'age', 'blood_pressure'
        :return: the method that should be used for categorization.
        """
        return self._categorizer_dict[category_name]

    # This method is not needed by the implementation, but I add it for completeness.
    def categorize(self, category_name, patient):
        return self.get_categorizer(category_name)(patient)

    # This method is not needed by the implementation, but I add it for completeness.
    @property
    def risk_factors(self):
        return self._categorizer_dict.keys()

    @property
    def categorizers(self):
        """
        Return an iterator over the (risk_factor, categorizer) pairs we define.
        :return:
        """
        for risk_factor, method in self._categorizer_dict.items():
            yield risk_factor, method


# =============================================================================
#                     Heart Attack Stage A
# =============================================================================
class StrokeStageA(DiseaseStageBase):
    def __init__(self):
        super().__init__()

        # All categorizers need to be initialized here.
        # If a new one is ever added, then it needs to be added here too.
        self.set_categorizer('age', self._categorize_age)
        self.set_categorizer('blood_pressure', self._cat_blood_pressure)
        self.set_categorizer('cholesterol', self._ctg_cholesterol)

    def _categorize_age(self, patient):
        return 0 if patient.age < 50 else 1

    def _cat_blood_pressure(self, patient):
        return 0 if patient.systolic_blood_pressure < 120 else 1

    def _ctg_cholesterol(self, patient):
        return 0 if patient.cholesterol < 200 else 1

# =============================================================================
#                     Diabetes Stage A
# =============================================================================
class DiabetesStageA(DiseaseStageBase):
    def __init__(self):
        super().__init__()

        # All categorizers need to be initialized here.
        # If a new one is ever added, then it needs to be added here too.
        self.set_categorizer('fasting_blood_sugar', self._categorize_patient_blood_sugar)
        self.set_categorizer('blood_pressure', self._categorize_bp)

    def _categorize_patient_blood_sugar(self, patient):
        return 0 if patient.fasting_blood_sugar < 100 else 1

    def _categorize_bp(self, patient):
        return 0 if patient.systolic_blood_pressure < 150 else 1


def test():
    patient = Patient(age = 40,
                      systolic_blood_pressure = 130,
                      fasting_blood_sugar = 90,
                      cholesterol = 210)
    disease_stages = [StrokeStageA(), DiabetesStageA()]

    for disease_stage in disease_stages:
        print()
        for risk_factor, categorizer in disease_stage.categorizers:
            category = categorizer(patient)
            print("{disease_stage}, {risk_factor} -> {category}".format(disease_stage = disease_stage.__class__.__name__,
                                                                        risk_factor = risk_factor,
                                                                        category = category))

if __name__ == '__main__':
    test()