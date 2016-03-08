#!/usr/bin/env python3
import fileinput
from subprocess import call
from sys import argv
from colorsys import rgb_to_hls
from colorsys import hls_to_rgb
from getpass import getuser
from random import randint
from os.path import isfile

homedir = "/home/" + getuser()
walldir = homedir + "/.wallpapers/"


def read_color_in_line( xres_file ):
    xres_file = "." + xres_file + ".Xres"
    try:
        f = open( walldir + xres_file, "r" )
    except IOError as err:
        print( err )
        print( err.args )
        print( err.filename )
        return "4A838F"
    line_get = randint( 1, 15 )
    xres_list = [ line for line in f ]
    color = xres_list[ line_get ]
    color = color.split( " ", len( color ) )
    color = color[1]
    color = color.strip( '#' )
    color = color.strip( '\n' )
    return color

def read_color_0( xres_file ):
    xres_file = "." + xres_file + ".Xres"
    try:
        f = open( walldir + xres_file, "r" )
    except IOError as err:
        print( err )
        print( err.args )
        print( err.filename )
        return "121212"
    xres_list = [ line for line in f ]
    color = xres_list[ 0 ]
    color = color.split( " ", len( color ) )
    color = color[1]
    color = color.strip( '#' )
    color = color.strip( '\n' )
    return color

def reduce_brightness( hex_string, reduce_lvl ):
    rgb = list( int(hex_string[i:i+2], 16) for i in ( 0, 2, 4 ) )
    hsl = rgb_to_hls( rgb[0], rgb[1], rgb[2] )
    hsl = list(hsl)
    hsl[1] = hsl[1] - reduce_lvl
    rgb = hls_to_rgb( hsl[0], hsl[1], hsl[2] )
    rgb_int = []
    for elem in rgb:
        rgb_int.append( int(elem) )
    rgb_int = tuple( rgb_int )
    hex_result = '%02x%02x%02x' % rgb_int
    return hex_result

def add_brightness( hex_string, reduce_lvl ):
    rgb = list( int(hex_string[i:i+2], 16) for i in ( 0, 2, 4 ) )
    hsl = rgb_to_hls( rgb[0], rgb[1], rgb[2] )
    hsl = list(hsl)
    hsl[1] = hsl[1] + reduce_lvl
    rgb = hls_to_rgb( hsl[0], hsl[1], hsl[2] )
    rgb_int = []
    for elem in rgb:
        rgb_int.append( int(elem) )
    rgb_int = tuple( rgb_int )
    hex_result = '%02x%02x%02x' % rgb_int
    return hex_result

def change_colors_ob( active, inactive ):
    backupdir = homedir + "/.themes/colorbamboo/openbox-3/themerc.base"
    realdir = homedir + "/.themes/colorbamboo/openbox-3/themerc"
    if( isfile( backupdir ) ):
        call( ["cp", backupdir, realdir] )
        with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
            for line in file:
                print( line.replace( "4A838F", active ), end='' )
        with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
            for line in file:
                print( line.replace( "2C4448", inactive ), end='' )
    backupdir = homedir + "/.themes/colorbamboo_nb/openbox-3/themerc.base"
    realdir = homedir + "/.themes/colorbamboo_nb/openbox-3/themerc"
    if( isfile( backupdir ) ):
        call( ["cp", backupdir, realdir] )
        with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
            for line in file:
                print( line.replace( "4A838F", active ), end='' )
        with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
            for line in file:
                print( line.replace( "2C4448", inactive ), end='' )
    if( isfile(homedir + "/.config/openbox/menu.xml") ):
        call( ["openbox", "--reconfigure"] )
    else:
        print( "NO OPENBOX INSTALL!" )

