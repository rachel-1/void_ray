// Modules related to the main body of the switch

use <utils.scad>

// Constants
CHERRY_CROSS_LENGTH = 4; // Length of the - and the | in the +
MAX_SINGLE_KEY_LEN = 20;
MIN_SPACE_BAR_LEN = 30;

// TODO: Document all these args
// The main housing of the switch that the sheath slides into
module switch_body(length, width, travel, taper=1.1, wall_thickness=1.4, sheath_wall_thickness=1.2, sheath_length=3, cover_overhang=1, cover_thickness=0.6, plate_thickness=1.5, plate_tolerance=0.2, stem_diameter=4.1, sheath_tolerance=0.2, lip_height=1, top_magnet_height=2, top_magnet_diameter=6, top_magnet_cover_thickness=-0.5, magnet_height=1.5, magnet_wall_thickness=0.5, magnet_thickness_tolerance=0.15, magnet_void=0.0, sheath_end_stop_thickness=0.8, corner_radius=0.5, droop_extra=0.2, sheath_clip_width=1.5, top_clip_hole_length=2.15, top_clip_hole_width=3.15, stem_tolerance=0.15, bridge_thickness=0.3, sheath_snug_magnet=true, sheath_inside_body=false, height=0) {
    total_travel = travel+top_magnet_height; // Actual total travel
    // How far into the body the stem shroud goes (so we can calculate depth)
    sheath_depth = (
        cover_thickness+sheath_length+total_travel-top_magnet_cover_thickness
        +magnet_height+magnet_wall_thickness*2+magnet_thickness_tolerance
        +magnet_void+sheath_end_stop_thickness); // NOTE: Does not include the lip_height on purpose
    // adjusted_magnet_wall_thickness = sheath_inside_body ? 0 : magnet_wall_thickness;
    body_height = height ? height : sheath_depth; // For clarity in the code
    echo(body_height=body_height);
    // NOTE: These two sheath variables need to match how they're handled in the actual sheath:
    sheath_width = stem_diameter+sheath_wall_thickness*2;
    sheath_height = stem_diameter+sheath_wall_thickness*2;
    snap_clip_protrusion = 0.2; // How much the little snap lip things stick out from the body (it gets rotate 45° so it's a little less, actually)
    snap_clip_thickness = 0.85; // How thick the clips are
    pin_diameter = 1.875; // Need to match the pin diameter used by the stabilizer clips
    clip_width = width/6;
    clip_side_hole_width = 0.35; // How wide the cutouts are beside each clip
    note(str("UNDER_PLATE_HEIGHT: ", body_height-cover_thickness));
    difference() {
        union() {
            // Generate the part of the body that overhangs the hole on the plate
            translate([0,0,cover_thickness/2])
                hull() { // This is tapered a bit to make removing the switch easier
                    squarish_rpoly(
                        xy=[length+cover_overhang-plate_tolerance/2, width+cover_overhang-plate_tolerance/2],
                        h=cover_thickness,
                        r=corner_radius, center=true);
                    translate([0,0,-cover_thickness/4]) squarish_rpoly(
                        xy=[length+cover_overhang*2-plate_tolerance/2, width+cover_overhang*2-plate_tolerance/2],
                        h=cover_thickness/2,
                        r=corner_radius, center=true);
                }
            // Generate the main body of the switch for the inner layer
            difference() {
                translate([0,0,cover_thickness]) hull() {
                    translate([0,0,plate_thickness/2]) squarish_rpoly(
                        xy=[width-plate_tolerance/2, width-plate_tolerance/2],
                        h=plate_thickness,
                        r=corner_radius, center=true);
                    translate([0,0,body_height-cover_thickness])
                        squarish_rpoly(
                            xy=[width/taper, width/taper],
                            h=cover_thickness/2, // Close enough
                            r=corner_radius, center=true);
                }
                // Cut out the corner so we don't have to worry about a large stem/magnet scraping the sides
                //adjusted_magnet_wall_thickness = sheath_inside_body ? 0 : magnet_wall_thickness;
                translate([
                -width/2.85,
                -width/2.85,
                body_height/2+top_magnet_height+magnet_wall_thickness+droop_extra-top_magnet_cover_thickness+sheath_length
                ])
                    cube([width/2,width/2,body_height], center=true);
                difference() {
                // NOTE: Because of the body taper we need to increase the wall thickness here slightly so that it prints well (don't want the slicer cutting off the corners).  That's why we have this "interior bulge" thing...
                    translate([0,0,-cover_thickness/2]) hull() {
                        // NOTE: The interior taper here is to give the wall-to-cover attachment a stronger bond (otherwise the top of the switch can break right off leaving you with a top and a hollow cube)
                        squarish_rpoly(
                            xy=[width-wall_thickness*3.75, width-wall_thickness*3.75],
                            h=cover_thickness/2,
                            r=corner_radius/1.5, center=true);
                        translate([0,0,body_height/4])
                            squarish_rpoly(
                                xy=[width-wall_thickness*2, width-wall_thickness*2],
                                h=cover_thickness/2,
                                r=corner_radius/1.5, center=true);
                        translate([0,0,cover_thickness+sheath_depth+magnet_height+wall_thickness/2])
                            squarish_rpoly(
                                xy=[width/taper-wall_thickness*1.25,
                                    width/taper-wall_thickness*1.25],
                                h=cover_thickness,
                                r=corner_radius/1.5, center=true);
                    }
                    // This gives the magnet a bit of a "seat" so it doesn't fall through:
                    translate([
                    -width/2-top_magnet_diameter/2.2,
                    -width/2-top_magnet_diameter/2.2,
                    -magnet_wall_thickness/2+top_magnet_height+magnet_wall_thickness+droop_extra-top_magnet_cover_thickness+sheath_length
                    ])
                        rotate([0,0,45])
                            cube([
                                width,
                                width,
                                magnet_wall_thickness,
                            ], center=true);
                } // end difference
                // Add a little hole that ensures the bridging goes right
                translate([
                -width/2+top_magnet_diameter/1.65,
                -width/2+top_magnet_diameter/1.65,
                -(magnet_wall_thickness+droop_extra)/2+top_magnet_height+magnet_wall_thickness+droop_extra-top_magnet_cover_thickness+sheath_length])
                    difference() {
                        cube([2,2,magnet_wall_thickness+droop_extra+0.01], center=true);
                        translate([0.65,0.65,0])
                            rotate([0,0,45])
                                cube([2,3,magnet_wall_thickness*10], center=true);
                    } // end difference
                // TODO: Make these hard-coded numbers like -4.7 take the size of the body into account...
                // Cut out the sides near where the stem presses against the magnet so it doesn't get caught on the sides
                // NOTE (Richard): the following two cuts don't do anything for the smaller switch
                // translate([
                //   -4.7,
                //   -1,
                //   top_magnet_height])
                //     cube([2,1.6,top_magnet_height*2], center=true);
                // translate([
                //   -1,
                //   -4.7,
                //   top_magnet_height])
                //     cube([1.6,2,top_magnet_height*2], center=true);
            }
            // Generate the main body of the switch for overlapping outer shell of larger switches
            difference() {
                // NOTE (Richard): main rectangle body
                translate([0,0,cover_thickness]) hull() {
                    translate([0,0,plate_thickness/2]) squarish_rpoly(
                        xy=[length-plate_tolerance/2, width-plate_tolerance/2],
                        h=plate_thickness,
                        r=corner_radius, center=true);
                    translate([0,0,body_height-cover_thickness])
                        squarish_rpoly(
                            xy=[length - (width - width/taper), width/taper],
                            h=cover_thickness/2, // Close enough
                            r=corner_radius, center=true);
                }
                // NOTE (Richard): cut into the main rectangle to make a hull
                // NOTE: Because of the body taper we need to increase the wall thickness here slightly so that it prints well (don't want the slicer cutting off the corners).  That's why we have this "interior bulge" thing...
                translate([0,0,-cover_thickness/2]) hull() {
                    // NOTE: The interior taper here is to give the wall-to-cover attachment a stronger bond (otherwise the top of the switch can break right off leaving you with a top and a hollow cube)
                    squarish_rpoly(
                        xy=[length-wall_thickness*3.75, width-wall_thickness*3.75],
                        h=cover_thickness/2,
                        r=corner_radius/1.5, center=true);
                    translate([0,0,body_height/4])
                        squarish_rpoly(
                            xy=[length-wall_thickness*2, width-wall_thickness*2],
                            h=cover_thickness/2,
                            r=corner_radius/1.5, center=true);
                    translate([0,0,cover_thickness+sheath_depth+magnet_height+wall_thickness/2])
                        squarish_rpoly(
                            xy=[length - (width - width/taper)-wall_thickness*1.25,
                                width/taper-wall_thickness*1.25],
                            h=cover_thickness,
                            r=corner_radius/1.5, center=true);
                }

                // Cut out the corner so we don't have to worry about a large stem/magnet scraping the sides
                translate([
                -width/2.85,
                -width/2.85,
                body_height/2+top_magnet_height+magnet_wall_thickness+droop_extra-top_magnet_cover_thickness+sheath_length
                ])
                    cube([width/2,width/2,body_height], center=true);
            }
        }
        // cut out slits for the clips
        if (cover_overhang) {
            // Create a gap underneath the clips so they can move freely
            gap_size = plate_thickness/2 - cover_thickness/2;
            translate([
                clip_width,
                0,
                cover_thickness+gap_size/2])
                    cube([
                        clip_width+clip_side_hole_width*2,
                        width*2,
                        gap_size], center=true);
            translate([
                -clip_width,
                width/2,
                cover_thickness+gap_size/2])
                    cube([
                        clip_width+clip_side_hole_width*2,
                        width/2,
                        gap_size], center=true);
            // Cutout holes beside the clips so they can bend (slightly) easier when inserting
            translate([
                clip_width+clip_width/2+clip_side_hole_width/2,
                0,
                cover_thickness/2+travel/2+plate_thickness/2+bridge_thickness])
                    cube([clip_side_hole_width, width*2, travel], center=true);
            translate([
                clip_width-clip_width/2-clip_side_hole_width/2,
                0,
                cover_thickness/2+travel/2+plate_thickness/2+bridge_thickness])
                    cube([clip_side_hole_width, width*2, travel], center=true);
            translate([
                -clip_width-clip_width/2-clip_side_hole_width/2,
                width/2+snap_clip_protrusion-cover_overhang/1.15,
                cover_thickness/2+travel/2+plate_thickness/2+bridge_thickness])
                    cube([clip_side_hole_width, width/2, travel], center=true);
            translate([
                -clip_width+clip_width/2+clip_side_hole_width/2,
                width/2+snap_clip_protrusion-cover_overhang/1.15,
                cover_thickness/2+travel/2+plate_thickness/2+bridge_thickness])
                    cube([clip_side_hole_width, width/2, travel], center=true);
            // Carve out a bit of the bridge that supports the clips so it can break away easier upon first insertion of the switch into the plate
            translate([ // Back side left
                -clip_width,
                width/2-wall_thickness/1.55,
                cover_thickness/2+plate_thickness/2+bridge_thickness/2])
                    cube([
                        clip_width+clip_side_hole_width*2,
                        wall_thickness/3.5,
                        bridge_thickness+0.01], center=true);
            translate([ // Back side right
                clip_width,
                width/2-wall_thickness/1.55,
                cover_thickness/2+plate_thickness/2+bridge_thickness/2])
                    cube([
                        clip_width+clip_side_hole_width*2,
                        wall_thickness/3.5,
                        bridge_thickness+0.01], center=true);
            translate([ // Front side right
                clip_width,
                -width/2+wall_thickness/1.55,
                cover_thickness/2+plate_thickness/2+bridge_thickness/2])
                    cube([
                        clip_width+clip_side_hole_width*2,
                        wall_thickness/3.5,
                        bridge_thickness+0.01], center=true);

            // NOTE (Richard): Switch body is long enough that we need additional clips
            if (length > MAX_SINGLE_KEY_LEN) {
                // gaps under clips
                translate([
                    length/2 - clip_width*2,
                    0,
                    cover_thickness+gap_size/2])
                        cube([
                            clip_width+clip_side_hole_width*2,
                            width*2,
                            gap_size], center=true);
                translate([
                    -length/2 + clip_width*2,
                    width/2,
                    cover_thickness+gap_size/2])
                        cube([
                            clip_width+clip_side_hole_width*2,
                            width/2,
                            gap_size], center=true);
                // gaps on the sides
                translate([
                    length/2 - clip_width*2+clip_width/2+clip_side_hole_width/2,
                    0,
                    cover_thickness/2+travel/2+plate_thickness/2+bridge_thickness])
                        cube([clip_side_hole_width, width*2, travel], center=true);
                translate([
                    length/2 - clip_width*2-clip_width/2-clip_side_hole_width/2,
                    0,
                    cover_thickness/2+travel/2+plate_thickness/2+bridge_thickness])
                        cube([clip_side_hole_width, width*2, travel], center=true);
                translate([
                    -length/2 + clip_width*2-clip_width/2-clip_side_hole_width/2,
                    width/2+snap_clip_protrusion-cover_overhang/1.15,
                    cover_thickness/2+travel/2+plate_thickness/2+bridge_thickness])
                        cube([clip_side_hole_width, width/2, travel], center=true);
                translate([
                    -length/2 + clip_width*2+clip_width/2+clip_side_hole_width/2,
                    width/2+snap_clip_protrusion-cover_overhang/1.15,
                    cover_thickness/2+travel/2+plate_thickness/2+bridge_thickness])
                        cube([clip_side_hole_width, width/2, travel], center=true);
                // carve under bridge
                translate([ // Back side left
                    -(length/2 - clip_width*2),
                    width/2-wall_thickness/1.55,
                    cover_thickness/2+plate_thickness/2+bridge_thickness/2])
                        cube([
                            clip_width+clip_side_hole_width*2,
                            wall_thickness/3.5,
                            bridge_thickness+0.01], center=true);
                translate([ // Back side right
                    length/2 - clip_width*2,
                    width/2-wall_thickness/1.55,
                    cover_thickness/2+plate_thickness/2+bridge_thickness/2])
                        cube([
                            clip_width+clip_side_hole_width*2,
                            wall_thickness/3.5,
                            bridge_thickness+0.01], center=true);
                translate([ // Front side right
                    length/2 - clip_width*2,
                    -width/2+wall_thickness/1.55,
                    cover_thickness/2+plate_thickness/2+bridge_thickness/2])
                        cube([
                            clip_width+clip_side_hole_width*2,
                            wall_thickness/3.5,
                            bridge_thickness+0.01], center=true);
            }
            // Typically on the side with the hole we cannot have a clip at the end
            // but this is possible for spacebars
            if (length > MIN_SPACE_BAR_LEN) {
                // gaps under clips
                translate([
                    -length/2 + clip_width*2,
                    -width/2,
                    cover_thickness+gap_size/2])
                        cube([
                            clip_width+clip_side_hole_width*2,
                            width/2,
                            gap_size], center=true);
                // gaps on sides
                translate([
                    -length/2 + clip_width*2-clip_width/2-clip_side_hole_width/2,
                    -(width/2+snap_clip_protrusion-cover_overhang/1.15),
                    cover_thickness/2+travel/2+plate_thickness/2+bridge_thickness])
                        cube([clip_side_hole_width, width/2, travel], center=true);
                translate([
                    -length/2 + clip_width*2+clip_width/2+clip_side_hole_width/2,
                    -(width/2+snap_clip_protrusion-cover_overhang/1.15),
                    cover_thickness/2+travel/2+plate_thickness/2+bridge_thickness])
                        cube([clip_side_hole_width, width/2, travel], center=true);
                // carve under bridge
                translate([ // Front side right
                    -(length/2 - clip_width*2),
                    -width/2+wall_thickness/1.55,
                    cover_thickness/2+plate_thickness/2+bridge_thickness/2])
                        cube([
                            clip_width+clip_side_hole_width*2,
                            wall_thickness/3.5,
                            bridge_thickness+0.01], center=true);
            }
        }
        // Cutout for the sheath to snap into (has something to do with stem diameter):
        center_adjust = (sheath_height/2-sheath_wall_thickness*1.5)*1.45+stem_tolerance*1.5;
        // NOTE: center_adjust matches how high off the floor the Cherry cross (+) is in stem.scad.  This allows us to accurately position the sheath so that the stem sits dead center.
        rotate([0,0,45])
            translate([-(sheath_height+sheath_tolerance*2)/2+center_adjust,0,0])
                difference() {
                    cube([
                        sheath_height+sheath_tolerance*2,
                        sheath_width+sheath_tolerance*2,
                        body_height], center=true);
                    translate([sheath_height/2,0,0])
                        cube([
                            cover_thickness,
                            sheath_clip_width-sheath_tolerance*2,
                            body_height*2], center=true);
                } // end difference

        // Add the cutout for the sheath + magnet (horizontal)
        if (!sheath_snug_magnet) {
            // Makes room for *just* the magnet (no material wrapping the magnet in the sheath)
            // NOTE: This will need adjustment for a 5 or 6mm magnet (made for 4mm)
            translate([
              // -stem_diameter/4-top_magnet_diameter/1.75,
              // -stem_diameter/4-top_magnet_diameter/1.75,
              -stem_diameter/2-(top_magnet_diameter-magnet_wall_thickness*3)/2.9,
              -stem_diameter/2-(top_magnet_diameter-magnet_wall_thickness*3)/2.9,
              -top_magnet_cover_thickness+droop_extra/2]) {
                  cylinder(
                      d=top_magnet_diameter, // For just magnet
                      h=top_magnet_height*2+magnet_thickness_tolerance+droop_extra,
                      center=true);
              }
        } else {
            fn = sheath_inside_body ? 64 : 8;
            // Makes room for the sheath when it wraps around the outside of the magnet
            translate([
              // -stem_diameter/4-top_magnet_diameter/1.75,
              // -stem_diameter/4-top_magnet_diameter/1.75,
              -stem_diameter/2-(top_magnet_diameter-magnet_wall_thickness*3)/2.9+stem_tolerance,
              -stem_diameter/2-(top_magnet_diameter-magnet_wall_thickness*3)/2.9+stem_tolerance,
              -top_magnet_cover_thickness+droop_extra/2+sheath_length/2]) {
                rotate([0,0,22.5]) cylinder(
                  d=top_magnet_diameter+magnet_wall_thickness*3+sheath_tolerance*2+0.5, // For magnet + sheath holding it
                  h=top_magnet_height*2+magnet_thickness_tolerance+droop_extra+sheath_length,
                  center=true, $fn=fn);
            }
        }
        // Visualize the magnet too
        translate([
          //  -stem_diameter/4-top_magnet_diameter/1.75,
          //  -stem_diameter/4-top_magnet_diameter/1.75,
          -stem_diameter/2-(top_magnet_diameter-magnet_wall_thickness*3)/2.9,
          -stem_diameter/2-(top_magnet_diameter-magnet_wall_thickness*3)/2.9,
          top_magnet_height/2-top_magnet_cover_thickness]) {
            %cylinder(
              d=top_magnet_diameter+magnet_thickness_tolerance,
              h=top_magnet_height,
              center=true);
        }
    } // end difference
    // Add little snap/clip nubs so the switch can "snap" into place (and stay there)
    if (cover_overhang) { // Don't need the clips if doing flush mount
        translate([
            clip_width,
            width/2+snap_clip_protrusion-cover_overhang/1.15,
            cover_thickness+snap_clip_thickness/1.25+plate_thickness])
                rotate([-60,0,0])
                    cube([clip_width, snap_clip_thickness*2, snap_clip_thickness], center=true);
        translate([
            -clip_width,
            width/2+snap_clip_protrusion-cover_overhang/1.15,
            cover_thickness+snap_clip_thickness/1.25+plate_thickness])
                rotate([-60,0,0])
                    cube([clip_width, snap_clip_thickness*2, snap_clip_thickness], center=true);
        translate([
            clip_width,
            -width/2-snap_clip_protrusion+cover_overhang/1.15,
            cover_thickness+snap_clip_thickness/1.25+plate_thickness])
                rotate([60,0,0])
                    cube([clip_width, snap_clip_thickness*2, snap_clip_thickness], center=true);
        if (length > MAX_SINGLE_KEY_LEN) {
            translate([
                length/2 - clip_width*2,
                width/2+snap_clip_protrusion-cover_overhang/1.15,
                cover_thickness+snap_clip_thickness/1.25+plate_thickness])
                    rotate([-60,0,0])
                        cube([clip_width, snap_clip_thickness*2, snap_clip_thickness], center=true);
            translate([
                -(length/2 - clip_width*2),
                width/2+snap_clip_protrusion-cover_overhang/1.15,
                cover_thickness+snap_clip_thickness/1.25+plate_thickness])
                    rotate([-60,0,0])
                        cube([clip_width, snap_clip_thickness*2, snap_clip_thickness], center=true);
            translate([
                length/2 - clip_width*2,
                -width/2-snap_clip_protrusion+cover_overhang/1.15,
                cover_thickness+snap_clip_thickness/1.25+plate_thickness])
                    rotate([60,0,0])
                        cube([clip_width, snap_clip_thickness*2, snap_clip_thickness], center=true);
        }
        if (length > MIN_SPACE_BAR_LEN) {
            translate([
                -(length/2 - clip_width*2),
                -width/2-snap_clip_protrusion+cover_overhang/1.15,
                cover_thickness+snap_clip_thickness/1.25+plate_thickness])
                    rotate([60,0,0])
                        cube([clip_width, snap_clip_thickness*2, snap_clip_thickness], center=true);
        }        
    }
    // TEMP: Uncomment this to visualize the cover plate:
//    %translate([0,0,plate_thickness/2+cover_thickness])
//        cube([length+2, width+2, plate_thickness], center=true);
}

switch_body(14, 14, 2);