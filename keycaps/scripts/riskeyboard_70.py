#!/usr/bin/env python3

"""
Generates a whole Riskeyboard 70's worth of keycaps (and a few extras). Best way
to use this script is from within the `keycap_playground` directory.

.. bash::

    $ ./scripts/riskeyboard_70.py --out /tmp/output_dir
"""

# stdlib imports
import os, sys
import json
import argparse
from copy import deepcopy
from subprocess import getstatusoutput
# 3rd party stuff
from colorama import Fore, Back, Style
from colorama import init as color_init
color_init()
# Our own stuff
from keycap import Keycap

KEY_UNIT = 14.5 # Square that makes up the entire space of a key
BETWEENSPACE = 0.8 # Space between keycaps

class riskeyboard70_base(Keycap):
    """
    Base keycap definitions for Gotham Rounded
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key_profile = "riskeycap"
        self.key_rotation = [0,110.1,90]
        self.key_length = KEY_UNIT-BETWEENSPACE
        self.key_width = KEY_UNIT-BETWEENSPACE
        self.wall_thickness = 0.45*2.25
        self.uniform_wall_thickness = True
        self.dish_thickness = 0.6 # Note: Not actually used
        self.stem_type = "box_cherry"
        self.stem_top_thickness = 0.5 # Note: Not actually used
        self.stem_inside_tolerance = 0.2
        # Disabled stem side support because it seems it is unnecessary @0.16mm
        self.stem_side_supports = [0,0,0,0]
        self.stem_locations = [[0,0,0]]
        self.stem_sides_wall_thickness = 0.5; # Thick (good sound/feel)
        # Because we do strange things we need legends bigger on the Z
        self.scale = [
            [1,1,1],
            [1,1.75,3], # For the pipe to make it taller/more of a divider
            [1,1,3],
        ]
        self.fonts = [
            #"Gotham Rounded:style=Bold",
            #"Gotham Rounded:style=Bold",
            "Arial Black:style=Regular",
        ]
        self.font_sizes = [
            5.5,
            4, # Gotham Rounded second legend (top right)
            4, # Front legend
        ]
        self.trans = [
            [-3,-2.6,2], # Lower left corner Gotham Rounded
            [3.5,3,1], # Top right Gotham Rounded
            [0.15,-3,2], # Front legend
        ]
        self.rotation = [
            [0,0,0],
            [0,-20,0],
            [68,0,0],
        ]
        self.postinit(**kwargs)

# KEY_ROTATION = [0,107.8,90]; // GEM profile rotation 1.5U

class riskeyboard70_alphas(riskeyboard70_base):
    """
    Tilde needs some changes because by default it's too small
    """
    def __init__(self, homing_dot=False, **kwargs):
        super().__init__(**kwargs)
        self.font_sizes = [
            5.5, # Regular Gotham Rounded
            4,
            4, # Front legend
        ]
        self.trans = [
            [-0.1,0,0], # Centered when angled -20°
            [3.5,3,1], # Top right Gotham Rounded
            [0.15,-3,2], # Front legend
        ]
        if homing_dot:
            self.homing_dot_length = 3
        self.postinit(**kwargs)

class riskeyboard70_FKey(riskeyboard70_alphas):
    """
    F keys are too large, need to scale smaller
    """
    def __init__(self, homing_dot=False, **kwargs):
        super().__init__(**kwargs)
        self.font_sizes = [
            3, # Regular Gotham Rounded
            4,
            4, # Front legend
        ]
        self.postinit(**kwargs)

class riskeyboard70_home(riskeyboard70_alphas):
    """
    F keys are too large, need to scale smaller
    """
    def __init__(self, homing_dot=False, **kwargs):
        super().__init__(**kwargs)
        self.font_sizes = [
            9, # Regular Gotham Rounded
            4,
            4, # Front legend
        ]
        self.fonts = [
            #"Gotham Rounded:style=Bold",
            #"Gotham Rounded:style=Bold",
            "Arial Black:style=Regular",
        ]
        self.postinit(**kwargs)

class riskeyboard70_numrow(riskeyboard70_base):
    """
    Number row numbers are slightly different
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fonts = [
            "Gotham Rounded:style=Bold", # Main char
            "Gotham Rounded:style=Bold", # Pipe character
            "Gotham Rounded:style=Bold", # Symbol
            "Arial Black:style=Regular", # F-key
        ]
        self.font_sizes = [
            4.5, # Regular character
            4.5, # Pipe
            4.5, # Regular Gotham Rounded symbols
            3.5, # Front legend
        ]
        self.trans = [
            [-0.3,0,0], # Left Gotham Rounded
            [2.6,0,0], # Center Gotham Rounded |
            [5,0,1], # Right-side Gotham symbols
            [0.15,-2,2], # F-key
        ]
        self.rotation = [
            [0,-20,0],
            [0,-20,0],
            [0,-20,0],
            [68,0,0],
        ]
        self.scale = [
            [1,1,3],
            [1,1.75,3], # For the pipe to make it taller/more of a divider
            [1,1,3],
            [1,1,3],
        ]
        self.postinit(**kwargs)

