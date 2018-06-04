"""
This file defines prototype code for multi-dispatch in the context of testing
a patient for multiple diseases.

This solution caches the categorization methods in a dict. They can have any names and
need not follow a naming convention. However, the downside is that each new categorization
method must be hand-added to the categorization method dictionary.
"""
from sandbox.josh_sandbox.disease_testing.common import test


class DiseaseStageBase:
    def __init__(self):
        self._categorizer_dict = {} # Map risk factor names to bound methods


    def set_categorizer(self, risk_factor, m):
        """
        Set the bound method m to be the categorization method
        for the risk factor named risk_factor.
        :param risk_factor: The name of the risk factor, e.g. 'age', 'blood_pressure'
        :param m: The method to be added.
        :return: m
        """
        self._categorizer_dict[risk_factor] = m
        return m

    # This method is not needed by the implementation, but I add it for completeness.
    def get_categorizer(self, risk_factor):
        """
        Return the method that categorizes the risk factor named risk_factor for ourselves.
        :param risk_factor: A risk factor, e.g. 'age', 'blood_pressure'
        :return: the method that should be used for categorization.
        """
        return self._categorizer_dict[risk_factor]

    # This method is not needed by the implementation, but I add it for completeness.
    def categorize(self, risk_factor, patient):
        return self.get_categorizer(risk_factor)(patient)

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
#                     Stroke Stage A
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


class IschemicStrokeStageA(StrokeStageA):
    def __init__(self):
        super().__init__()

        self.set_categorizer('blood_viscosity', self._cat_blood_viscosity)


    def _cat_blood_viscosity(self, patient):
        return 0 if patient.blood_viscosity < 2.7 else 1


class HemorrhagicStrokeStageA(StrokeStageA):
    def _ctg_blood_pressure(self, patient):
        return 0 if patient.systolic_blood_pressure < 170 else 1


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


if __name__ == '__main__':
    test([StrokeStageA(), IschemicStrokeStageA(), HemorrhagicStrokeStageA(), DiabetesStageA()])