from rest_framework import serializers

from core.models import Ingredient, Recipe


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for the ingredient objects"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for the recipe objects"""
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients')
        read_only_fields = ('id',)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            Ingredient.objects.create(recipe=recipe, **ingredient)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description
        )
        instance.save()
        if ingredients:
            Ingredient.objects.filter(recipe=instance).delete()
            for ingredient in ingredients:
                ingredient['recipe'] = instance
                Ingredient.objects.create(**ingredient)
        return instance