class riskeyboard70_tilde(riskeyboard70_numrow):
    """
    Tilde needs some changes because by default it's too small
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_sizes[0] = 6.5 # ` symbol
        self.font_sizes[2] = 5.5 # ~ symbol
        self.trans[0] = [-0.3,-2.7,0] # `
        self.trans[2] = [5.5,-1,1]    # ~

class riskeyboard70_2(riskeyboard70_numrow):
    """
    2 needs some changes based on the @ symbol
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fonts[2] = "Aharoni"
        self.font_sizes[2] = 4.5 # @ symbol (Aharoni)
        self.trans[2] = [5.4,0,1]

class riskeyboard70_3(riskeyboard70_numrow):
    """
    3 needs some changes based on the # symbol (slightly too big)
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_sizes[2] = 4 # # symbol (Gotham Rounded)
        self.trans[2] = [5.5,0,1] # Move to the right a bit

class riskeyboard70_5(riskeyboard70_numrow):
    """
    5 needs some changes based on the % symbol (too big, too close to bar)
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_sizes[2] = 3.75 # % symbol
        self.trans[2] = [5.2,0,1]

class riskeyboard70_7(riskeyboard70_numrow):
    """
    7 needs some changes based on the & symbol (it's too big)
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_sizes[2] = 3.85 # & symbol
        self.trans[2] = [5.2,0,1]

class riskeyboard70_8(riskeyboard70_numrow):
    """
    8 needs some changes based on the tiny * symbol
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_sizes[2] = 7.5 # * symbol (Gotham Rounded)
        self.trans[2] = [5.2,-1.9,1] # * needs a smidge of repositioning

class riskeyboard70_equal(riskeyboard70_numrow):
    """
    = needs some changes because it and the + are a bit off center
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.trans[0] = [-0.3,-0.5,0] # = sign adjustments
        self.trans[2] = [5,-0.3,1] # + sign adjustments

class riskeyboard70_dash(riskeyboard70_numrow):
    """
    The dash (-) is fine but the underscore (_) needs minor repositioning.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.trans[2] = [5.2,-1,1] # _ needs to go down and to the right a bit
        self.scale[2] = [0.8,1,3] # Also needs to be squished a bit

class riskeyboard70_double_legends(riskeyboard70_base):
    """
    For regular keys that have two legends... ,./;'[]
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fonts = [
            "Gotham Rounded:style=Bold", # Main legend
            "Gotham Rounded:style=Bold", # Pipe character
            "Gotham Rounded:style=Bold", # Second legend
        ]
        self.font_sizes = [
            4.5, # Regular Gotham Rounded character
            4.5, # Pipe
            3, # Regular Gotham Rounded character
        ]
        self.trans = [
            [-2,0,0], # Left Gotham Rounded
            [0,0,0], # Center Gotham Rounded |
            [2,0,0], # Right-side Gotham symbols
        ]
        self.rotation = [
            [0,0,0],
            [0,0,0],
            [0,0,0],
        ]
        self.scale = [
            [1,1,1],
            [1,1.75,3], # For the pipe to make it taller/more of a divider
            [1,1,1],
        ]
        self.postinit(**kwargs)

class riskeyboard70_prtsc(riskeyboard70_double_legends):
    """
    Rescale for minus key
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_sizes = [
            2.5,
            3,
            2.5,
        ]
        self.postinit(**kwargs)

