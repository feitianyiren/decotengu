#
# DecoTengu - dive decompression library.
#
# Copyright (C) 2013 by Artur Wroblewski <wrobell@pld-linux.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
DecoTengu calculator tests.
"""

from decotengu.engine import GasMix
from decotengu.model import eq_schreiner, eq_gf_limit, TissueCalculator, \
    ZH_L16_GF, ZH_L16B_GF

import unittest
from unittest import mock

AIR = GasMix(depth=0, o2=21, n2=79, he=0)

class SchreinerEquationTestCase(unittest.TestCase):
    """
    Schreiner equation tests.
    """
    def test_air_ascent(self):
        """
        Test Schreiner equation - ascent 10m on air
        """
        # ascent, so rate == -1 bar/min
        v = eq_schreiner(4, 60, 0.79, -1, 3, 5.0)
        self.assertAlmostEqual(2.96198, v, 4)


    def test_air_descent(self):
        """
        Test Schreiner equation - descent 10m on air
        """
        # rate == 1 bar/min
        v = eq_schreiner(4, 60, 0.79, 1, 3, 5.0)
        self.assertAlmostEqual(3.06661, v, 4)


    def test_ean_ascent(self):
        """
        Test Schreiner equation - ascent 10m on EAN32
        """
        # ascent, so rate == -1 bar/min
        v = eq_schreiner(4, 60, 0.68, -1, 3, 5.0)
        self.assertAlmostEqual(2.9132, v, 4)


    def test_ean_descent(self):
        """
        Test Schreiner equation - descent 10m on EAN32
        """
        # rate == 1 bar/min
        v = eq_schreiner(4, 60, 0.68, 1, 3, 5.0)
        self.assertAlmostEqual(3.00326, v, 4)



class GradientFactorLimitTestCase(unittest.TestCase):
    """
    Gradient factor limit tests.
    """
    def test_gf_limit_n2_30(self):
        """
        Test 30% gradient factor limit for N2
        """
        v = eq_gf_limit(0.3, 3, 0, 1.1696, 0.5578)
        self.assertAlmostEqual(2.14013, v, 4)


    def test_gf_limit_n2_100(self):
        """
        Test 100% gradient factor limit for N2
        """
        v = eq_gf_limit(1.0, 3, 0, 1.1696, 0.5578)
        self.assertAlmostEqual(1.02099, v, 4)



class ZH_L16_GFTestCase(unittest.TestCase):
    """
    Buhlmann ZH-L16 decompression model with gradient factors tests.
    """
    def test_model_init(self):
        """
        Test deco model initialization
        """
        m = ZH_L16_GF()
        t = m.init(1.013)
        self.assertEquals(ZH_L16_GF.NUM_COMPARTMENTS, len(t))
        self.assertEquals([0.75092706] * ZH_L16_GF.NUM_COMPARTMENTS, t)


    def test_tissues_load(self):
        """
        Test deco model tissues gas loading
        """
        m = ZH_L16B_GF()
        n = m.NUM_COMPARTMENTS
        c_load = m.calc.load_tissue = mock.MagicMock(side_effect=range(1, 17))

        v = m.load(4, 60, AIR, -1, [0.79] * n)

        self.assertEquals(n, c_load.call_count)
        self.assertEquals(v, tuple(range(1, 17)))

        expected = tuple(range(n))
        results = tuple(t[0][5] for t in c_load.call_args_list)
        self.assertEquals(expected, results)


    def test_gf_limit(self):
        """
        Test deco model gradient factor limit calculation
        """
        with mock.patch('decotengu.model.eq_gf_limit') as f:
            f.side_effect = list(range(1, 17))
            m = ZH_L16B_GF()
            v = m.gf_limit(0.3, list(range(1, 17)))

            self.assertEquals(m.NUM_COMPARTMENTS, f.call_count)
            result = tuple(t[0][3] for t in f.call_args_list)
            self.assertEquals(m.N2_A, result)
            result = tuple(t[0][4] for t in f.call_args_list)
            self.assertEquals(m.N2_B, result)
            self.assertEquals(v, tuple(range(1, 17)))



class TissueCalculatorTestCase(unittest.TestCase):
    """
    Tissue calculator tests.
    """
    def test_tissue_load(self):
        """
        Test tissue calculator tissue gas loading
        """
        with mock.patch('decotengu.model.eq_schreiner') as f:
            f.return_value = 2
            m = ZH_L16B_GF
            c = TissueCalculator(m.N2_HALF_LIFE, m.HE_HALF_LIFE)
            v = c.load_tissue(4, 60, AIR, -1, 3, 1)
            f.assert_called_once_with(4, 60, 0.79, -1, 3, 8.0)
            self.assertEquals(2, v)


# vim: sw=4:et:ai