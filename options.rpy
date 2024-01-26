## This file contains options that can be changed to customize your game.
##
## Lines beginning with two '#' marks are comments, and you shouldn't uncomment
## them. Lines beginning with a single '#' mark are commented-out code, and you
## may want to uncomment them when appropriate.


## Basics ######################################################################

## A human-readable name of the game. This is used to set the default window
## title, and shows up in the interface and error reports.
##
## The _() surrounding the string marks it as eligible for translation.

define config.name = _("A Day In The Life")


## Determines if the title given above is shown on the main menu screen. Set
## this to False to hide the title.

define gui.show_name = True


## The version of the game.

define config.version = "1.0"


## Text that is placed on the game's about screen. Place the text between the
## triple-quotes, and leave a blank line between paragraphs.

define gui.about = ("""
GUI features for PC have all been painstakingly edited, recoloured, redrawn, or fully recreated by Valerie. Please acknowledge and appreciate her efforts.

Music from Uppbeat:
{a=https://uppbeat.io/t/yokonap/airplane-mode}Main Menu{/a} (Airplane Mode, Yokonap)
{a=https://uppbeat.io/t/ra/cold-brew}Main Game{/a} (Cold Brew, RA)

Sound effects:
{a=https://freesound.org/people/kwahmah_02/sounds/250629/}Alarm Clock{/a} (kwahmah_02)
{a=https://pixabay.com/sound-effects/analog-appliance-button-10-185285/}Button click SFX{/a} (floraphonic)
{a=https://pixabay.com/sound-effects/light-switch-81967/}Light switch SFX{/a} (Pixabay)
{a=https://pixabay.com/sound-effects/cellphone-ringing-6475/}Phone ringing SFX{/a} (Pixabay)

Images:
{a=https://www.geoguessr.com/}GeoGuessr screenshots{/a}
{a=https://hips.hearstapps.com/hmg-prod/images/ghk010121homefeature-008-1671137680.png}Bedroom{/a}
{a=https://cut2size.ca/uploads/system_files/small_kitchen_layout_ideas.jpeg}Kitchen{/a}
{a=https://cars.usnews.com/cars-trucks/advice/brands-with-the-nicest-interiors}Car{/a}
{a=https://www.sercoconstruction.ca/projects/kingston-secondary-school-module-vanier}Library and atrium backgrounds{/a}
{a=https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.limestone.on.ca%2Fboard%2Fnew_school__kingston_secondary_school&psig=AOvVaw0On-BHkVxdP2DI26Jgtnpw&ust=1706234852884000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCPiZyqa694MDFQAAAAAdAAAAABAD}School building background{/a}
{a=https://globalnews.ca/news/7299049/kingston-secondary-schools-octomester/}History classroom background{/a}
{a=https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.teachhub.com%2Fclassroom-management%2F2019%2F05%2Fclassroom-management-for-an-effective-learning-environment%2F&psig=AOvVaw0WypgxfaZN4FgRE6jH3hhI&ust=1706235013973000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCMiO7PG694MDFQAAAAAdAAAAABAD}Science classroom background{/a}
{a=https://www.primarisreit.com/system/attachments/1062/original/_DSC3717.jpg?1619722057}Mall{/a}
{a=https://www.greenbiz.com/sites/default/files/styles/og_image_1200x630/public/2020-10/chicago_citybus_stock.jpg?itok=L-k33qIv}City bus{/a}
{a=https://upload.wikimedia.org/wikipedia/commons/9/9e/Interior_school_bus.jpg}School bus{/a}
{a=https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.cprcertified.com%2Fblog%2Fstuck-outside-in-winter-first-aid-tips-for-cold-weather-survival&psig=AOvVaw2zwA6jUm1z5cATw6L9xepC&ust=1706324647284000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCKDy7-mI-oMDFQAAAAAdAAAAABAI}Outside winter{/a}
{a=https://www.google.com/url?sa=i&url=https%3A%2F%2Fca.linkedin.com%2Fin%2Fluke-delva-b914aa75&psig=AOvVaw197kWXUmksl8q1gu29F8Q4&ust=1706325790647000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCNipkYeN-oMDFQAAAAAdAAAAABAD}Luke Delva{/a}
{a=https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.hgtv.com%2Fdesign%2Frooms%2Fliving-and-dining-rooms%2F15-almost-free-living-room-updates-pictures&psig=AOvVaw0HJzEV_ZQcg7EIAFGgOoKr&ust=1706325818574000&source=images&cd=vfe&opi=89978449&ved=0CBMQjRxqFwoTCJDatZSN-oMDFQAAAAAdAAAAABAE}Living room{/a}
{a=https://ifaketextmessage.com/}Text conversations{/a}

""")