class riskeyboard70_pg_ptr(riskeyboard70_double_legends):
    """
    Rescale for minus key
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_sizes = [
            3,
            3,
            4.5,
        ]
        self.fonts[2] = "Hack"
        self.postinit(**kwargs)

class riskeyboard70_minus(riskeyboard70_double_legends):
    """
    Rescale for minus key
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scale = [
            [2,2,1],
            [1,1.75,3], # For the pipe to make it taller/more of a divider
            [2,2,1],
        ]
        self.postinit(**kwargs)

class riskeyboard70_tick(riskeyboard70_double_legends):
    """
    Rescale for tick key
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.trans = [
            [-2.5,-1,0], # Left Gotham Rounded
            [0,0,0], # Center Gotham Rounded |
            [2,-0.5,0], # Right-side Gotham symbols
        ]
        self.font_sizes = [
            5.5, # Regular Gotham Rounded character
            4.5, # Pipe
            4.5, # Regular Gotham Rounded character
        ]
        self.postinit(**kwargs)

class riskeyboard70_gt_lt(riskeyboard70_double_legends):
    """
    The greater than (>) and less than (<) signs need to be adjusted down a bit
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.trans[0] = [-0.3,-0.1,0] # , and . are the tiniest bit too high
        self.trans[2] = [5.2,-0.35,1] # < and > are too high for some reason

class riskeyboard70_brackets(riskeyboard70_double_legends):
    """
    The curly braces `{}` needs to be moved to the right a smidge
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.trans[2] = [5.2,0,1] # Just a smidge to the right

class riskeyboard70_semicolon(riskeyboard70_double_legends):
    """
    The semicolon ends up being slightly higher than the colon but it looks
    better if the top dot in both is aligned.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.trans[0] = [0.2,-0.4,0]
        self.trans[2] = [4.7,0,1]

class riskeyboard70_1_U_text(riskeyboard70_alphas):
    """
    Ctrl, Del, and Ins need to be downsized and moved a smidge.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kwargs_copy = deepcopy(kwargs)
        self.font_sizes[0] = 4
        self.trans[0] = [2.5,0,0]
        self.postinit(**kwargs_copy)

class riskeyboard70_arrows(riskeyboard70_alphas):
    """
    Arrow symbols (◀▶▲▼) needs a different font (Hack)
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fonts[0] = "Hack"
        #self.fonts[2] = "FontAwesome" # For next/prev track icons
        #self.font_sizes[2] = 4 # FontAwesome prev/next icons
        #self.trans[2] = [0,-2,2] # Ditto

class riskeyboard70_fontawesome(riskeyboard70_alphas):
    """
    For regular centered FontAwesome icon keycaps.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fonts[0] = "FontAwesome"
        self.font_sizes[0] = 5
        self.trans[0] = [2.6,0.3,0]

class riskeyboard70_1_25U(riskeyboard70_alphas):
    """
    The base for all 1.25U keycaps.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kwargs_copy = deepcopy(kwargs) # Because self.trans[0] updates in place
        self.key_length = KEY_UNIT*1.25-BETWEENSPACE
#        self.key_rotation = [0,108.55,90]
        self.trans[0] = [0.5,0,0]
        self.postinit(**kwargs_copy)
        if not self.name.startswith('1.25U_'):
            self.name = f"1.25U_{self.name}"

