# Define a Recipe class. A Recipe is initialized with a name
# and a list of IngredientAmount objects.
#
# Give your Recipe class an alternate constructor called "make"
# that takes a name and a **kwds arg of ingredient-name/amount pairs.
# The ingredient-name is a capitalized string, e.g., 'Lemon', corresponding to the name
# of an Ingredient class. NOTE: In order to convert the name of a class into the class object
# itself, you can use python's "eval()" built-in. Thus, eval("Lemon") -> <class '__main__.Lemon'>
#
# Create a "calories" property that represents that total calories of the recipe.
# Create a "grams" property that represents the total grams of the recipe.
# Create a read-only "name" property that represents the name of the recipe.
# Create a __repr__() method that returns a multi-line string representing the recipe. The string
# should contain the recipe's name, ingredients, total grams, and total calories. Here's an example:
# <lemonade:
#     <12 grams of sugar>
#     <20 grams of lemon>
#     <50 grams of water>
#  grams: 82.00
#  calories: 50.84
#  >

class Ingredient:
    NAME = ''
    DENSITY = 0.0
    CALORIES = 0.0

    @classmethod
    def calories_per_cm3(cls):
        return cls.CALORIES * cls.DENSITY


class Sugar(Ingredient):
    NAME = 'sugar'
    DENSITY = 1.59
    CALORIES = 3.87


class Lemon(Ingredient):
    NAME = 'lemon'
    DENSITY = 1.03
    CALORIES = .22


class Water(Ingredient):
    NAME = 'water'
    DENSITY = 1
    CALORIES = 0


class IngredientAmount:
    def __init__(self, ingredient, grams):
        self._grams = 1.0  # throw-away value. Will be reset below.
        self._ingredient = Sugar  # throw-away value. Will be reset below.
        self._calories = None

        self.grams = grams
        self.ingredient = ingredient

    @property
    def grams(self):
        return self._grams

    @grams.setter
    def grams(self, v):
        assert v > 0, "Grams must be positive."
        self._grams = v
        self._calories = self._calc_calories()

    @property
    def ingredient(self):
        return self._ingredient

    @ingredient.setter
    def ingredient(self, v):
        assert issubclass(v, Ingredient)
        self._ingredient = v
        self._calories = self._calc_calories()

    @property
    def calories(self):
        return self._calories

    def _calc_calories(self):
        return self.grams * self.ingredient.CALORIES

    def __repr__(self):
        return "<{grams} grams of {ingredient}>".format(grams = self.grams, ingredient = self.ingredient.NAME)


class Recipe:
    def __init__(self, name, ingredient_amounts):
        self._name = name
        self._ingredient_amounts = ingredient_amounts

    @staticmethod
    def ounces_to_grams(ounces):
        return 28.35 * ounces  # In real life, this hardcoded constant would be OUNCES_TO_GRAMS
        # and we wouldn't need a static method for the conversion.

    @classmethod
    def make(cls, name, **ingredient_amounts):
        """
        Create a new recipe object whose ingredient amounts are
        specified by the key/value pairs in ingredient_amount_dict,
        where the key is not a string but an Ingredient object.
        """
        return cls(name, [IngredientAmount(ingredient = eval(ingr), grams = amt) for ingr, amt in ingredient_amounts.items()])

    @classmethod
    def make_from_ounces(cls, name, **ingredient_amounts):
        new_dict = {ingr:cls.ounces_to_grams(amt) for ingr, amt in ingredient_amounts.items()}
        return cls.make(name, **new_dict)

    @property
    def calories(self):
        return sum(x.calories for x in self._ingredient_amounts)

    @property
    def grams(self):
        return sum(x.grams for x in self._ingredient_amounts)

    @property
    def name(self):
        return self._name

    def __repr__(self):
        lines = ["<{name}:".format(name = self.name)]
        lines.extend('    ' + str(ingred_amt) for ingred_amt in self._ingredient_amounts)
        lines.append("grams: {grams:.2f}".format(grams = self.grams))
        lines.append("calories: {calories:.2f}".format(calories = self.calories))
        lines.append('>')
        return '\n'.join(lines)

def test():
    print(Recipe.make_from_ounces('lemonade', Sugar = 12, Lemon = 20, Water = 50))

if __name__ == '__main__':
    test()