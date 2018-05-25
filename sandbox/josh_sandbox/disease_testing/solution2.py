"""
This file defines prototype code for multi-dispatch in the context of testing
a patient for multiple diseases.

This solution essentially implements the previous solution1, except that it takes control
of handling the naming convention for categorization methods, hiding that "under the hood"
of a decorator function.

Categorization methods are still methods that follow a special naming convention. In this
case, a categorization method for risk factor 'age' has the name _categorize_age().
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
    @staticmethod
    def get_categorization_method_name(risk_factor):
        return '_categorize_' + risk_factor


    def get_categorizer(self, risk_factor):
        """
        Return the method that categorizes the risk factor named risk_factor for ourselves.
        :param risk_factor: A risk factor name, e.g. 'age', 'blood_pressure'
        :return: the method that should be used for categorization.
        """
        return getattr(self, self.get_categorization_method_name(risk_factor))


    @classmethod
    def set_categorizer(cls, risk_factor, f):
        """
        Set the function f to be the categorization method for class cls for the risk factor
        named risk_factor

        We do this by dynamically creating a method on cls with an algorithmically defined name
        and assigning f to be that method.

        :param cls: The class to which f should be added as a categorization method
        :param risk_factor: The name of the risk factor, e.g. 'age', 'blood_pressure'
        :param f: The function to be added.
        :return: cls
        """
        # Create an empty risk factors set for this class if the risk factors set does not yet exist
        if not hasattr(cls, 'risk_factors'):
            cls.risk_factors = set()

        cls.risk_factors.add(risk_factor)
        setattr(cls, cls.get_categorization_method_name(risk_factor), f)
        return cls


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
# =============================================================================
#                     Decorator
# =============================================================================
# This is the magic. See use cases below.
def categorizer(cls, risk_factor):
    """
    This is a special-purpose decorator generator for subclasses of DiseaseStageBase.
    Declare the decorated function to be a categorization method for the specified class and risk factor.
    :param cls: The class to which the function should be added as a categorization method
    :param risk_factor: the name of the risk factor to which this method applies.
    :return: a dynamically generated decorator that adds f to the set of categorization methods.
             It doesn't wrap the decorated function but simply returns None.
             The name given to the original function will still be in the namespace, but its value will be None; it
             will not be a valid executable function.
    """
    def decorator(f):
        """
        This is a dynamically generated decorator function.
        :param f: The function to be decorated. In this case, it is a categorization method.
        :return: None, but, as a side effect, add f to the set of categorization methods.
        """
        cls.set_categorizer(risk_factor, f) # Add f as the categorizer for (cls, risk_factor)
        return None # Render useless the symbol to which the original function definition f was bound.

    return decorator

# =============================================================================
#                     Stroke Stage A
# =============================================================================
# The instantiable disease-stage classes get defined *without* their categorizer methods.
# Those are added afterwards via the decorator. Since this demo only illustrates the categorizer
# method definitions, these particular disease-stage classes have empty definitions in this implementation.
# In real-life, they would not be empty, because they would define other methods that are not categorizers.

class StrokeStageA(DiseaseStageBase):
    pass

@categorizer(StrokeStageA, 'age')
def _(self, patient):
    return 0 if patient.age < 50 else 1

@categorizer(StrokeStageA, 'blood_pressure')
def _(self, patient):
    return 0 if patient.systolic_blood_pressure < 120 else 1

@categorizer(StrokeStageA, 'cholesterol')
def _(self, patient):
    return 0 if patient.cholesterol < 200 else 1


# =============================================================================
#                     Diabetes Stage A
# =============================================================================
class DiabetesStageA(DiseaseStageBase):
    pass

@categorizer(DiabetesStageA, 'fasting_blood_sugar')
def _(self, patient):
    return 0 if patient.fasting_blood_sugar < 100 else 1

@categorizer(DiabetesStageA, 'blood_pressure')
def _(self, patient):
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