## A short name for the game used for executables and directories in the built
## distribution. This must be ASCII-only, and must not contain spaces, colons,
## or semicolons.

define build.name = "A_Day_In_The_Life"


## Sounds and music ############################################################

## These three variables control, among other things, which mixers are shown
## to the player by default. Setting one of these to False will hide the
## appropriate mixer.

define config.has_sound = True
define config.has_music = True
define config.has_voice = False


## To allow the user to play a test sound on the sound or voice channel,
## uncomment a line below and use it to set a sample sound to play.

# define config.sample_sound = "sample-sound.ogg"
# define config.sample_voice = "sample-voice.ogg"


## Uncomment the following line to set an audio file that will be played while
## the player is at the main menu. This file will continue playing into the
## game, until it is stopped or another file is played.

define config.main_menu_music = "airplanemode.mp3"

## Transitions #################################################################
##
## These variables set transitions that are used when certain events occur.
## Each variable should be set to a transition, or None to indicate that no
## transition should be used.

## Entering or exiting the game menu.
## Edited by Valerie from dissolve into fade
define config.enter_transition = fade
define config.exit_transition = fade


## Between screens of the game menu.

define config.intra_transition = fade


## A transition that is used after a game has been loaded.

define config.after_load_transition = None


## Used when entering the main menu after the game has ended.

define config.end_game_transition = None


## A variable to set the transition used when the game starts does not exist.
## Instead, use a with statement after showing the initial scene.


## Window management ###########################################################
##
## This controls when the dialogue window is displayed. If "show", it is always
## displayed. If "hide", it is only displayed when dialogue is present. If
## "auto", the window is hidden before scene statements and shown again once
## dialogue is displayed.
##
## After the game has started, this can be changed with the "window show",
## "window hide", and "window auto" statements.

define config.window = "auto"


## Transitions used to show and hide the dialogue window

define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)


## Preference defaults #########################################################

## Controls the default text speed. The default, 0, is infinite, while any other
## number is the number of characters per second to type out.
## Edited
default preferences.text_cps = 75


## The default auto-forward delay. Larger numbers lead to longer waits, with 0
## to 30 being the valid range.

default preferences.afm_time = 15


## Save directory ##############################################################
##
## Controls the platform-specific place Ren'Py will place the save files for
## this game. The save files will be placed in:
##
## Windows: %APPDATA\RenPy\<config.save_directory>
##
## Macintosh: $HOME/Library/RenPy/<config.save_directory>
##
## Linux: $HOME/.renpy/<config.save_directory>
##
## This generally should not be changed, and if it is, should always be a
## literal string, not an expression.

define config.save_directory = "LappiMorganAcademy-1705266869"


## Icon ########################################################################
##
## The icon displayed on the taskbar or dock.

define config.window_icon = "gui/window_icon.png"


## Build configuration #########################################################
##
## This section controls how Ren'Py turns your project into distribution files.

init python:

    ## The following functions take file patterns. File patterns are case-
    ## insensitive, and matched against the path relative to the base directory,
    ## with and without a leading /. If multiple patterns match, the first is
    ## used.
    ##
    ## In a pattern:
    ##
    ## / is the directory separator.
    ##
    ## * matches all characters, except the directory separator.
    ##
    ## ** matches all characters, including the directory separator.
    ##
    ## For example, "*.txt" matches txt files in the base directory, "game/
    ## **.ogg" matches ogg files in the game directory or any of its
    ## subdirectories, and "**.psd" matches psd files anywhere in the project.

    ## Classify files as None to exclude them from the built distributions.

    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)

    ## To archive files, classify them as 'archive'.

    # build.classify('game/**.png', 'archive')
    # build.classify('game/**.jpg', 'archive')

    ## Files matching documentation patterns are duplicated in a mac app build,
    ## so they appear in both the app and the zip file.

    build.documentation('*.html')
    build.documentation('*.txt')


## A Google Play license key is required to perform in-app purchases. It can be
## found in the Google Play developer console, under "Monetize" > "Monetization
## Setup" > "Licensing".

# define build.google_play_key = "..."


## The username and project name associated with an itch.io project, separated
## by a slash.

# define build.itch_project = "renpytom/test-project"