class riskeyboard70_1_4U(riskeyboard70_alphas):
    """
    The base for all 1.4U keycaps.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kwargs_copy = deepcopy(kwargs) # Because self.trans[0] updates in place
        self.key_length = (KEY_UNIT-2)*1.4+2-BETWEENSPACE
        self.font_sizes[0] = 4
        self.trans[0] = [0,0,0]
        self.postinit(**kwargs_copy)
        if not self.name.startswith('1.4U_'):
            self.name = f"1.4U_{self.name}"

class riskeyboard70_1_6U(riskeyboard70_alphas):
    """
    The base for all 1.6U keycaps.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kwargs_copy = deepcopy(kwargs) # Because self.trans[0] updates in place
        self.key_length = (KEY_UNIT-2)*1.6+2-BETWEENSPACE
        self.font_sizes[0] = 4
        self.trans[0] = [0,0,0]
        self.postinit(**kwargs_copy)
        if not self.name.startswith('1.6U_'):
            self.name = f"1.6U_{self.name}"

class riskeyboard70_1_5U(riskeyboard70_double_legends):
    """
    The base for all 1.5U keycaps.

    .. note:: Uses riskeyboard70_double_legends because of the \\| key.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key_length = KEY_UNIT*1.5-BETWEENSPACE
        #self.key_rotation = [0,107.825,90]
        self.trans[0] = [1.5, 0, 0]
        self.postinit(**kwargs)
        if not self.name.startswith('1.5U_'):
            self.name = f"1.5U_{self.name}"

class riskeyboard70_bslash(riskeyboard70_double_legends):
    """
    Backslash key needs a very minor adjustment to the backslash.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key_length = (KEY_UNIT-2)*2+2-BETWEENSPACE
        self.trans[0] = [-1.2,0,0.3] # Move \ to the left a bit more than normal

class riskeyboard70_tab(riskeyboard70_1_5U):
    """
    "Tab" needs to be centered.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_sizes[0] = 4.5 # Regular Gotham Rounded
        self.trans[0] = [2.6,0,0] # Centered when angled -20°

class riskeyboard70_1_75U(riskeyboard70_alphas):
    """
    The base for all 1.75U keycaps.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key_length = KEY_UNIT*1.75-BETWEENSPACE
        self.key_rotation = [0,107.85,90]
        self.postinit(**kwargs)
        if not self.name.startswith('1.75U_'):
            self.name = f"1.75U_{self.name}"

class riskeyboard70_2U(riskeyboard70_alphas):
    """
    The base for all 2U keycaps.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key_length = (KEY_UNIT-2)*2+2-BETWEENSPACE
        self.font_sizes[0] = 4
        self.key_rotation = [0,107.85,90] # Same as 1.75U
        if "dish_invert" in kwargs and kwargs["dish_invert"]:
            self.key_rotation = [0,111.88,90] # Spacebars are different
        self.postinit(**kwargs)
        if not self.name.startswith('2U_'):
            self.name = f"2U_{self.name}"

class riskeyboard70_2_25U(riskeyboard70_alphas):
    """
    The base for all 2.25U keycaps.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kwargs_copy = deepcopy(kwargs)
        self.key_length = KEY_UNIT*2.25-BETWEENSPACE
        self.key_rotation = [0,107.85,90] # Same as 1.75U and 2U
        if "dish_invert" in kwargs and kwargs["dish_invert"]:
            self.key_rotation = [0,111.88,90] # Spacebars are different
        self.stem_locations = [[0,0,0], [12,0,0], [-12,0,0]]
        self.trans[0] = [3.1,0.2,0]
        self.font_sizes[0] = 4
        self.postinit(**kwargs_copy)
        if not self.name.startswith('2.25U_'):
            self.name = f"2.25U_{self.name}"

