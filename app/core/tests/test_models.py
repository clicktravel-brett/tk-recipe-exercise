from django.test import TestCase

from core import models


def sample_recipe():
    """Create and return a sample recipe"""
    return models.Recipe.objects.create(
        name='Sample recipe',
        description='Sample description',
    )


class ModelTests(TestCase):

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = sample_recipe()
        self.assertEqual(str(recipe), recipe.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            name='Cheese',
            recipe=sample_recipe(),
        )

        self.assertEqual(str(ingredient), ingredient.name)
