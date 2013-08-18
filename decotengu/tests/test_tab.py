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
Tabular calculator tests.
"""

from decotengu.tab import eq_schreiner_t, ZH_L16B_EXP_HALF_LIFE_10M

import unittest

class SchreinerTabularEquationTestCase(unittest.TestCase):
    """
    Schreiner equation tests.
    """
    def test_air_ascent(self):
        """
        Test Schreiner equation (tabular) - ascent 10m on air
        """
        # ascent, so rate == -1 bar/min
        v = eq_schreiner_t(4, 60, -1, 3, 5.0, ZH_L16B_EXP_HALF_LIFE_10M[0])
        self.assertAlmostEqual(2.96198, v, 4)


    def test_air_descent(self):
        """
        Test Schreiner equation (tabular) - descent 10m on air
        """
        # rate == 1 bar/min
        v = eq_schreiner_t(4, 60, 1, 3, 5.0, ZH_L16B_EXP_HALF_LIFE_10M[0])
        self.assertAlmostEqual(3.06661, v, 4)

# vim: sw=4:et:ai