"""
This file defines prototype code for multi-dispatch in the context of testing
a patient for multiple diseases.

The solution employed in this file takes advantage of special knowledge that
categorization methods are all named _categorize_<risk_factor>, e.g., _categorize_age(),
and dynamically builds up the method to call as a string.
"""
from sandbox.josh_sandbox.disease_testing.common import test

class DiseaseStageBase:
    risk_factors = set()  # Empty set of risk factors for base class

    @classmethod
    def get_categorization_method_name(cls, risk_factor):
        return '_categorize_' + risk_factor

    def get_categorizer(self, risk_factor):
        """
        Return the method that categorizes the risk factor named risk_factor for ourselves.
        :param risk_factor: A risk factor, e.g. 'age', 'blood_pressure'
        :return: the method that should be used for categorization.
        """
        return getattr(self, self.get_categorization_method_name(risk_factor))

    # This method is not needed by the implementation, but I add it for completeness.
    def categorize(self, risk_factor, patient):
        return self.get_categorizer(risk_factor)(patient)

    @property
    def categorizers(self):
        """
        Return an iterator over the (risk_factor, categorizer) pairs we define.
        :return:
        """
        for risk_factor in self.risk_factors:
            yield risk_factor, self.get_categorizer(risk_factor)


class StrokeStageA(DiseaseStageBase):
    risk_factors = {'age', 'blood_pressure', 'cholesterol'}

    def _categorize_age(self, patient):
        return 0 if patient.age < 50 else 1

    def _categorize_blood_pressure(self, patient):
        return 0 if patient.systolic_blood_pressure < 120 else 1

    def _categorize_cholesterol(self, patient):
        return 0 if patient.cholesterol < 200 else 1


class IschemicStrokeStageA(StrokeStageA):
    risk_factors = {'age', 'blood_pressure', 'cholesterol', 'blood_viscosity'}

    def _categorize_blood_viscosity(self, patient):
        return 0 if patient.blood_viscosity < 2.7 else 1


class HemorrhagicStrokeStageA(StrokeStageA):
    risk_factors = {'age', 'blood_pressure', 'cholesterol'}

    def _categorize_blood_pressure(self, patient):
        return 0 if patient.systolic_blood_pressure < 170 else 1


class DiabetesStageA(DiseaseStageBase):
    risk_factors = {'fasting_blood_sugar', 'blood_pressure'}

    def _categorize_fasting_blood_sugar(self, patient):
        return 0 if patient.fasting_blood_sugar < 100 else 1

    def _categorize_blood_pressure(self, patient):
        return 0 if patient.systolic_blood_pressure < 150 else 1



if __name__ == '__main__':
    test([StrokeStageA(), IschemicStrokeStageA(), HemorrhagicStrokeStageA(), DiabetesStageA()])