"""
This file contains examples that illustrate the difference between regular methods, class methods, and static methods in python.
"""
import math
class BasicPizza(object):
    """
    Represents a pricing structure for a basic pizza, which is circular. Knows its size (diameter) and how much to charge depending
    on its size and on the delivery method. Toplevel method is cost()
    """
    # This specifies additional costs to be charged depending on how the pizza is delivered.
    COST_PER_SQUARE_INCH = .10
    DELIVERY_COSTS = dict(for_here = 10,
                          pick_up_to_go = 0,
                          deliver_to_house = 20)

    def __init__(self, diameter):
        """
        :param diameter: Specifies the size of the pizza.
        """
        self.diameter = diameter


    # This method requires knowing the diameter of the pizza instance (through the area property). Therefore it needs to
    # be a regular instance method.
    def cost(self, delivery_method):
        """
        :return: the our cost, taking into account the delivery method.
        :param delivery_method: One of 'for_here', 'pick_up_to_go', 'deliver_to_house'.
        """
        print("Calling method cost() from class BasicPizza") # debugging

        return self.area * self.COST_PER_SQUARE_INCH + self.delivery_cost(delivery_method)


    @property
    def area(self):
        """
        Return our area
        """
        return self.calc_area(self.diameter)


    # This method doesn't need to consult any instance member variables. It only needs to consult the class constant DELIVERY_COSTS.
    # Because of that, it can be declared a @classmethod.
    @classmethod
    def delivery_cost(cls, delivery_method):
        """
        :param delivery_method:
        :return: our delivery cost as a function of the delivery method.
        """
        print("Calling classmethod delivery_cost() from class BasicPizza") # debugging

        return cls.DELIVERY_COSTS[delivery_method]


    # This is just a helper function to calculate the area of a circle, because cheese pizzas are circular. It doesn't depend on
    # any class member variables or instance member variables, so it can be declared static. Nonetheless, it is *inherited* to
    # all subclasses.
    @staticmethod
    def calc_area(diameter):
        """
        :param diameter:
        :return: the area of a circle of the specified radius
        """
        print("Calling static method calc_area() from class BasicPizza") # debugging

        return math.pi * (diameter / 2) ** 2



class SquarePizza(BasicPizza):
    """
    Square pizzas are square, not circular. Otherwise, they are the same as basic pizzas.
    """

    # Because square pizzas are square, not circular, we need to override the calc_area() method. It's still static;
    # nonetheless, our child class PepperoniPizza will inherit this override.
    @staticmethod
    def calc_area(diameter):
        """
        :param diameter: The diameter of the (square) pizza.
        :return: the area of a square of the specified diameter
        """
        print("Calling static method calc_area() from class SquarePizza") # debugging

        return diameter**2 / 2



class PepperoniPizza(SquarePizza):
    """
    Pepperoni pizzas are square and have pepperoni on them. Because they are the number one seller, we
    give a discount on delivery for them, regardless of delivery method.
    But their base cost per square inch is higher, because of the pepperoni.
    """
    COST_PER_SQUARE_INCH = .15
    DELIVERY_DISCOUNT    = 3    # Give a flat $3 discount on delivery, regardless of method.

    # Because the delivery cost is different for pepperoni pizzas, we override it here.
    @classmethod
    def delivery_cost(cls, delivery_method):
        """
        We give a flat discount on delivery, regardless of method.
        :param delivery_method:
        :return: our delivery cost as a function of the delivery method.
        """
        print("Calling classmethod delivery_cost() from class PepperoniPizza") # debugging

        return super().delivery_cost(delivery_method) - cls.DELIVERY_DISCOUNT


# =============================================================================
#                            TESTS
# =============================================================================

def test():
    print("Basic pizza delivered for-here costs: %s" % BasicPizza(10).cost('for_here'))
    print()
    print("Square pizza delivered pick-up-to-go costs: %s" % SquarePizza(10).cost('pick_up_to_go'))
    print()
    print("Pepperoni pizza delivered deliver-to-house costs: %s" % PepperoniPizza(10).cost('deliver_to_house'))


if __name__ == '__main__':
    test()
