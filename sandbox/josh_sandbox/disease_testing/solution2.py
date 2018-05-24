"""
This file defines prototype code for multi-dispatch in the context of testing
a patient for multiple diseases.

This solution essentially implements the previous solution1, except that it takes control
of handling the naming convention for categorization methods, hiding that "under the hood"
of a decorator function.

Categorization methods are still methods that follow a special naming convention. In this
case, a categorization method for category name 'age' has the name _categorize_age(patient).
"""
# =============================================================================
#                     Base Classes
# =============================================================================
class Patient:
    def __init__(self, age, systolic_blood_pressure):
        self.age = age
        self.systolic_blood_pressure = systolic_blood_pressure


class DiseaseStageBase:
    @classmethod
    def set_categorizer(cls, category_name, f):
        """
        Set the function f to be the categorization method for class cls for the category named category_name.

        We do this by dynamically creating a method on cls with an algorithmically defined name
        and assigning f to be that method.

        :param cls: The class to which f should be added as a categorization method
        :param category_name: The name of the category, e.g. 'age', 'blood_pressure'
        :param f: The function to be added.
        :return: cls
        """
        setattr(cls, cls.get_categorization_method_name(category_name), f)
        return cls


    @staticmethod
    def get_categorization_method_name(category_name):
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

# =============================================================================
#                     Decorator
# =============================================================================
# This is the magic. See use cases below.
def categorizer(cls, category_name):
    """
    This is a special-purpose decorator generator for subclasses of DiseaseStageBase.
    Declare the decorated function to be a categorization method for the specified class and category name.
    :param cls: The class to which the function should be added as a categorization method
    :param category_name: the name of the category to which this method applies.
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
        cls.set_categorizer(category_name, f) # Add f as the categorizer for (cls, category_name)
        return None # Render useless the symbol to which the original function definition f was bound.

    return decorator

# =============================================================================
#                     Heart Attack Stage A
# =============================================================================
# For the purposes of this demo, we initially define the disease-stage class as empty,
# because it receives its functionality through the use of the @categorizer decorator.
class HeartAttackStageA(DiseaseStageBase):
    pass

@categorizer(HeartAttackStageA, 'age')
def _(self, patient):
    return 0 if patient.age < 50 else 1

@categorizer(HeartAttackStageA, 'blood_pressure')
def _(self, patient):
    return 0 if patient.systolic_blood_pressure < 120 else 1



# =============================================================================
#                     Diabetes Stage A
# =============================================================================
class DiabetesStageA(DiseaseStageBase):
    pass


@categorizer(DiabetesStageA, 'age')
def categorize_age(self, patient):
    return 0 if patient.age < 30 else 1

@categorizer(DiabetesStageA, 'blood_pressure')
def categorize_blood_pressure(self, patient):
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