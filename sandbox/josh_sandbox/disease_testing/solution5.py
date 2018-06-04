"""
This file defines prototype code for multi-dispatch in the context of testing
a patient for multiple diseases.

This solution is an enhancement of Solution 4.
It implements categorizor dispatch at the class level, rather than duplicating the categorizer dispatch
dictionary for each instance of the same class.

The core code ensures that all categorizer methods are automatically installed on
the categorizer_dict of the disease-stage class that defines them, so that client
code does not have to explicitly do this. Further, it guarantees that subclassing a disease-stage
class works correctly. If IschemicStrokeStageA is a subclass of StrokeStageA, then it automatically
inherits and installs all of the categorizers of its class parent.
"""
from sandbox.josh_sandbox.disease_testing.common import test


# =============================================================================
#                     Class DiseaseStageBase
# =============================================================================

class DiseaseStageBase:
    _categorizer_dict = {}

    def __init_subclass__(cls, **kwargs):
        """
        Install onto ourselves all method names that have been decorated as categorizers.
        :return: self
        """
        cls._categorizer_dict = cls._categorizer_dict.copy() # Copy the dict from our parent.

        for risk_factor, method_name in cls._get_defined_categorizers():
            cls._categorizer_dict[risk_factor] = method_name


    # This method is not needed by the implementation, but I add it for completeness.
    def get_categorizer(self, risk_factor):
        """
        Return the bound method that categorizes the risk factor named risk_factor for ourselves.
        :param risk_factor: A risk factor, e.g. 'age', 'blood_pressure'
        :return: the bound method that should be used for categorization.
        """
        return getattr(self, self._categorizer_dict[risk_factor])


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
        Return an iterator over the installed (risk_factor, bound_method) categorizers we defined.
        :return:
        """
        for risk_factor, method_name in self._categorizer_dict.items():
            yield risk_factor, getattr(self, method_name)


    @classmethod
    def _get_defined_categorizers(cls):
        """
        Return an iterable over all (risk_factor, method_name) categorizers defined on cls.

        This is called as part of the installation process. This method finds the categorizers that
        have been defined, prior to their being installed on our _categorizer_dict.
        """
        # Loop through all our attributes, checking for those that are categorizer methods.
        # If we find a categorizer, yield its (risk_factor, method_name) pair.
        for attribute_name in dir(cls):
            f = getattr(cls, attribute_name) # Note that this might not be a function. It could be a plain value if
                                             # attribute_name is not the name of a method.
            if cls._is_categorizer(f):
                yield cls._get_risk_factor_for_categorizer(f), attribute_name


    @staticmethod
    def _is_categorizer(f):
        return callable(f) and hasattr(f, '_risk_factor')

    @staticmethod
    def _get_risk_factor_for_categorizer(f):
        return f._risk_factor

    @staticmethod
    def set_risk_factor_for_categorizer(f, risk_factor):
        f._risk_factor = risk_factor


# =============================================================================
#                     Decorator
# =============================================================================
def categorizer(risk_factor):
    """
    This is a decorator generator.
    :param risk_factor: The risk factor for which the method we are decorating is being defined.
    :return: a dynamically generated decorator
    """
    def decorator(f):
        """
        Set the risk factor for f so that we can determine later that f is actually
        a categorizer. This decorator does not actually wrap f or alter its behavior.
        It just flags it as a categorizer.
        :param f: a function (not a bound method, since this is being evaluated at class-definition time)
        :return: f, with the risk factor added to it as an attribute.
        """
        DiseaseStageBase.set_risk_factor_for_categorizer(f, risk_factor)
        return f

    return decorator

# =============================================================================
#                     Stroke Stage A
# =============================================================================
class StrokeStageA(DiseaseStageBase):
    @categorizer('age')
    def _categorize_age(self, patient):
        return 0 if patient.age < 50 else 1

    @categorizer('blood_pressure')
    def _cat_blood_pressure(self, patient):
        return 0 if patient.systolic_blood_pressure < 120 else 1

    @categorizer('cholesterol')
    def _ctg_cholesterol(self, patient):
        return 0 if patient.cholesterol < 200 else 1


class IschemicStrokeStageA(StrokeStageA):
    @categorizer('blood_viscosity')
    def _cat_blood_viscosity(self, patient):
        return 0 if patient.blood_viscosity < 2.7 else 1


class HemorrhagicStrokeStageA(StrokeStageA):
    @categorizer('blood_pressure')
    def _ctg_blood_pressure(self, patient):
        return 0 if patient.systolic_blood_pressure < 170 else 1

# =============================================================================
#                     Diabetes Stage A
# =============================================================================
class DiabetesStageA(DiseaseStageBase):
    @categorizer('blood_sugar')
    def _categorize_patient_blood_sugar(self, patient):
        return 0 if patient.fasting_blood_sugar < 100 else 1

    @categorizer('blood_pressure')
    def _categorize_bp(self, patient):
        return 0 if patient.systolic_blood_pressure < 150 else 1


# =============================================================================
#                     Test
# =============================================================================


if __name__ == '__main__':
    test([StrokeStageA(), IschemicStrokeStageA(), HemorrhagicStrokeStageA(), DiabetesStageA()])