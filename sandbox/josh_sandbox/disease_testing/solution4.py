"""
This file defines prototype code for multi-dispatch in the context of testing
a patient for multiple diseases.

This solution is an enhancement of Solution 3. It supplies a decorator that automatically
marks the methods that are categorizers, which methods can be given any name at all.

The core code also ensures that all categorizer methods are automatically installed on
the categorizer_dict of the disease-stage object that defines them, so that client
code does not have to explicitly do this. Further, it guarantees that subclassing a disease-stage
class works correctly. If IschemicStrokeStageA is a subclass of StrokeStageA, then it automatically
inherits and installs all of the categorizers of its class parent.
"""
# =============================================================================
#                     Base Classes
# =============================================================================
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

# =============================================================================
#                     Categorizer Helper Functions
# =============================================================================
# A categorizer is a function defined within a class (unbound method) that has
# been decoratored with the @categorizer decorator. Implementation-wise, this means
# the decorator has installed a _risk_factor attribute on the function object.
#    The functions below are helper functions to deal with categorizers.

def is_categorizer(f):
    return callable(f) and hasattr(f, '_risk_factor')

def categorizer_risk_factor(f):
    return f._risk_factor

def categorizer_set_risk_factor(f, risk_factor):
    f._risk_factor = risk_factor

def categorizer_bound_method(f, disease_stage):
    """
    :return: the bound-method of disease_stage represented by f.
    :param disease_stage: an instance descendant of DiseaseStageBase

    NOTES: f is just a function. The associated bound method
    "binds" its self arg, which is a disease-stage instance, so that it only
    needs to receive the remaining non-self arguments. Python will find the bound method
    for us using the inheritance mechanism. We just need to ask it to get the method
    of disease_stage we desire, by supplying its name.
    """
    return getattr(disease_stage, f.__name__)

# =============================================================================
#                     Class DiseaseStageBase
# =============================================================================

class DiseaseStageBase:
    def __init__(self):
        self._categorizer_dict = {} # Maps risk factor names to bound methods
        self._install_categorizers()


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
        Return an iterator over the installed (risk_factor, method) categorizers we defined.
        :return:
        """
        for risk_factor, method in self._categorizer_dict.items():
            yield risk_factor, method


    def _install_categorizers(self):
        """
        Install onto ourselves all methods that have been decorated as categorizers.
        :return: self
        """
        for risk_factor, bound_method in self._get_defined_categorizers():
            self._install_categorizer(risk_factor, bound_method)


    def _get_defined_categorizers(self):
        """
        Return an iterable over all (risk_factor, bound_method) categorizers defined on self.

        This is called as part of the installation process. This method finds the categorizers that
        have been defined, prior to their being installed on our _categorizer_dict.
        """
        # Loop through all our attributes, checking for those that are categorizer methods.
        # If we find a categorizer, yield its (risk_factor, bound_method) pair.
        for attribute_name in dir(self):
            f = getattr(self, attribute_name) # Note that f might not be a function. It could be a plain value.
            if is_categorizer(f):
                yield categorizer_risk_factor(f), categorizer_bound_method(f, self)


    def _install_categorizer(self, risk_factor, bound_method):
        """
        Install bound_method as a categorizer for risk_factor on self.

        Doing so means that self.categorize(risk_factor, patient) will work.

        Further, looping through all categorizers via the iterable self.categorizers
        will yield (risk_factor, bound_method) as one of its return values.

        :param risk_factor: a string, the name of a risk fator
        :param bound_method: a bound method of self that functions as a categorization method.
        :return: self
        """
        self._categorizer_dict[risk_factor] = bound_method
        return self


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
        :param f:
        :return: f, with the risk factor added to it as an attribute.
        """
        categorizer_set_risk_factor(f, risk_factor)
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


def test():
    patient = Patient(age = 40,
                      systolic_blood_pressure = 130,
                      blood_viscosity = 2.8,
                      fasting_blood_sugar = 90,
                      cholesterol = 210)
    disease_stages = [StrokeStageA(), IschemicStrokeStageA(), HemorrhagicStrokeStageA(), DiabetesStageA()]

    for disease_stage in disease_stages:
        print()
        for risk_factor, method in disease_stage.categorizers:
            category = method(patient)
            print("{disease_stage}, {risk_factor} -> {category}".format(disease_stage = disease_stage.__class__.__name__,
                                                                        risk_factor = risk_factor,
                                                                        category = category))

if __name__ == '__main__':
    test()