class riskeyboard70_2_5U(riskeyboard70_alphas):
    """
    The base for all 2.5U keycaps.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kwargs_copy = deepcopy(kwargs)
        self.key_length = KEY_UNIT*2.5-BETWEENSPACE
        self.key_rotation = [0,107.85,90] # Same as 1.75U and 2U
        if "dish_invert" in kwargs and kwargs["dish_invert"]:
            self.key_rotation = [0,111.88,90] # Spacebars are different
        self.stem_locations = [[0,0,0], [12,0,0], [-12,0,0]]
        self.trans[0] = [3.1,0.2,0]
        self.font_sizes[0] = 4
        self.postinit(**kwargs_copy)
        if not self.name.startswith('2.5U_'):
            self.name = f"2.5U_{self.name}"

class riskeyboard70_2_6U(riskeyboard70_alphas):
    """
    The base for all 2.6U keycaps.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kwargs_copy = deepcopy(kwargs)
        self.key_length = (KEY_UNIT-2)*2.6+2-BETWEENSPACE
        self.key_rotation = [0,107.85,90] # Same as 1.75U and 2U
        if "dish_invert" in kwargs and kwargs["dish_invert"]:
            self.key_rotation = [0,111.88,90] # Spacebars are different
        self.stem_locations = [[0,0,0], [11,0,0], [-12,0,0]]
        self.font_sizes[0] = 4
        self.postinit(**kwargs_copy)
        if not self.name.startswith('2.6U_'):
            self.name = f"2.6U_{self.name}"

class riskeyboard70_enter(riskeyboard70_2_6U):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kwargs_copy = deepcopy(kwargs)
        self.stem_locations = [[0,0,0], [11.5,0,0], [-12,0,0]]
        self.postinit(**kwargs_copy)
        if not self.name.startswith('2.6U_'):
            self.name = f"2.6U_{self.name}"

class riskeyboard70_backspace(riskeyboard70_2_6U):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kwargs_copy = deepcopy(kwargs)
        self.font_sizes[0] = 3
        self.stem_locations = [[0,0,0], [11.5,0,0], [-12,0,0]]
        self.postinit(**kwargs_copy)
        if not self.name.startswith('2.6U_'):
            self.name = f"2.6U_{self.name}"

class riskeyboard70_leftSpace(riskeyboard70_alphas):
    """
    Left space bar
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kwargs_copy = deepcopy(kwargs)
        self.key_length = 49+2-BETWEENSPACE
        self.key_rotation = [0,107.85,90] # Same as 1.75U and 2U
        if "dish_invert" in kwargs and kwargs["dish_invert"]:
            self.key_rotation = [0,111.88,90] # Spacebars are different
        self.stem_locations = [[0,0,0], [20,0,0], [-20,0,0]]
        self.postinit(**kwargs_copy)

class riskeyboard70_rightSpace(riskeyboard70_alphas):
    """
    Left space bar
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kwargs_copy = deepcopy(kwargs)
        self.key_length = 51+2-BETWEENSPACE
        self.key_rotation = [0,107.85,90] # Same as 1.75U and 2U
        if "dish_invert" in kwargs and kwargs["dish_invert"]:
            self.key_rotation = [0,111.88,90] # Spacebars are different
        self.stem_locations = [[0,0,0], [21,0,0], [-21,0,0]]
        self.postinit(**kwargs_copy)

class riskeyboard70_2_75U(riskeyboard70_alphas):
    """
    The base for all 2.75U keycaps.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kwargs_copy = deepcopy(kwargs)
        self.key_length = KEY_UNIT*2.75-BETWEENSPACE
        self.key_rotation = [0,107.85,90] # Same as 1.75U and 2U
        if "dish_invert" in kwargs and kwargs["dish_invert"]:
            self.key_rotation = [0,111.88,90] # Spacebars are different
        self.stem_locations = [[0,0,0], [12,0,0], [-12,0,0]]
        self.trans[0] = [3.1,0.2,0]
        self.font_sizes[0] = 4
        self.postinit(**kwargs_copy)
        if not self.name.startswith('2.75U_'):
            self.name = f"2.75U_{self.name}"

class riskeyboard70_6_25U(riskeyboard70_alphas):
    """
    The base for all 6.25U keycaps.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kwargs_copy = deepcopy(kwargs)
        self.key_length = KEY_UNIT*6.25-BETWEENSPACE
        self.key_rotation = [0,107.85,90] # Same as 1.75U and 2U
        if "dish_invert" in kwargs and kwargs["dish_invert"]:
            self.key_rotation = [0,111.88,90] # Spacebars are different
        self.stem_locations = [[0,0,0], [50,0,0], [-50,0,0]]
        self.trans[0] = [3.1,0.2,0]
        self.font_sizes[0] = 4
        self.postinit(**kwargs_copy)
        if not self.name.startswith('6.25U_'):
            self.name = f"6.25U_{self.name}"

