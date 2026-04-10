import io
import unittest
from unittest.mock import patch

from fit1008.ass01.ed_utils.decorators import number, visibility

from fit1008.ass01.pokemon_base import PokeType, TypeEffectiveness


class TestTypeEffectiveness(unittest.TestCase):
    @number("1.1")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_get_effectiveness(self):
        self.assertEqual(
            TypeEffectiveness.get_effectiveness(PokeType.WATER, PokeType.GRASS),
            0.5,
        )
        self.assertEqual(
            TypeEffectiveness.get_effectiveness(PokeType.FIRE, PokeType.FLYING),
            1.0,
        )
        self.assertEqual(
            TypeEffectiveness.get_effectiveness(PokeType.GRASS, PokeType.WATER),
            2.0,
        )
        self.assertEqual(
            TypeEffectiveness.get_effectiveness(PokeType.ROCK, PokeType.FIRE),
            0.5,
        )

    @number("1.2")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_len(self):
        self.assertEqual(len(TypeEffectiveness()), 15)


if __name__ == "__main__":
    unittest.main()