def change_colors_icons( active, inactive, glyph ):
    backupdir = homedir + "/.icons/flattrcolor/scripts/replace_folder_file.sh.base"
    realdir = homedir + "/.icons/flattrcolor/scripts/replace_folder_file.sh"
    xsl_file = homedir + "/.icons/flattrcolor/scripts/change_folder_colors.xslt"
    executable = homedir + "/.icons/flattrcolor/scripts/replace_script.sh"
    if( isfile( backupdir ) ):
        file_current_glyph = open( realdir, "r" )
        current_glyph = []
        for line in file_current_glyph:
            if( "New" in line ):
                current_glyph.append( line )
                break
        current_glyph = current_glyph.pop()
        current_glyph = current_glyph.strip( "\n" )
        current_glyph = current_glyph.split( "=" )
        current_glyph = current_glyph.pop()
        file_current_glyph.close()
        print( "CURRENT GLYPH: " + current_glyph )

        call( ["cp", backupdir, realdir] )
        with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
            for line in file:
                print( line.replace( "34495d", inactive ), end='' )
        with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
            for line in file:
                print( line.replace( "1abc9c", active ), end='' )
        with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
            for line in file:
                print( line.replace( "l=304050", "l=" + current_glyph ), end='' )
        with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
            for line in file:
                print( line.replace( "w=304050", "w=" + glyph ), end='' )
        call( executable, shell=True )

def change_colors_tint2( active, inactive ):
    backupdir = homedir + "/.config/tint2/tint2rc.base"
    realdir = homedir + "/.config/tint2/tint2rc"
    if( isfile( backupdir ) ):
        call( ["cp", backupdir, realdir] )
        with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
            for line in file:
                print( line.replace( "4A838F".lower(), active ), end='' )
        with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
            for line in file:
                print( line.replace( "2C4448".lower(), inactive ), end='' )
        call( [ "killall", "-SIGUSR1", "tint2" ] )

def change_colors_gtk2( active, inactive, base_0, base_1 ):
    backupdir = homedir + "/.themes/FlatColor/gtk-2.0/gtkrc.base"
    realdir = homedir + "/.themes/FlatColor/gtk-2.0/gtkrc"
    base_0_darker = reduce_brightness( base_0, 5 )
    if( isfile( backupdir ) ):
        call( ["cp", backupdir, realdir] )
        with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
            for line in file:
                print( line.replace( "4A838F", active ), end='' )
        with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
            for line in file:
                print( line.replace( "121212", base_0 ), end='' )
        with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
            for line in file:
                print( line.replace( "202020", base_1 ), end='' )
        with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
            for line in file:
                print( line.replace( "090909", base_0_darker ), end='' )

def change_colors_gtk3( active, inactive, base_0, base_1 ):
    backupdir = homedir + "/.themes/FlatColor/gtk-3.0/gtk.css.base"
    realdir = homedir + "/.themes/FlatColor/gtk-3.0/gtk.css"
    if( isfile( backupdir ) ):
        call( ["cp", backupdir, realdir] )
        with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
            for line in file:
                print( line.replace( "4A838F".lower(), active ), end='' )
        with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
            for line in file:
                print( line.replace( "121212", base_0 ), end='' )
        with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
            for line in file:
                print( line.replace( "202020", base_1 ), end='' )

def execute_gcolorchange( image_name ):
    base_color = read_color_in_line( image_name )
    base_color_0 = read_color_0( image_name )
    base_color_1 = add_brightness( base_color_0, 10 )
    if( base_color == "4A838F" ):
        base_redux = 0
        inact_redux = 50
    else:
        base_redux = 30
        inact_redux = 75
    active = reduce_brightness( base_color, base_redux )
    inactive = reduce_brightness( base_color, inact_redux )
    fg_icon = base_color
    bg_icon = reduce_brightness( base_color, 40 )
    glyph = reduce_brightness( base_color, 70 )
    print( "FG: " + active )
    print( "BG: " + inactive )
    print( "CHANGING::OPENBOX" )
    change_colors_ob( active, inactive )
    print( "CHANGING::TINT2" )
    change_colors_tint2( active, inactive )
    print( "CHANGING::GTK" )
    change_colors_gtk2( active, inactive, base_color_0, base_color_1 )
    change_colors_gtk3( active, inactive, base_color_0, base_color_1 )
    print( "CHANGING::ICONS" )
    change_colors_icons( fg_icon, bg_icon, glyph )
    print( "SUCCESS" )

if __name__ == "__main__":
    image_name = argv[1]
    execute_gcolorchange( image_name )
