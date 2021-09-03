from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Ingredient


RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """Return recipe detail url"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def search_url(recipe_name):
    """Return recipe search url"""
    return f'{RECIPES_URL}?name={recipe_name}'


def sample_recipe(**params):
    """Create and return a sample recipe"""
    defaults = {
        'name': 'Sample recipe',
        'description': 'Sample description',
    }
    defaults.update(params)
    return Recipe.objects.create(**defaults)


class RecipeApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes"""
        recipe1 = sample_recipe(name='Pizza')
        recipe2 = sample_recipe(name='Fries')

        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0].get('name'), recipe1.name)
        self.assertEqual(res.data[1].get('name'), recipe2.name)

    def test_retrieve_recipe_by_id(self):
        """Test retrieving a single recipe by ID"""
        recipe = sample_recipe()
        url = detail_url(recipe.id)

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get('name'), recipe.name)

    def test_search_recipe_by_name(self):
        """Test searching for a recipe by name"""
        recipe = sample_recipe(name='Burger')

        res = self.client.get(search_url('Bur'))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0].get('name'), recipe.name)

    def test_create_recipe(self):
        """Test creating a recipe"""
        payload = {
            'name': 'Pizza',
            'description': 'Put it in the oven.',
            'ingredients': [
                {'name': 'Cheese'},
                {'name': 'Dough'},
                {'name': 'Tomato'},
            ]
        }

        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        self.assertEqual(payload.get('name'), recipe.name)

        ingredients = Ingredient.objects.filter(recipe=res.data['id'])
        self.assertEqual(ingredients.count(), 3)
        for ingredient_name in ingredients.values_list('name', flat=True):
            self.assertIn(ingredient_name, 'Cheese Dough Tomato')

    def test_update_recipe(self):
        """Test updating a recipe"""
        recipe = sample_recipe()
        url = detail_url(recipe.id)
        payload = {'name': 'Pizza'}

        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], payload.get('name'))

    def test_delete_recipe(self):
        """Test deleting a recipe"""
        recipe = sample_recipe()
        url = detail_url(recipe.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(pk=recipe.id).exists())
