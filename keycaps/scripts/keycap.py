#!/usr/bin/env python3

"""
Contains the Keycap class which makes it easy to script the generation of
keycaps using the Keycap Playground.
"""

import json
from pathlib import Path

KEY_UNIT = 14.5 # Square that makes up the entire space of a key
BETWEENSPACE = 0.8 # Space between keycaps

class Keycap(object):
    """
    A convenient abstraction for specifying a keycap's details.  The most useful
    way to use this class is to subclass it to make your own "base" class
    containing our kecap's parameters.  Example::

        class KeycapBase(Keycap):
        '''
        Base keycap definitions for keycaps using Gotham Rounded.
        '''
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.key_profile = "gem"
            self.key_rotation = [0,108.6,90]
            self.wall_thickness = 0.45*2.25
            self.uniform_wall_thickness = True
            self.stem_inside_tolerance = 0.15
            self.stem_sides_wall_thickness = 0.8; # Thick (good sound/feel)
            self.fonts = [
                "Gotham Rounded:style=Bold", # Main legend
                "Gotham Rounded:style=Bold", # Secondary (top right)
                "Arial Black:style=Regular", # Front-facing
            ]
            self.font_sizes = [
                5.5, # Regular legend (lower left)
                4, # Gotham Rounded second legend (top right)
                4, # Front legend
            ]
            self.trans = [
                [-3,-2.6,2], # Lower left corner Gotham Rounded
                [3.5,3,1], # Top right Gotham Rounded
                [0.15,-3,2], # Front legend
            ]
            self.rotation = [
                [0,-20,0], # -20 here to match the layer lines when printing
                [0,-20,0],
                [68,0,0], # Front-facing legends need a lot of rotation
            ]
            self.postinit(**kwargs)

    The call to `self.postinit(**kwargs)` is important if you want to be able
    to override things in `KeycapBase()` by passing them via arguments like so::

        tilde = KeycapBase(name="tilde", legends=["`", "", "~"])

    To actually generate a keycap you can use something like this::

        from subprocess import getstatusoutput
        retcode, output = getstatusoutput(str(tilde))
    """
    def __init__(self,
            name=None, render=["keycap", "stem"],
            key_profile="riskeycap",
            key_length=KEY_UNIT-BETWEENSPACE,
            key_width=KEY_UNIT-BETWEENSPACE,
            key_rotation=[0,0,0],
            key_height=9,
            key_top_difference=5,
            wall_thickness=0.45*2.25,
            dish_thickness=0.6,
            dish_type="sphere",
            dish_depth=1,
            dish_invert=False,
            dish_tilt=0,
            dish_tilt_curve=True,
            dish_fn=256,
            dish_corner_fn=64,
            uniform_wall_thickness=True,
            polygon_layers=10,
            polygon_layer_rotation=0,
            polygon_edges=4,
            polygon_rotation=True,
            corner_radius=1,
            corner_radius_curve=3,
            stem_type="box_cherry",
            stem_top_thickness=0.5,
            stem_inset=1,
            stem_inside_tolerance=0.2,
            stem_outside_tolerance_x=0.05,
            stem_outside_tolerance_y=0.05,
            stem_side_supports=[0,0,0,0],
            stem_locations=[[0,0,0]],
            stem_sides_wall_thickness=0.5,
            stem_snap_fit=False,
            stem_walls_inset=0,
            stem_walls_tolerance=0,
            homing_dot_length=0, # 0 means no "dot"
            homing_dot_width=1,
            homing_dot_x=0,
            homing_dot_y=-(KEY_UNIT-BETWEENSPACE) * 0.3,
            homing_dot_z=0, # How far it sticks out
            legends=[""],
            fonts=[], font_sizes=[],
            trans=[[0,0,0]], trans2=[[0,0,0]],
            rotation=[[0,0,0]], rotation2=[[0,0,0]],
            scale=[[1,1,1]], underset=[[0,0,0]],
            legend_carved=False,
            keycap_playground_path=Path("."),
            openscad_path=Path('"C:\Program Files\OpenSCAD\openscad.exe"'),
            output_path=Path(".")):
        self.name = name
        self.output_path = output_path
        self.render = render
        self.key_height = key_height
        self.key_length = key_length
        self.key_width = key_width
        self.key_profile = key_profile
        self.key_top_difference = key_top_difference
        if not self.name:
            if legends and legends[0]:
                self.name = legends[0]
            else:
                self.name = "keycap"
        self.key_rotation = key_rotation
        self.wall_thickness = wall_thickness
        self.dish_thickness = dish_thickness
        self.dish_invert = dish_invert
        self.dish_type = dish_type
        self.dish_depth = dish_depth
        self.dish_tilt = dish_tilt
        self.dish_tilt_curve = dish_tilt_curve
        self.dish_fn = dish_fn
        self.dish_corner_fn = dish_corner_fn
        self.uniform_wall_thickness = uniform_wall_thickness
        self.polygon_layers = polygon_layers
        self.polygon_layer_rotation = polygon_layer_rotation
        self.polygon_edges = polygon_edges
        self.polygon_rotation = polygon_rotation
        self.corner_radius = corner_radius
        self.corner_radius_curve = corner_radius_curve
        self.stem_type = stem_type
        self.stem_top_thickness = stem_top_thickness
        self.stem_inset = stem_inset
        self.stem_inside_tolerance = stem_inside_tolerance
        self.stem_outside_tolerance_x = stem_outside_tolerance_x
        self.stem_outside_tolerance_y = stem_outside_tolerance_y
        self.stem_locations = stem_locations
        self.stem_side_supports = stem_side_supports
        self.stem_sides_wall_thickness = stem_sides_wall_thickness
        self.stem_snap_fit = stem_snap_fit
        self.stem_walls_inset = stem_walls_inset
        self.stem_walls_tolerance = stem_walls_tolerance
        self.homing_dot_length = homing_dot_length
        self.homing_dot_width = homing_dot_width
        self.homing_dot_x = homing_dot_x
        self.homing_dot_y = homing_dot_y
        self.homing_dot_z = homing_dot_z
        self.legends = legends
        self.fonts = fonts
        self.font_sizes = font_sizes
        self.trans = trans
        self.trans2 = trans2
        self.rotation = rotation
        self.rotation2 = rotation2
        self.scale = scale
        self.underset = underset
        self.legend_carved = legend_carved
        self.keycap_playground_path = keycap_playground_path
        self.openscad_path = openscad_path

    # NOTE: This doesn't seem to work right for unknown reasons so you'll want
    #       to generate the quote keycap by hand on the command line.
    def quote(self, legends):
        """
        Checks for the edge case of a single quote (') legend and converts it
        into `"'"'"'"` so that bash will pass it correclty to OpenSCAD via
        `getstatusoutput()`.  Also covers the slash (\\) legend for
        completeness.

        .. note::

            Example of what it should look like: `LEGENDS="["'"'"'", "", "\""]";`
        """
        properly_escaped_quote = ''
        out = "["
        for i, legend in enumerate(legends):
            if legend == "'":
                out += "\\\"" + "'" + "\\\","
            elif legend == '"':
                out += r'"\""'
            else:
                out += "\\\"" + legend + "\\\","
        out = out.rstrip(',') # Get rid of trailing comma
        return out + "]"

    def __repr__(self):
        return f"""        name: {self.name}
        render: {self.render}
        key_profile: {self.key_profile}
        legends: {self.legends}
        trans: {self.trans}
        trans2: {self.trans2}
        rotation: {self.rotation}
        rotation2: {self.rotation2}
        scale: {self.scale}
        underset: {self.underset}"""

    def str_fmt(self, var):
        return json.dumps(var).replace('"', '\\"')
    
    def __str__(self):
        """
        Returns the OpenSCAD command line to use to generate this keycap.
        """
        # NOTE: Since OpenSCAD requires double quotes I'm using the json module
        #       to encode things that need it:
        return (
            f"{self.openscad_path} -o "#--enable=fast-csg -o "
            f"{self.output_path}\{self.name}.stl "
            f'-D RENDER="{self.str_fmt(self.render)}" '
            f'-D KEY_PROFILE="{self.str_fmt(self.key_profile)}" '
            f'-D KEY_LENGTH="{round(self.key_length,2)}" '
            f'-D KEY_WIDTH="{round(self.key_width,2)}" '
            f'-D KEY_TOP_DIFFERENCE="{self.key_top_difference}" '
            f'-D KEY_ROTATION="{self.key_rotation}" '
            f'-D KEY_HEIGHT="{self.key_height}" '
            f'-D WALL_THICKNESS="{self.wall_thickness}" '
            f'-D UNIFORM_WALL_THICKNESS="{self.str_fmt(self.uniform_wall_thickness)}" '
            f'-D DISH_THICKNESS="{self.dish_thickness}" '
            f'-D DISH_INVERT="{self.str_fmt(self.dish_invert)}" '
            f'-D DISH_TYPE="{self.str_fmt(self.dish_type)}" '
            f'-D DISH_DEPTH="{self.dish_depth}" '
            f'-D DISH_TILT="{self.dish_tilt}" '
            f'-D DISH_TILT_CURVE="{self.str_fmt(self.dish_tilt_curve)}" '
            f'-D DISH_FN="{self.dish_fn}" '
            f'-D DISH_CORNER_FN="{self.dish_corner_fn}" '
            f'-D POLYGON_LAYERS="{self.polygon_layers}" '
            f'-D POLYGON_LAYER_ROTATION="{self.str_fmt(self.polygon_layer_rotation)}" '
            f'-D POLYGON_EDGES="{self.polygon_edges}" '
            f'-D POLYGON_ROTATION="{self.str_fmt(self.polygon_rotation)}" '
            f'-D CORNER_RADIUS="{self.corner_radius}" '
            f'-D CORNER_RADIUS_CURVE="{self.str_fmt(self.corner_radius_curve)}" '
            f'-D STEM_TYPE="{self.str_fmt(self.stem_type)}" '
            f'-D STEM_TOP_THICKNESS="{self.stem_top_thickness}" '
            f'-D STEM_INSET="{self.stem_inset}" '
            f'-D STEM_INSIDE_TOLERANCE="{self.stem_inside_tolerance}" '
            f'-D STEM_OUTSIDE_TOLERANCE_X="{self.stem_outside_tolerance_x}" '
            f'-D STEM_OUTSIDE_TOLERANCE_Y="{self.stem_outside_tolerance_y}" '
            f'-D STEM_SIDE_SUPPORTS="{self.stem_side_supports}" '
            f'-D STEM_SIDES_WALL_THICKNESS="{self.stem_sides_wall_thickness}" '
            f'-D STEM_LOCATIONS="{self.stem_locations}" '
            f'-D STEM_SNAP_FIT="{self.str_fmt(self.stem_snap_fit)}" '
            f'-D STEM_WALLS_INSET="{self.stem_walls_inset}" '
            f'-D STEM_WALLS_TOLERANCE="{self.stem_walls_tolerance}" '
            f'-D HOMING_DOT_LENGTH="{self.homing_dot_length}" '
            f'-D HOMING_DOT_WIDTH="{self.homing_dot_width}" '
            f'-D HOMING_DOT_X="{self.homing_dot_x}" '
            f'-D HOMING_DOT_Y="{self.homing_dot_y}" '
            f'-D HOMING_DOT_Z="{self.homing_dot_z}" '
            #f'-D LEGENDS="[\\"{self.legends}\\"]" '
            f'-D LEGENDS="{self.quote(self.legends)}" ' # (TODO) figure out the correct escape sequence
            f'-D LEGEND_FONTS="{self.str_fmt(self.fonts)}" '
            f'-D LEGEND_FONT_SIZES="{self.font_sizes}" '
            f'-D LEGEND_TRANS="{self.trans}" '
            f'-D LEGEND_TRANS2="{self.trans2}" '
            f'-D LEGEND_ROTATION="{self.rotation}" '
            f'-D LEGEND_ROTATION2="{self.rotation2}" '
            f'-D LEGEND_SCALE="{self.scale}" '
            f'-D LEGEND_UNDERSET="{self.underset}" '
            # NOTE: For some reason I have to duplicate RENDER here for it to work properly:
            f'-D RENDER="{self.str_fmt(self.render)}" '
            f"scad\keycap_playground.scad"
        )

    def postinit(self, **kwargs):
        """
        Override anything passed in via kwargs
        """
        #print(f"postinit kwargs: {kwargs}")
        for k, v in kwargs.items():
            #print(f"Updating: {k}: {v}")
            self.__dict__.update({k: v})