class riskeyboard70_7U(riskeyboard70_alphas):
    """
    The base for all 7U keycaps.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kwargs_copy = deepcopy(kwargs)
        self.key_length = KEY_UNIT*7-BETWEENSPACE
        self.key_rotation = [0,107.85,90] # Same as 1.75U and 2U
        if "dish_invert" in kwargs and kwargs["dish_invert"]:
            self.key_rotation = [0,111.88,90] # Spacebars are different
        self.stem_locations = [[0,0,0], [57,0,0], [-57,0,0]]
        self.trans[0] = [3.1,0.2,0]
        self.font_sizes[0] = 4
        self.postinit(**kwargs_copy)
        if not self.name.startswith('7U_'):
            self.name = f"7U_{self.name}"
    '''
    riskeyboard70_alphas(legends=["A"]),
    riskeyboard70_alphas(legends=["B"]),
    riskeyboard70_alphas(legends=["C"]),
    riskeyboard70_alphas(legends=["D"]),
    riskeyboard70_alphas(legends=["E"]),
    riskeyboard70_alphas(legends=["F"], homing_dot=True),
    riskeyboard70_alphas(legends=["G"]),
    riskeyboard70_alphas(legends=["H"]),
    riskeyboard70_alphas(legends=["I"]),
    riskeyboard70_alphas(legends=["J"], homing_dot=True),
    riskeyboard70_alphas(legends=["K"]),
    riskeyboard70_alphas(legends=["L"]),
    riskeyboard70_alphas(legends=["M"]),
    riskeyboard70_alphas(legends=["N"]),
    riskeyboard70_alphas(legends=["O"]),
    riskeyboard70_alphas(legends=["P"]),
    riskeyboard70_alphas(legends=["Q"]),
    riskeyboard70_alphas(legends=["R"]),
    riskeyboard70_alphas(legends=["S"]),
    riskeyboard70_alphas(legends=["T"]),
    riskeyboard70_alphas(legends=["U"]),
    riskeyboard70_alphas(legends=["V"]),
    riskeyboard70_alphas(legends=["W"]),
    riskeyboard70_alphas(legends=["X"]),
    riskeyboard70_alphas(legends=["Y"]),
    riskeyboard70_alphas(legends=["Z"]),
    riskeyboard70_double_legends(name="lbracket", legends=["[", "", "{"]),
    riskeyboard70_double_legends(name="rbracket", legends=["]", "", "}"]),
    riskeyboard70_double_legends(name="semicolon", legends=[";", "", ":"]),
    riskeyboard70_double_legends(name="quote", legends=["'", "", '\"']),
    riskeyboard70_double_legends(name="slash", legends=["/", "", "?"]),
    '''
KEYCAPS = [
    # 1U keys
    #riskeyboard70_double_legends(name="backslash", legends=["\\", "", "|"]),
    #riskeyboard70_double_legends(name="gt", legends=[".", "", ">?"]),
    #riskeyboard70_double_legends(name="lt", legends=[",", "", "<?"]),
    riskeyboard70_alphas(name="blank", legends=[""]),
    riskeyboard70_alphas(legends=["fn"]),
    riskeyboard70_FKey(legends=["F1"]),
    riskeyboard70_FKey(legends=["F2"]),
    riskeyboard70_FKey(legends=["F3"]),
    riskeyboard70_FKey(legends=["F4"]),
    riskeyboard70_FKey(legends=["F5"]),
    riskeyboard70_FKey(legends=["F6"]),
    riskeyboard70_FKey(legends=["F7"]),
    riskeyboard70_FKey(legends=["F8"]),
    riskeyboard70_FKey(legends=["F9"]),
    riskeyboard70_FKey(legends=["F10"]),
    riskeyboard70_FKey(legends=["F11"]),
    riskeyboard70_FKey(legends=["F12"]),
    riskeyboard70_FKey(legends=["esc"]),
    riskeyboard70_prtsc(name="prt", legends=["prt", "", "sc"]),
    riskeyboard70_FKey(legends=["ins"]),
    riskeyboard70_FKey(legends=["del"]),
    riskeyboard70_home(name="home", legends=["\\u2302"]), # ⌂
    riskeyboard70_FKey(legends=["end"]),
    riskeyboard70_pg_ptr(name="pup", legends=["pg", "", '\\u25B2']), # ▲
    riskeyboard70_pg_ptr(name="pdn", legends=["pg", "", '\\u25BC']), # ▼

    riskeyboard70_double_legends(name="1", legends=["1", "", '!']),
    riskeyboard70_double_legends(name="2", legends=["2", "", '@']),
    riskeyboard70_double_legends(name="3", legends=["3", "", '#']),
    riskeyboard70_double_legends(name="4", legends=["4", "", '$']),
    riskeyboard70_double_legends(name="5", legends=["5", "", '%']),
    # follow two symbols were modified to run through powershell. ^^ escapes ^, "&" allows special character &
    riskeyboard70_double_legends(name="6", legends=["6", "", '^^']),
    riskeyboard70_double_legends(name="7", legends=["7", "", '"&"']),
    riskeyboard70_double_legends(name="8", legends=["8", "", '*']),
    riskeyboard70_double_legends(name="9", legends=["9", "", '(']),
    riskeyboard70_double_legends(name="0", legends=["0", "", ')']),
    riskeyboard70_double_legends(name="equal", legends=["=", "", '+']),
    riskeyboard70_double_legends(name="gt", legends=[".", "", '">"']),
    riskeyboard70_double_legends(name="lt", legends=[",", "", '"<"']),
    riskeyboard70_tick(name="tick", legends=[r"`", "", "~"]),
    riskeyboard70_double_legends(name="quote", legends=[r"'", "", r'\\\"']),
    riskeyboard70_minus(name="minus", legends=["-", "", '_']),
    riskeyboard70_1_4U(legends=["alt"]),
    riskeyboard70_1_6U(name="LCtrl", legends=["ctrl"]),
    riskeyboard70_1_6U(legends=["tab"]),
    riskeyboard70_2U(legends=["caps"]),
    riskeyboard70_2U(name="RCtrl", legends=["ctrl"]),
    riskeyboard70_2U(name="RShift", legends=["shift"]),
    riskeyboard70_bslash(name="bslash", legends=[r'\\\\', "", '"|"']),

    # TODO: 2.6 and longer need supports on the sides
    riskeyboard70_2_6U(name="LShift", legends=["shift"]),
    # riskeyboard70_2_6U(name="backspace", legends=["\u2190"]),
    riskeyboard70_enter(legends=["enter"]),
    riskeyboard70_backspace(legends=["backspace"]),
    riskeyboard70_leftSpace(name="LSpace", legends=[""], dish_invert=True),
    riskeyboard70_rightSpace(name="RSpace", legends=[""], dish_invert=True),

    # keys that don't work with windows terminal, either because of unicode or escape quotes
    riskeyboard70_arrows(name="left", legends=["◀"]),
    riskeyboard70_arrows(name="right", legends=["▶"]),
    riskeyboard70_arrows(name="up", legends=["▲"]),
    riskeyboard70_arrows(name="down", legends=["▼"]),
]

def print_keycaps():
    """
    Prints the names of all keycaps in KEYCAPS.
    """
    print(Style.BRIGHT +
          f"Here's all the keycaps we can render:\n" + Style.RESET_ALL)
    keycap_names = ", ".join(a.name for a in KEYCAPS)
    print(f"{keycap_names}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Render keycap STLs for all the Riskeyboard 70's switches.")
    parser.add_argument('--out',
        metavar='<filepath>', type=str, default=".",
        help='Where the generated STL files will go.')
    parser.add_argument('--force',
        required=False, action='store_true',
        help='Forcibly re-render STL files even if they already exist.')
    parser.add_argument('--legends',
        required=False, action='store_true',
        help='If True, generate a separate set of STLs for legends.')
    parser.add_argument('--keycaps',
        required=False, action='store_true',
        help='If True, prints out the names of all keycaps we can render.')
    parser.add_argument('names',
        nargs='*', metavar="name",
        help='Optional name of specific keycap you wish to render')
    args = parser.parse_args()
    #print(args)
    if len(sys.argv) == 1:
        parser.print_help()
        print("")
        print_keycaps()
        sys.exit(1)
    if args.keycaps:
        print_keycaps()
        sys.exit(1)
    if not os.path.exists(args.out):
        print(Style.BRIGHT +
              f"Output path, '{args.out}' does not exist; making it..."
              + Style.RESET_ALL)
        os.mkdir(args.out)
    print(Style.BRIGHT + f"Outputting to: {args.out}" + Style.RESET_ALL)
    if args.names: # Just render the specified keycaps
        matched = False
        for name in args.names:
            for keycap in KEYCAPS:
                if keycap.name.lower() == name.lower():
                    keycap.output_path = f"{args.out}"
                    matched = True
                    exists = False
                    if not args.force:
                        if os.path.exists(f"{args.out}/{keycap.name}.stl"):
                            print(Style.BRIGHT +
                                f"{args.out}/{keycap.name}.stl exists; "
                                f"skipping..."
                                + Style.RESET_ALL)
                            exists = True
                    if not exists:
                        print(Style.BRIGHT +
                            f"Rendering {args.out}/{keycap.name}.stl..."
                            + Style.RESET_ALL)
                        print(keycap)
                        retcode, output = getstatusoutput(str(keycap))
                        print(output)
                        if retcode == 0: # Success!
                            print(
                                f"{args.out}/{keycap.name}.stl "
                                f"rendered successfully")
                    if args.legends:
                        keycap.name = f"{keycap.name}_legends"
                        if os.path.exists(f"{args.out}/{keycap.name}.stl"):
                            print(Style.BRIGHT +
                                f"{args.out}/{keycap.name}.stl exists; "
                                f"skipping..."
                                + Style.RESET_ALL)
                            continue
                        print(Style.BRIGHT +
                            f"Rendering {args.out}/{keycap.name}.stl..."
                            + Style.RESET_ALL)
                        print(keycap)
                        retcode, output = getstatusoutput(str(keycap))
                        if retcode == 0: # Success!
                            print(
                                f"{args.out}/{keycap.name}.stl "
                                f"rendered successfully")
        if not matched:
            print(f"Cound not find a keycap named {name}")
    else:
        # First render the keycaps
        for keycap in KEYCAPS:
            keycap.output_path = f"{args.out}"
            if not args.force:
                if os.path.exists(f"{args.out}/{keycap.name}.stl"):
                    print(Style.BRIGHT +
                        f"{args.out}/{keycap.name}.stl exists; skipping..."
                        + Style.RESET_ALL)
                    continue
            print(Style.BRIGHT +
                f"Rendering {args.out}/{keycap.name}.stl..."
                + Style.RESET_ALL)
            print(keycap)
            retcode, output = getstatusoutput(str(keycap))
            if retcode == 0: # Success!
                print(f"{args.out}/{keycap.name}.stl rendered successfully")
            print(output)
        # Next render the legends (for multi-material, non-transparent legends)
        if args.legends:
            for legend in KEYCAPS:
                if legend.legends == [""]:
                    continue # No actual legends
                legend.name = f"{legend.name}_legends"
                legend.output_path = f"{args.out}"
                legend.render = ["legends"]
                if not args.force:
                    if os.path.exists(f"{args.out}/{legend.name}.stl"):
                        print(Style.BRIGHT +
                            f"{args.out}/{legend.name}.stl exists; skipping..."
                            + Style.RESET_ALL)
                        continue
                print(Style.BRIGHT +
                    f"Rendering {args.out}/{legend.name}.stl..."
                    + Style.RESET_ALL)
                print(legend)
                retcode, output = getstatusoutput(str(legend))
                if retcode == 0: # Success!
                    print(f"{args.out}/{legend.name}.stl rendered successfully")
