import unittest
from tools.audit_regalia_native_recipes import is_native_crafting_output


class NativeRegaliaRecipes(unittest.TestCase):
    def test_recipe_ingredient_does_not_authenticate_output(self):
        recipe = {'type': 'minecraft:crafting_shaped', 'key': {'X': {'item': 'test:reward'}},
                  'result': {'id': 'test:other'}}
        self.assertFalse(is_native_crafting_output(recipe, 'test:reward'))

    def test_conditional_or_smithing_progression_is_not_general_crafting(self):
        for recipe in (
            {'type': 'minecraft:smithing_transform', 'result': {'id': 'test:reward'}},
            {'type': 'minecraft:crafting_shaped', 'result': {'id': 'test:reward'},
             'neoforge:conditions': [{'type': 'neoforge:false'}]},
        ):
            self.assertFalse(is_native_crafting_output(recipe, 'test:reward'))

    def test_unconditional_native_result_is_accepted(self):
        self.assertTrue(is_native_crafting_output(
            {'type': 'minecraft:crafting_shapeless', 'result': {'id': 'test:reward'}}, 'test:reward'))
