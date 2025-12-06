"""
This is a silly but useful tool to import stuff automatically in renpy, mostly designed to be 
customizable in most of the cases and save you some time renaming and moving files/folder 
in your game, horiented for large game with a bunch of files... 

this is mostly a CLI tool, but it can also be used as an external lib... most of the times

check each function docs and study their behavior as you want, it's not like I can't do much about it

just hope you like it and give me a star in [github](https://github.com/Z3R0GT/renpy-auto-importer)... and since you are there, follow me!

<br><br>

<center>Tool originally made by Z3R0_GT, in representation of ScoStudios for 
RITF (Roses In The Flames&trade;), made by DragonForge Studios LLC. </center>

# How to use (easy tutorial)

## Setup

1. download the tool and place in the folder relative to `./game` (or basically in your renpy game's proyect)
2. ensure you have python between 3.13 and 3.14 (since one of our core functions only exits in 3.14 and low versions
but it was marked for removal in 3.15, and its alternative sucks) 
3. install [typing_extensions], since it one of our main [dependencies](#dependencies)
4. once installed, you are ready to go the next section

## Basic commands

if you follow the [folder structure](#folder-structure), you should only use

```shell
$ python importer.py --set-game ./game --enable-common
```

otherwise, you should check the [commands](#commands) section, or just use 

```shell
$ python importer.py -h
```

to get more info about commands, since the [commands](#commands) only covers case-of-use, but it doesn't actually explains why 
the commands, we consider their names are very explicit

# Details

__Compilation__ (recommend for windows): auto-py-to-exe >= 2.45.1

__Python__: 

> Originally 3.13.2 (Microsoft store)

> This version was created with 3.14.0t (yes, free threads)

__Code structure__:

> Main imports

> Metadata related

> Enums

> Language service

> Secundary / optional imports

> Constants

> Functions

> > Utils

> > Path realted

> > Specifics 1

> > Writers

> > Specifics 2 (now it's personal)

> > > Scanners

> > Imports

> > Entry point

__Code__: single file

__Docummentation__: [pydoc3] >= 0.11.6

# Depencencies

> Third-party libs

| name                | version     | is optional? | why?                                                           |
|---------------------|:-----------:|:------------:|----------------------------------------------------------------|
| [colorama]          | >= 0.4.6    |     ✅      | just to get colors to the console                              |
| [pillow]            | >= 12.0.0   |     ✅      | to create side images                                          |
| [platformdirs]      | == 4.5.0    |     ✅      | to get the equivalent to appdata folder in many OS as possible |
| [pyminizip]         | >= 0.2.6    |     ✅      | to create zip file using a single function                     |
| [tqdm]              | >= 4.67.1   |     ✅      | same as colorama, but for lists                                |
| [typing_extensions] | >= 4.15.0   |     ❌      | typing..........                                               |
| [Whoosh]            | >= 2.7.4    |     ✅      | weight light search engine                                     |
| [pydoc3]            | >= 0.11.6   |     ✅      | to create this doc                                             |

> Python build-in (from 3.13.2 to 3.14.0t)

| name         | version    |
|--------------|------------|
| sys          | (build-in) |
| logging      | (build-in) |
| warnings     | (build-in) |
| plataform    | (build-in) |
| os           | (build-in) |
| enum         | (build-in) |
| collections  | (build-in) |
| locale       | (build-in) |
| argparse     | (build-in) |
| shutil       | (build-in) |
| functools    | (build-in) |
| pathlib      | (build-in) |
| json         | (build-in) |
| configparser | (build-in) |

# Naming

Due to the design of the following code, the following variables are designated for naming and/or modifying the structure.
This was designed to be "portable" and based on the "black box" concept (you have an input and an output, but you don't know what happens inside).
Therefore, any function must follow the following "rules," and there are exceptions to these.

.. note::
    Every function or class must specify the expected data type and the returned data type, always

> - ### **GET** Functions

>> These functions should be as small as possible. If two or more of these functions are related in their operation, then they should share as much size as possible. Generally, they should get:

>> ``get_{kind}_{what it does}_{where or how}``

>> Generally, a getter function should only have a minimum of two of these parts and no more.
Exceptions to this rule are functions whose purpose is very simple or whose operation is literally defined by the function's name.

> - ### **MKR** Functions

>> These are functions whose purpose is to "create" something within the machine, whether it's manipulating files or directories. They generally have 2 or 3 words (maximum-minimum) following the structure below:

>> ``mkr_{what}_{type}``

> - ### Functions **ADD/DEL/RM/SAVE/LOAD**

>> These are actually extra functions whose names cannot exceed two words and must be specific to their function.
The documentation for these functions MUST be shorter and simpler, as they are extra.

> - ### **IMPORT** Functions

>> most of the time, these function are mean to be shortcuts for all other functions, calling
of these is the equivalent to do a proccess, since behind, these function automatically fullfill 
all possible requirements for a procces to be made

> - ### **SCAN** Functions

>> basically, the only job of this kind of functions is to scan something, search for patterns, and 
return what they found, their structure consists of:

>> ``scan_{what or type}_{where or how}``

>> just like [get functions](#get-functions), there might be exception to this rule

> - ### **WRITE** Functions

>> these function can't do much, other than recollect data and print/save into a file, most of the times
their objective should gather the requiriments for other functions be done and check their viability before perform
any procces

> - ### Other Functions

>> Most functions are already covered. You can add more if you wish, but you must update this header to keep the documentation current.

# Folder structure

First of all, this tool was designed to be effort-less for beginers to use, to this might be something we would like game that use this tool to implement
as their own folder structure

so, renpy basically have all their game in the folder with same name (./game), which we call `game data`, where all __chapters__ (renpy files were the story
takes place) and assets are placed, we believe in a folder structure similar to some games, where:

every asset will go to an __assets__ folder (`DEFAULT_RESOURCE_PATH`), where all of them are saved in different folders, such as 

1. audio (`DEFAULT_PATH_SOUND`)
2. video (`DEFAULT_PATH_VIDEO`)
3. images (`DEFAULT_PATH_IMAGE`)
4. fonts
5. etc

if you do something like

```
game/
|   |
|   | assets/
|   |       |
|   |       | audio/
|   |       |      | folder A
|   |       |      | folder B
|   |       |      | folder C
|   |       |      | my_song.mp3
|   |       |      | my_song.wav
|   |       | video/
|   |       |      | folder A
|   |       |      | folder B
|   |       |      | folder C
|   |       |      | my_video.mp4
|   |       |      | my_song.ogv
```

the tool will work automatically to import the files for you, you don't need to specify `--set-audio` or `--set-video` for the path, since (as mention before), 
they are already declared (you can change them later if ya want, but that might require you to change the script)

**but**, there's a detail about background and sprites, due how they are organized and how different they are between games, 
we separate them into their own commands (`--set-sprite` and `--set-background` to be precise), yet, the same can apply, given us 
something like:

```
game/
|   |
|   | assets/
|   |       |
|   |       | images/
|   |       |      | characters/
|   |       |      |           |
|   |       |      |           | character folder A
|   |       |      |           | character folder B
|   |       |      |           | character folder C
|   |       |      | background/
|   |       |      |           |
|   |       |      |           | background folder A
|   |       |      |           | background folder B
|   |       |      |           | background folder C
```

ended up being something like this when using the whole folder structure

```
game/
|   |
|   | assets/
|   |       |
|   |       | audio/
|   |       |      | folder A
|   |       |      | folder B
|   |       |      | folder C
|   |       |      | my_song.mp3
|   |       |      | my_song.wav
|   |       | video/
|   |       |      | folder A
|   |       |      | folder B
|   |       |      | folder C
|   |       |      | my_video.mp4
|   |       |      | my_song.ogv
|   |       | images/
|   |       |      | characters/
|   |       |      |           |
|   |       |      |           | character folder A /
|   |       |      |           |                    |
|   |       |      |           |                    | image A.png
|   |       |      |           |                    | image B.png
|   |       |      |           | character folder B
|   |       |      |           | character folder C
|   |       |      | background/
|   |       |      |           |
|   |       |      |           | background folder A /
|   |       |      |           |                     |
|   |       |      |           |                     | image A.png
|   |       |      |           |                     | image B.png
|   |       |      |           | background folder B
|   |       |      |           | background folder C
|   |       |fonts /
|   |       |      | font A.ttf
|   |       |      | font B.ttf
|   |       |      | font C.ttf
```

and so, basically, using a structure like `./game/assets`, where `./game` is our setted game data folder (using `--set-game`) will
make this whole procces more easy to use and for you even more organized if you are starting....

yet, if your proyect already have certain structure, you might consider modify `DEFAULT_RESOURCE_PATH`, `DEFAULT_PATH_VIDEO`,
`DEFAULT_PATH_SOUND` and `DEFAULT_PATH_IMAGE` to make the tool do something similar to the procces describe adove and make it more 
automated, or just use the `--set-[something]` commands to indicate that manually, it's up to you

# Commands

.. note::
    better use `-h` or `--help` to get the full explanation of each command

```shell
$ python importer.py -h
```

Cases
--------
--------

<br>
- Case 1: I want to use custom folders due how my proyect is structured

```shell
$ python importer.py -s-ass ./game -s-sprite ./game/image/sprites -s-background ./game/backgrounds --enable-common
```

here we are using `-s-sprite` and `-s-background` to set manually their folders, the same could be using the audio or video variants of `-s-[something]` command

and don't forget about the `--enable-common` to create the common files

<br>
- Case 2: I want to create side images, but no common files

```shell
$ python importer.py -s-ass ./game -s-sprite ./game/image/sprites -s-background ./game/backgrounds --enable-sides
```

and note that if you use both, `--enable-common` and `--enable-sides` this will first create the sides images and then create common file

<br>
- Case 3: I want to rename some file and create common files after that

```shell
$ python importer.py -s-ass ./game -s-sprite ./game/image/sprites -s-background ./game/backgrounds --enable-common --enable-renamer
```

before even create the common file, the tool will enter into a simple interface asking you to provide the names, then select an option and
confirm a new name for the file, once done, this will change **ALL** part where this image was used, this include audio, video, images, backgrounds, side variants and more!

Once done, it will create the common file, even if you don't enable `--enable-common`, this is because once the file is renamed, there's no way for renpy be sure
if this change was mode, so we really need that change be done, either if it's needed or not, so we make sure the changes are applied

# Error codes

Basically, if the tool is executed as a CLI (Command Line Interface), these commands will
be what it will return being:

- 0: Everything is good
- 1: missing required lib/dependency
- 2: incorrect python version
- 3: unkwon error

# Changelog

### 17/02/2025
- added more formats
- most of the code is documented and the tool is mostly funcionable
- almost production version

### 10/03/2025
- added progress bars
- added new commands 
- added new encryption functions
- added some eastern eggs
- fixed plataform dependencies and compatibility
- fixed minor bugs during compilation phase
- improve JSON import system and templates
- improve arguments parse function
- new search and import system
- code formatted under "black" formatting
- finish docummention

### 05/12/2025

- added multiplataform support
- added a better logging system
- added new functions and template system
- added more validations about paths during the whole creation
- added a better configuration file
- added some self-made alternatives to some third party [dependencies](#depencencies)
- added enums to represent constant data within the tool
- added even more docs and external links for more info
- changed the `frame` and `handler` function to represent what the actual flow is
- changed the way the tool flow works
- changed the file structure 
- changed the common.rpy workflow to make it more clear and stable
- improved language system (it still needs some minor improments, but it's the final version)
- improved importer and side generation system
- fixed some tricks to make `tqdm` works as expected
- fixed minor bugs due how side images were originally planned
- fixed some arguments bugs 
- deleted all eastern eggs (for now)
- finally the searcher feature works properly (yet with some bugs due how the path is now handle)

hope this maskes sence XD

[colorama]: https://pypi.org/project/colorama/
[pillow]: https://pypi.org/project/pillow/
[platformdirs]: https://pypi.org/project/platformdirs/
[pyminizip]: https://pypi.org/project/pyminizip/
[tqdm]: https://pypi.org/project/tqdm/
[typing_extensions]: https://pypi.org/project/typing-extensions/
[Whoosh]: https://pypi.org/project/Whoosh/
[pydoc3]: https://pypi.org/project/pdoc3/
"""

# error code
# 1 -> mising important lib
# 2 -> incorrect version
# 3 -> unkwon error
########################################################
#
# Imports general zone
#
########################################################
import sys
import logging
import warnings
from platform import system
from os import listdir, getcwd, remove, rename

# __all__ = [] #TODO: keep this updated
__pdoc__ = {}
########################################################
#
# Meta zone
#
########################################################
__version__: str = "1.0.5.0"
"""
The actual tool's version
"""
__return__: int = 0
"""
Error code, which also determine the log message once the tool has ended using `__return_text__` 
"""
__return_text__: list[str] = [
    "completed",
    "missing library, check the logs",
    "you have an unsupported python version",
    "Unkwon error, check the logs",
]
"""
Error text used within `__return__` (a little trick if ya ask me)
"""
__product__: str = "importer"
"""
the product/tool name
"""
__author__: str | list[str] = "Z3R0_GT"
"""
the author(s) that made this possible
"""
__is_main__: bool = __name__ == "__main__"
"""
represent if the tool is being used as main or not
"""
__can_edit__ = True
"""
determine if the tool can create/edit/delete files (the last layer of security so to speak)
"""
########################################################
#
# Logger zone
#
########################################################
FORMAT: str = (
    "%(asctime)s <%(name)s> in %(funcName)s launched %(levelname)s with: %(message)s"
)
"""
The format used by the logger `logger`
"""
logger: logging.Logger = logging.getLogger(__name__ if not __is_main__ else "import.py")
"""
the logger, the files will be saved within the same level as where the tool is, this might be called importer.log
"""
logging.basicConfig(
    filename="importer.log", level=logging.INFO, format=FORMAT, filemode="w"
)

if __is_main__:
    logger.info("Program started")

# yeah.... 3.15 is not supported cuz locale.getdefaultlocale was marked as 'future removal' for that version and
# the code needs the funtion to get system's language code (its alternay provide the entire name, we need just the RFC1766 code)
if sys.version_info >= (3, 15):
    __return__ = 2
    logger.fatal(
        "The python version used is actually unsupported and shouldn't use it due some problems we have at the moment"
    )
    if __is_main__:
        raise Exception(
            "The python version used actually unsupported due a library incompatibility"
        )

from enum import StrEnum
from collections import namedtuple

ArgumentsGiven = namedtuple(
    "ArgumentsGiven",
    [
        "game",
        "audio",
        "video",
        "sprite",
        "background",
        "can_generate_side",
        "can_generate_common",
        "use_renamer",
        "use_cipher_zone",
        "can_generate_zip",
    ],
)
__pdoc__[
    "ArgumentsGiven"
] = """
A namedtuple that is used only when the tool is being used as `__main__`, which basically represents certain options, in what paths
we refer, such as `ArgumentsGiven.game`, `ArgumentsGiven.audio`, `ArgumentsGiven.video`, `ArgumentsGiven.sprite`, `ArgumentsGiven.background` refers,

we recomend your proyect be structurered just like [folder structure] suggest, otherwise, you might ended up using some [commands] or all the commands,
but you can customize their behavior changing manually `DEFAULT_RESOURCE_PATH` (which comes after [proyect]/game) and their respective field (`DEFAULT_PATH_VIDEO`, `DEFAULT_PATH_SOUND`, `DEFAULT_PATH_IMAGE`)

.. tip::
    an example of how the object is builded can be found in [commands] section, yet, it's important to check [folder structure] for more info
    about why this feature and how critical this one could be
    
[folder structure]: #folder-structure
[commands]: #commands

"""
__pdoc__[
    "ArgumentsGiven.game"
] = """
The data folder (mostly where __[project]/game__ in your renpy folder), this must be a valid folder/path to be used!
"""
__pdoc__[
    "ArgumentsGiven.audio"
] = """
The audio folder (mostly where __[project]/game/audio__ in your renpy folder), this must be a valid folder/path to be used!
"""
__pdoc__[
    "ArgumentsGiven.video"
] = """
The video folder (this is depends if your game supports video or not, this might be in __[proyect]/game/video__, otherwise, always check [folder structure] section for more info), this must be a valid folder/path to be used!

[folder structure]: #folder-structure
"""
__pdoc__[
    "ArgumentsGiven.sprite"
] = """
Just like `ArgumentsGiven.game`, but for characters' sprites, in most renpy proyects this is more custom that you might expect, check [folder structure] section for suggestions

[folder structure]: #folder-structure
"""
__pdoc__[
    "ArgumentsGiven.background"
] = """
Just like `ArgumentsGiven.game`, but for backgrounds' sprites, in most renpy proyects this is more custom that you might expect, check [folder structure] section for suggestions

[folder structure]: #folder-structure
"""
__pdoc__[
    "ArgumentsGiven.can_generate_side"
] = """
Indicate if side images can be generated
"""
__pdoc__[
    "ArgumentsGiven.can_generate_common"
] = """
Indicate if common files can be generated
"""
__pdoc__[
    "ArgumentsGiven.use_renamer"
] = """
Indicate if the renamer process can/will be used
"""
__pdoc__[
    "ArgumentsGiven.use_cipher_zone"
] = """
Indicate if cipher system will be used, mostly this requires a custom SDK be made adn this will literally broke all your files if used
"""
__pdoc__[
    "ArgumentsGiven.can_generate_zip"
] = """
Indicate if zip/compression files can be generated
"""
# use_cipher_zone
# NOTE: this import is here cuz the section 'Imports specifc zone' is after some code that needs this function working
# We ignore 'locale.getdefaultlocale' warning
warnings.filterwarnings("ignore", ".*is deprecated and slated for removal in.*")
try:
    from locale import getdefaultlocale
except ImportError:

    def getdefaultlocale() -> tuple:
        return ("en", 0)


from argparse import ArgumentParser
from shutil import rmtree


from functools import singledispatch

from pathlib import Path
from json import load, loads, dumps
from configparser import ConfigParser

########################################################
#
# Enums zone
#
########################################################


class ImageConfigHead(StrEnum):
    """A silly enum that configure how the file `RequiredFiles.INFO` behave and their headers"""

    SIDE = "side"
    """header for side configurations
    """
    SCALE = "scale"
    """header for scale configurations
    """


class ImageConfigValue(StrEnum):
    """A silly enum that configure the name for each field within `ImageConfigHead` and `RequiredFiles.INFO` file"""

    SIZE = "size"
    """configure the size
    """
    SQUARE = "square"
    """configure the square/frame for side images (when created)
    """
    DIMENSION = "dimension"
    """mostly, this configure the target-screen dimension (1920x1080), this is moslty used by scale functions
    """
    KEYS = "keys"
    """configure animation keys when scanning for files
    """
    REPEAT = "repeat"
    """configure if something must be repeated (this mostly is used by a different procces, like template)
    """


class FeaturesKeywords(StrEnum):
    """A silly enum that saves the feature that this tool have (mostly depends if ya have some of all dependencies)"""

    ZIP_COMPRESSION = "z"
    """Only exits if ya have [pyminizip] installed 
    
    
    [pyminizip]: https://pypi.org/project/pyminizip/
    """
    PRETTY_CONSOLE = "t"
    """Only exits if ya have [tqdm] installed
    
    [tqdm]: https://pypi.org/project/tqdm/
    """
    IMAGE_CREATION = "i"
    """Only exits if ya have [PIL/Pillow] installed
    
    [PIL/Pillow]: https://pypi.org/project/pillow/
    """
    RENAMING_PROCESS = "s"
    """This feature might be easy to make as a buildin, but due how difficult it is, for it's left only if ya have [whoosh] installed
    
    .. note::
        this is temporary 'till we make the actual implementation, for now, it's limited just like `FeaturesKeywords.IMAGE_CREATION` or `FeaturesKeywords.ZIP_COMPRESSION`
    
    [whoosh]: https://pypi.org/project/Whoosh/
    """
    SIDE_GENERATION = "ms"
    """This feature is mostly limited if `FeaturesKeywords.IMAGE_CREATION` was enabled and `ArgumentsGiven.can_generate_side` was used, see [commands] for more info
    
    [commands]: #commands
    """


class RequiredFiles(StrEnum):
    """A silly enum that save some required file names (mostly optional)"""

    TEMPLATES = "templates.json"
    """Here the textual templates are saved, you might use `TemplateKeys` or custome ones, but using the tool with commands, only
    those that actually exits in `TemplateKeys` are supported, and the template is kinda limited, check `BUILDIN_TEMPLATES` for more info
    """
    ANIMATED = "keys.json"
    """Here the keyword within the words are saved, mostly they are saved to differeciate single image with animated ones, see `BUILDIN_ANIMATION_KEYS` for a better
    how-to guide
    """
    INFO = "info.cgf"
    """Here part of the tool's behavior starts, what is described in `ImageConfigHead` and `ImageConfigValue` are saved and evaluated
    in runtime, for more info, check their respective section 
    """


class ColorPerLevel(StrEnum):
    """A silly enum that saves certain colors for different porpuses"""

    GENERIC = "#A33838"
    """Generic color"""
    CRITIC = "#BEBC1B"
    """Critical color, mostly related to delete files or certain process"""
    INTERNAL = "#922296"
    """like `ColorPerLevel.GENERIC`, but for internal porpuses"""


class ProccesKeywords(StrEnum):
    """A silly enum that saves a flag-like system (not the best ofc) that determines how `write_common_file` and other functions behave"""

    ALL = "a"
    """indicate to use everything"""
    SCALE = "s"
    """indicate to use scale-like format"""
    FLIP = "i"
    """indicate to use flip-like format"""
    SIDE = "k"
    """indicate to use side-like format (this doesn't check if the file actually exits...........)"""
    ANIMATED = "m"
    """indicate to use animated-like format, and this will actually check if the file is available for that porpuse, see `KEYS_IMPORTED` or `BUILDIN_ANIMATION_KEYS` for more info"""
    NOTHING = "n"
    """indicate to ignore certain low-level checks when used"""
    IGNORE = "g"
    """indicate to ignore certain internal-level checks when used"""
    SUBFOLDER = "r"
    """indicate to also add subfolders to the procces"""


class ParseKeywords(StrEnum):
    """A silly enum used mostly to refer the format the images will have once the common files are created"""

    FILE = "f"
    """indicate to use file-like format"""
    FOLDER = "o"
    """indicate to use folder-like format"""


class ImportKeywords(StrEnum):
    """A silly collection of file types that are supported to import by the tool, they are mostly used to no evaluate twice the file type"""

    IMAGES = "i"
    """indicate to use image not/support extensions"""
    VIDEOS = "v"
    """indicate to use video not/support extensions"""
    SOUNDS = "s"
    """indicate to use sound not/support extensions"""


class MessagesError(StrEnum):
    """A silly collection of error messages, mostly used by the language service"""

    MODULE_NOT_FOUND = "MODULE_NOT_FOUND"
    MODULE_NOT_FOUND_USING_DEFAULT = "MODULE_NOT_FOUND_USING_DEFAULT"
    FEAUTRE_NOT_FOUND = "FEAUTRE_NOT_FOUND"
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    PATH_NOT_FOUND = "PATH_NOT_FOUND"
    USING_BUILT_IN = "USING_BUILT_IN"
    FEATURE_NOT_SUPPORTED = "FEATURE_NOT_SUPPORTED"
    ARGUMENT_NOT_FOUND = "ARGUMENT_NOT_FOUND"
    EXTENSION_ERROR = "EXTENSION_ERROR"
    INCORRECT_ARGUMENTS = "INCORRECT_ARGUMENTS"


class MessagesMeta(StrEnum):
    """A silly collection of meta arguments, mostly used by the language service"""

    DESCRIPTION = ("DESCRIPTION",)
    MESSAGE_INFO = "MESSAGE_INFO"
    MESSAGE_FUNCTION_INIT = "MESSAGE_FUNCTION_INIT"
    MESSAGE_FUNCTION_PROGRESS = "MESSAGE_FUNCTION_PROGRESS"
    MESSAGE_FUNCTION_ENDED = "MESSAGE_FUNCTION_ENDED"


class TemplateKeys(StrEnum):
    """A silly collection of formats that are currectly supported, mostly this is just a reference, the real ones might be present in
    `FORMATS_IMPORTED`, but these ones can be used in the correct areas (like `mkr_lines_list` to make exceptions to the rule, but that's not
    recommended anyway)
    """

    NORMAL = "normal"
    SCALE = "scale"
    FLIPED = "fliped"
    SIDE = "side"
    SOUND = "sound"
    VIDEO = "video"
    ZIPLOAD = "zipload"
    ANIMATED_BLINK_NORMAL = "animated_blink_normal"
    ANIMATED_ANIMATED_BODY = "animated_animated_body"


# trick XDDDD
for n in list(TemplateKeys):
    __pdoc__["TemplateKeys." + n.upper()] = f"""indicate to use the '{n}' template"""


class TemplatePath(StrEnum):
    """A silly enum that saves how the path is expressed and imported by `get_name_template`"""

    NORMAL = "normal"
    ENCRYPT = "encrypt"
    ZIP = "zip"


for n in list(TemplatePath):
    __pdoc__["TemplatePath." + n.upper()] = f"""indicate to use the {n} import"""


class TemplatePathKeys(StrEnum):
    """A really... reallly... REALLY silly enum that doesn't really do much.... just is being used by `write_side_image` cuz someone didn't want to use functional arguments (?)"""

    BASE = "base"
    """Base path (this should include everything, in windows C:/User/[name]/etc/etc/etc)"""
    NAME = "name"
    """Base name, mostly what is at the end of `TemplatePathKeys.BASE` path"""


########################################################
#
# Features zone
#
########################################################
features_available: list[str] = []
"""
A silly collection of features that saves all available/ready to add features
"""
features_enabled: list[str] = []
"""
the same as `features_available`, but when enabled
"""


def add_feature(what: FeaturesKeywords, is_internal: bool = True) -> bool:
    """Add a feature based on `FeaturesKeywords` and return if it was added

    Args:
        what (FeaturesKeywords): the feature to enable
        is_internal (bool, optional): determine if use `features_available` or `features_enabled` to add the feature. Defaults to True.

    Returns:
        bool: was it added?
    """
    global features_available, features_enabled
    ref = features_available if is_internal else features_enabled
    if not what in FeaturesKeywords:
        return False
    ref.append(what)
    return True


def has_feature(what: FeaturesKeywords, is_internal: bool = True) -> bool:
    """Check if the feature is enabled or can exits

    Args:
        what (FeaturesKeywords): the feature
        is_internal (bool, optional): determine if use `features_available` or `features_enabled`. Defaults to True.

    Returns:
        bool: has the feature?
    """
    return what in FeaturesKeywords and what in (
        features_available if is_internal else features_enabled
    )


########################################################
#
# Messages/Language built-in zone
#
########################################################
logger.info("Starting language service")
languages: dict[str, dict[str, str]] = {
    "en": {
        MessagesError.MODULE_NOT_FOUND_USING_DEFAULT: "There's not '{name}' installed, using default",
        MessagesError.MODULE_NOT_FOUND: "There's not '{name}' installed",
        MessagesError.FEAUTRE_NOT_FOUND: "The {name} feature couldn't be found or used",
        MessagesError.ARGUMENT_NOT_FOUND: "The {name} argument couldn't be found",
        MessagesError.FILE_NOT_FOUND: "The {file} file couldn't be found",
        MessagesError.PATH_NOT_FOUND: "The {path} path couldn't be found",
        MessagesError.USING_BUILT_IN: "Using {name} built-in instead",
        MessagesMeta.DESCRIPTION: "This is a simple tool easy-to-use to import assets and stuff from normal files to common.rpy files",
        MessagesError.FEATURE_NOT_SUPPORTED: "The feature '{name}' is not supported due to {reason}",
        MessagesMeta.MESSAGE_INFO: "Given '{name}' was made the operation '{operation}' with result '{result}'",
        MessagesMeta.MESSAGE_FUNCTION_INIT: "The operation '{name}' was started",
        MessagesMeta.MESSAGE_FUNCTION_PROGRESS: "Resolving '{name}' operation",
        MessagesMeta.MESSAGE_FUNCTION_ENDED: "The operation '{name}' was ended with '{result}' as result",
        MessagesError.EXTENSION_ERROR: "There are some files that might need change its extension or be compressed:",
        MessagesError.INCORRECT_ARGUMENTS: "Due a incorrect configuration for '{arguments}', '{default}' will be used, based on '{message}'",
    }
}
"""
The dictonary used by the language service, and this is a buildin variable that basically saves all of them

a file could be better, but might limit the tool
"""
logger.info("Built-in languages: " + str(list(languages.keys())))
os_language: str = getdefaultlocale()[0].split("_")[0]  # type: ignore
"""
the detected os language (thanks to `getdefaultlocale` )
"""
logger.info("OS language detected: " + os_language)
language: str = os_language if os_language in languages.keys() else "en"
"""
the selected language, by default `os_language` is used, otherwise enligsh by default
"""
logger.info("Selected language: " + language)
logger.info("Language service ended")


def get_message_translated(name: str, /, **kwargs: dict[str, str]) -> str:
    """Get and return the message using the actual language determined by `language` and the text corresponds to `languages`

    Args:
        name (str): the key to get from

    Returns:
        str: the text in question
    """
    if not name in languages[language]:
        logger.debug(
            "The key '{}' couldn't be found base in the language {}".format(
                name, language
            )
        )
        return ""
    try:
        return (
            languages[language][name].format(**kwargs)
            if len(kwargs) != 0
            else languages[language][name]
        )
    except KeyError:
        print(
            get_message_translated(
                MessagesMeta.MESSAGE_INFO,
                name=name,
                operation="get_message_translated",
                result="key not found",
            )
        )
        return "Unkown error"


parser: ArgumentParser = ArgumentParser(
    "Importer",
    description=get_message_translated(MessagesMeta.DESCRIPTION),
    epilog="You can search for more help here! --> https://github.com/Z3R0GT/renpy-auto-importer",
)
"""
mostly used when the tool is __main__
"""

########################################################
#
# Imports specifc zone
#
#
# NOTE: all modules (except for those that are require adove) MUST be declared here,
# in case is required and this doesn't is delivered with python, use __return__ variable
# to make the program die after the error is launched (typing_extensions module section is an example of how-to)
#
# NOTE 2.0: if some class/module is required/used by the program, but there's an alternative or workaround, don't use
# __return__, just declare its class or function when needed (just like with tqdm)
#
########################################################
logger.info("Starting phase 1: Importing extra module")
try:
    from typing_extensions import (
        Sequence,
        overload,
        Literal,
        Callable,
    )
except ModuleNotFoundError:
    from typing import overload

    logger.fatal(
        get_message_translated(MessagesError.MODULE_NOT_FOUND).format(
            name="typing_extensions"
        )
    )
    __return__ = 1


# let's add some arguments to this
@overload
def compress_multiple(
    src_file: list[Path | str],
    src_path: list[Path, str],
    output_path: str | Path,
    password: str,
    level: int,
    do_during: Callable[[int], None],
) -> None:
    """Given a certain(s) path(s), this compress them into a single zip/rar file, check their [source] for more info

    Args:
        src_file (list[Path  |  str]): source files
        src_path (list[Path, str]): source paths (this must be related to src_file)
        output_path (str | Path): where the file should be placed
        password (str): (opcional) the password
        level (int): check the [source] for more info
        do_during (Callable[[int], None]): check the [source] for more info

    [source]: https://pypi.org/project/pyminizip/
    """
    ...


try:
    from pyminizip import compress_multiple

    if not add_feature(FeaturesKeywords.ZIP_COMPRESSION):
        logger.info(
            get_message_translated(MessagesError.MODULE_NOT_FOUND).format(
                name=FeaturesKeywords.ZIP_COMPRESSION
            )
        )
except ModuleNotFoundError:

    def compress_multiple(
        src_file: list[Path | str],
        src_path: list[Path, str],
        output_path: str | Path,
        password: str,
        level: int,
        do_during: Callable[[int], None],
    ) -> None:
        logger.warning(
            get_message_translated(MessagesError.MODULE_NOT_FOUND).format(
                name="pyminizip"
            )
        )

    warnings.warn(
        get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="pyminizip")
    )

try:
    from tqdm import tqdm

    if not add_feature(FeaturesKeywords.PRETTY_CONSOLE):
        logger.info(
            get_message_translated(MessagesError.MODULE_NOT_FOUND).format(
                name=FeaturesKeywords.PRETTY_CONSOLE
            )
        )
except ModuleNotFoundError:

    class tqdm[T]:

        def __init__(self, a: Sequence[T], **kwargs):
            self.iterable = a

        def __iter__(self) -> T:
            for n in self.iterable:
                yield n

    logger.warning(
        get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="tqdm")
    )
    warnings.warn(
        get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="tqdm")
    )

try:
    from colorama import Fore
except ModuleNotFoundError:

    class Fore(StrEnum):
        BLACK = "\033[30m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        MAGENTA = "\033[35m"
        CYAN = "\033[36m"
        WHITE = "\033[37m"
        RESET = "\033[38m"

    logger.warning(
        get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="colorama")
    )
    warnings.warn(
        get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="colorama")
    )


try:
    from PIL import Image, UnidentifiedImageError

    if not add_feature(FeaturesKeywords.IMAGE_CREATION):
        logger.info(
            get_message_translated(MessagesError.MODULE_NOT_FOUND).format(
                name=FeaturesKeywords.IMAGE_CREATION
            )
        )
except ModuleNotFoundError:
    # copy paste lol
    class UnidentifiedImageError(OSError):
        """
        Raised in :py:meth:`PIL.Image.open` if an image cannot be opened and identified.

        If a PNG image raises this error, setting :data:`.ImageFile.LOAD_TRUNCATED_IMAGES`
        to true may allow the image to be opened after all. The setting will ignore missing
        data and checksum failures.
        """

        pass

    logger.warning(
        get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="pillow")
    )
    warnings.warn(
        get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="pillow")
    )

try:
    from whoosh.filedb.filestore import RamStorage
    from whoosh.qparser import MultifieldParser
    from whoosh.fields import TEXT, Schema

    if not add_feature(FeaturesKeywords.RENAMING_PROCESS):
        logger.info(
            get_message_translated(MessagesError.MODULE_NOT_FOUND).format(
                name=FeaturesKeywords.RENAMING_PROCESS
            )
        )
except ModuleNotFoundError:
    logger.warning(
        get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="whoosh")
    )
    warnings.warn(
        get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="whoosh")
    )

try:
    from platformdirs import user_data_dir
except ModuleNotFoundError:

    def user_data_dir(
        appname: str | None = None,
        appauthor: str | Literal[False] | None = None,
        version: str | None = None,
        roaming: bool = False,  # noqa: FBT001, FBT002
        ensure_exists: bool = False,  # noqa: FBT001, FBT002
    ) -> str:
        return Path(".").as_posix()

    logger.warning(
        get_message_translated(MessagesError.MODULE_NOT_FOUND).format(
            name="platformdirs"
        )
    )
    warnings.warn(
        get_message_translated(MessagesError.MODULE_NOT_FOUND).format(
            name="platformdirs"
        )
    )

parser.exit(__return__, __return_text__[__return__]) if __return__ != 0 else None
logger.info("Ended phase 1")

########################################################
#
# Defaults zone
#
########################################################
DEFAULT_SIZE_SCREEN: str = (
    "1920x1080"  # usado para el tamaño de la pantalla a escalar imagenes
)
"""
default target's screen dimension
"""
DEFAULT_SIZE_SIDE_VAR: str = (
    "300x350"  # usado para la dimensión de las imagenes de marco (side)
)
"""
default target's frame used by side variants
"""
DEFAULT_SIZE_CORP_VAR: tuple[int, int, int, int] = (675, 5, 1067, 480)
"""
default dimensions to cut from an image
"""

DEFAULT_RESOURCE_PATH: str = "assets"
"""
default folder to search for assets, check [folder structure] for more info

[folder structure]: #folder-structure
"""

DEFAULT_PATH_VIDEO: str = "%(base)s/video"  # base
"""
default folder to search for videos, check [folder structure] for more info

[folder structure]: #folder-structure
"""
DEFAULT_PATH_SOUND: str = "%(base)s/audio"  # base
"""
default folder to search for audio, check [folder structure] for more info

[folder structure]: #folder-structure
"""
DEFAULT_PATH_IMAGE: str = "%(base)s/images"  # base
"""
default folder to search for images, check [folder structure] for more info

[folder structure]: #folder-structure
"""

DEFAULT_PATH_SIDE: str = f"%({TemplatePathKeys.BASE})s/side"  # mostly for images
"""
default folder to add side variants (once created), this will use of __`DEFAULT_PATH_IMAGE`/[etc]/[sprite/character]/`DEFAULT_PATH_SIDE`__
"""

########################################################
#
# Extensions zone
#
########################################################
IGNORE_NOT_SUPPORTED: bool = False
"""
controll if ignore not supported files (basically supress some warnings)
"""
DEFAULT_EXTEND_IMAGE_NOT_SUPPORT: list[str] = ["png", "jpg"]
"""
extension of file that are not actually supported (images this case), yet, this doesn't means renpy can't, check [the renpy docs]


[the renpy docs]: https://www.renpy.org/doc/html/displaying_images.html
"""
DEFAULT_EXTEND_VIDEO_NOT_SUPPORT: list[str] = ["mp4"]
"""
extension of file that are not actually supported (videos this case), yet, this doesn't means renpy can't, check [the renpy docs]

[the renpy docs]: https://www.renpy.org/doc/html/audio.html
"""
DEFAULT_EXTEND_SOUND_NOT_SUPPORT: list[str] = ["mp3"]
"""
extension of file that are not actually supported (sound this case), yet, this doesn't means renpy can't, check [the renpy docs]

[the renpy docs]: https://www.renpy.org/doc/html/movie.html
"""


DEFAULT_EXTEND_IMAGE_SUPPORT: list[str] = ["webp", "png"]
"""
extension of file that are actually supported (images this case), yet, this doesn't means renpy can, check [the renpy docs]


[the renpy docs]: https://www.renpy.org/doc/html/displaying_images.html
"""
DEFAULT_EXTEND_VIDEO_SUPPORT: list[str] = ["webm"]
"""
extension of file that are actually supported (videos this case), yet, this doesn't means renpy can, check [the renpy docs]


[the renpy docs]: https://www.renpy.org/doc/html/audio.html
"""
DEFAULT_EXTEND_SOUND_SUPPORT: list[str] = ["ogg"]
"""
extension of file that are actually supported (sounds this case), yet, this doesn't means renpy can, check [the renpy docs]


[the renpy docs]: https://www.renpy.org/doc/html/movie.html
"""

SKIP_SYMBOLS: list[str] = ["_"]
"""
a series of single-characters, mostly used when the name of something start, this will controll if this will be skiped
"""
SKIP_GEN_NAMES: list[str] = []
"""
a collection of names, this is totally independement from its type
"""
SKIP_FILE_NAME: list[str] = ["gui", "options", "screens"]
"""
the same as `SKIP_GEN_NAMES`, but it's limited to file names
"""
SKIP_FOL_NAMES: list[str] = ["gui", "credits", "logos", "fonts"]
"""
the same as `SKIP_GEN_NAMES`, but it's limited to folder names
"""
SKIP_EXTENSION: list[str] = []
"""
the same as `SKIP_GEN_NAMES`, but it's limited to extensions names
"""

RESERVED_GENERIC_FILE_NAMES: tuple[str, str, str, str, str, str] = (
    "character",
    "characters",
    "noncommon",
    "common",
    "common_test",
    "common_dist",
)
"""
a silly collection of reserved files that the tool will make use of
"""
RESERVED_GENERIC_FILE_EXTEN: list[str] = ["rpyc"]
"""
a silly collection of reserved extension (mostly by renpy or by the tool)
"""
RESERVED_GENERIC_FOLD_NAMES: tuple[str, str, str, str] = (
    "generic_template",
    "side",
    "logs",
    "interactive",
)
"""
a silly collection of reserved folder names
"""
RESERVED_GENERIC_CREA_NAMES: tuple[str, str, str] = (
    "common",
    "common_test",
    "common_dist",
)
"""
a silly collection of file names used by the tool
"""
RESERVED_GENERIC_CREA_EXTEN: tuple[str] = "rpy"
"""
a silly collection of extensions used by the tool
"""

########################################################
#
# Etc zone
#
########################################################
ZIP_PASSWORD: str = ""
DEFAULT_TAB: int = 4
"""
controll how the tool detect lines within the renpy files (hope you use tabs.... please... use TABs)
"""
DEFAULT_NAME_LIMIT: int = 3
"""
controll the times limit for the tool find the __character.rpy__ file to get the alias from some character
"""
DEFAULT_KIND_IMPORT: Literal["source", "dev", "zip"] = "dev"
"""
controll the template used
"""
FILE_NAME_REPLACE: dict[int, str] = str.maketrans(
    {"(": "", "!": " ", ")": "", "-": "_", "{": "", "}": ""}
)
"""
a list of symbols that we hate and they must be replaced at once!
"""
FILE_NAME_REPLACE_LONG: dict[str, str] = {
    "scene": "scn",
}
"""
a list of symbols to resume some names (when used) to not match with renpy keyword/reserved words 

[this material] is old, but it cover the basics of why this variable

[this material]: https://www.renpy.org/wiki/renpy/spa/doc/reference/El_lenguaje_Ren'Py
"""

########################################################
#
# Buildin zone
#
########################################################

BUILDIN_TEMPLATES: dict[TemplateKeys | str, str | list[str | bool | list[str]]] = {
    TemplateKeys.NORMAL: 'image %(name)s = "%(path)s"\n',
    TemplateKeys.SCALE: 'image %(name)s = im.Scale("%(path)s", %(size_scale)s)\n',
    TemplateKeys.FLIPED: 'image %(name)s flip = im.Flip("%(path)s", horizontal=True)\n',
    TemplateKeys.SIDE: 'image side %(abbr)s %(name)s = im.Scale("%(path)s", %(size_side)s)\n',
    TemplateKeys.SOUND: 'define audio.%(name)s = "%(path)s"\n',
    TemplateKeys.VIDEO: 'image %(name)s = Movie(play="%(path)s", bypass=True)\n',
    TemplateKeys.ZIPLOAD: "renpy.loadbytes('%(file)s', '%(path)s', '%(kind)s')",
    TemplateKeys.ANIMATED_BLINK_NORMAL: [
        True,
        "image %(name)s blink:",
        ["repeat", '%(tab)s"%(path)s"', "%(tab)sBlinkSpeed"],
    ],
    TemplateKeys.ANIMATED_ANIMATED_BODY: [
        True,
        "image %(name)s:",
        "%(tab)sparallel:",
        [
            "repeat",
            '%(tab)s%(tab)sim.Scale("%(path)s", %(size_scale)s) with Dissolve(0.2)',
            "%(tab)s%(tab)s0.5",
        ],
        "%(tab)sparallel:",
        "%(tab)s%(tab)sxzoom -1.0",
        "%(tab)s%(tab)sxalign -20.0",
        "%(tab)s%(tab)slinear 2.0 xalign -8.0",
    ],
}
"""
about
-------------
This is one of the core variables for this tool, because it basically defines how the template for each `TemplateKeys` or new key should be

keywords
-------------
how it works is basically using the % operator to replace more easily certain keywords, when the tool reach `mkr_lines_list` function, 
based on what `write_names` and the modes based on `TemplateKeys`, `ProccesKeywords`, `TemplatePathKeys` and `ParseKeywords` are configured, 
alongside with `FeaturesKeywords` and `ImportKeywords` configured, one or several templates will be used, we reserve the next ones
seening in the information table, and also take a look at the examples, but take into account these are __examples__ assuming certain 
configurations

the real ones might be different from what is showed here, and each one of the next keyword must be used like the next example
(and also this should the form that your custom templates might have):

```python
{
    "normal" : 'image %(name)s = "%(path)s"\\n'
}
```

the example from adove is an extract from the default `BUILDIN_TEMPLATES` reference template, ofc your might be different

and well... here is the information you might be looking for

Information table
----
----

| Keyword   | Meaning                                                                                                                                                                                                                                                                                                     | 
|:----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|name       | represents the most simple part of the file which is being parsed by `get_name_parsed`                                                                                                                                                                                                             <br><br> | 
|path       | this is the easiest and most simple part of the path, this starts from `DEFAULT_RESOURCE_PATH` or `ArgumentsGiven.game` 'till the path's end, mostly they are parsed as posix (/) and then normalized by `get_path_parsed` (under normal circunstance, check the [folder structure] for more info) <br><br> | 
|size_scale | this represent the target's screen deimension, this should a Heigh__x__width (`DEFAULT_SIZE_SCREEN`) or a ```tuple[int, int]```, (anyway, they will parsed like the output says)                                                                                                                   <br><br> | 
|size_side  | similar to the other, but this time represents the side's frame (`DEFAULT_SIZE_SIDE_VAR`)                                                                                                                                                                                                          <br><br> |
|abbr       | this the short form of __name__, but, this will be created using the folder's name or character.rpy (mostly depends on `get_name_acron`)                                                                                                                                                           <br><br> | 
|file       | it's the same as path, but fixed with `TemplatePath`, which either case, might change depends on this last mode                                                                                                                                                                                    <br><br> | 
|kind       | this feature depends on a modded SDK (which support the encription system), basically this repreent a literal value from `ImportKeywords`                                                                                                                                                          <br><br> | 
|tab        | this is basically a ```" " * DEFAULT_TAB``` operation                                                                                                                                                                                                                                              <br><br> | 

A bit of side note, when one of the values is a `list`, we don't know how to how to determine if it's an animated template, since a list might be also a non-animated template
so, the first argument must always be __True__ or __False__ to indicate that, and if it is an animated template, it can use `ImageConfigValue.REPEAT` to enter into a 
loop to repeat certain statement, motly when dealing with multiple files

.. caution::
    most of their behavior depends on multiple variable, the examples of below were made considering the most simpliest 
    flags, being `ParseKeywords.FILE`, `ImportKeywords.IMAGES` and `TemplatePath.NORMAL` in a __sprite__ folder with a `DEFAULT_TAB` of __4__

Example table
--------
--------

| Keyword   | Input                                                                  | Output                                                        |
|:----------|------------------------------------------------------------------------|:-------------------------------------------------------------:|
|   name    | hello_world.png                                                        | hello_world                                          <br><br> |
|   path    | C:/Users/[USER]/Desktop/awesome-game/game/assets/images/Sprites/Xellar | assets/images/Sprites/Xellar                         <br><br> |
|size_scale | 1920x1080 or (1920, 1080)                                              | 1920, 1080                                           <br><br> |
|size_side  | 300x350 or (300, 350)                                                  | 300, 350                                             <br><br> |
|file       | __`ArgumentsGiven.sprite`__/Xellar/xellar_normal.png <br><br>          | __`ArgumentsGiven.sprite`__/Xellar/xellar_normal.png <br><br> |
|tab        | 4                                                                      |"----"                                                <br><br> |


[folder structure]: #folder-structure
"""

BUILDIN_FILE_TEMPLATES: dict[TemplatePath, str] = {
    TemplatePath.ENCRYPT: "%(path)s/%(file)s.enc",
    TemplatePath.NORMAL: "%(path)s/%(file)s",
    TemplatePath.ZIP: "%(path)s/%(file)s.zip",
}
"""
about
-------
basically this defines how the __file__ part of the template from `BUILDIN_TEMPLATES` or `FORMATS_IMPORTED` is using almost the same structure, but with differences

which basically are adding certain keyword/extension extras to the file.
.. todo::
    make the function `get_name_template` or once finished the 1st assets import validate the file using `handler` (?)

check `BUILDIN_TEMPLATES`, in their "keywords" section to know about how the format works
------

Information table
----
----
| Keyword  | Meaning                                           | 
|:---------|---------------------------------------------------|
|path      | the whole or simpliest path from a certain origin |
|file      | the file that is being tested                     | 

"""


BUILDIN_ANIMATION_KEYS: dict[TemplateKeys, list[str]] = {
    TemplateKeys.ANIMATED_ANIMATED_BODY: ["walking"],
    TemplateKeys.ANIMATED_BLINK_NORMAL: ["blink", "e"],
}
"""
about
--------
basically, this controlls when used some template based on their names (if includes some keywords or not)

here we use a `key` to represent a template within `TemplateKeys`, and a `list[str]` to represent a collection of keywords that `is_animated_name`
will make use to indicate if it's animated or not
"""

########################################################
#
# Path handlers zone
#
########################################################
ROOT_EXE_GAME: Path = Path(getcwd())
"""
the root folder (usually the same as where the tool is)
"""
ROOT_RES_SOFT: Path = Path(user_data_dir(__product__, __author__))
"""
the data folder (in windows, basically appdata/`__product__`/`__author__`) 
"""

_literal_fields_files = Literal["dir", "file", "both"]

_literal_fields_exten = Literal["image", "sound", "video"]


def get_list_system_dirs(
    origin: Path = Path("."), kind: _literal_fields_files = "file", **kwargs
) -> list[str | list[str]]:
    """Based on `origin`, this will get all files based on `kind` without any filter, whatever is in `origin`, this will return

    Args:
        origin (Path, optional): the origin path. Defaults to Path(".").
        kind (_literal_fields_files, optional): the resource type that will return. Defaults to "file".

    Returns:
        list[str | list[str]]: a list of file/folders or both
    """
    if not origin.exists():
        return []

    match kind:
        case "both":
            return [
                get_list_system_dirs(origin, "dir"),
                get_list_system_dirs(origin, "file"),
            ]
        case "dir":
            return list(filter(lambda x: (origin / x).is_dir(), listdir(origin)))
        case "file":
            return list(filter(lambda x: (origin / x).is_file(), listdir(origin)))


logger.info("Starting phase 2: importing config files")
FORMATS_IMPORTED: dict[TemplateKeys | str, str | list[str]]
"""
The actual variable that the tool will make use, not what `BUILDIN_TEMPLATES`, that's just the default 
implementation in case `RequiredFiles.TEMPLATES` couldn't be found

see `BUILDIN_TEMPLATES` for more info, since the structure it's pretty much the same
"""
if RequiredFiles.TEMPLATES in get_list_system_dirs(ROOT_EXE_GAME, "file"):
    FORMATS_IMPORTED = load(open(ROOT_EXE_GAME / RequiredFiles.TEMPLATES, "r"))
else:
    _ = get_message_translated(MessagesError.FILE_NOT_FOUND).format(
        file=RequiredFiles.TEMPLATES
    )
    _ += ", " + get_message_translated(MessagesError.USING_BUILT_IN).format(
        name="format_imported"
    )
    logger.warning(_)
    FORMATS_IMPORTED = BUILDIN_TEMPLATES

KEYS_IMPORTED: dict[TemplateKeys, list[str]]
"""
The actual variable that the tool will make use, not what `BUILDIN_ANIMATION_KEYS`, that's just the default 
implementation in case `RequiredFiles.ANIMATED` couldn't be found

see `BUILDIN_ANIMATION_KEYS` for more info, since the structure it's pretty much the same
"""
if RequiredFiles.ANIMATED in get_list_system_dirs(ROOT_EXE_GAME, "file"):
    KEYS_IMPORTED = load(open(ROOT_EXE_GAME / RequiredFiles.ANIMATED, "r"))
else:
    _ = get_message_translated(MessagesError.FILE_NOT_FOUND).format(
        file=RequiredFiles.ANIMATED
    )
    _ += ", " + get_message_translated(MessagesError.USING_BUILT_IN).format(
        name="keys_imported"
    )
    logger.warning(_)
    KEYS_IMPORTED = BUILDIN_ANIMATION_KEYS
logger.info("Ended phase 2")


########################################################
#
# Utils zone
#
########################################################
class SearchEngine:
    """light weigth search based on whoosh"""

    def __init__(self, sc: Schema):
        # sc = sc#Schema(path=TEXT(stored=True), content=TEXT(stored=True))
        self.schema = sc
        sc.add("raw", TEXT(stored=True))
        self.ix = RamStorage().create_index(self.schema)

    def index_documents(self, docs: Sequence):
        """Index some documents to RAM

        Args:
            docs (Sequence): docs
        """
        writer = self.ix.writer()
        for doc in docs:
            d = {k: v for k, v in doc.items() if k in self.schema.stored_names()}
            d["raw"] = dumps(doc)  # raw version of all of doc
            writer.add_document(**d)
        writer.commit(optimize=True)

    def get_index_size(self) -> int:
        """Get all docs indexed so far

        Returns:
            repr (int): lenght of docs indexed
        """
        return self.ix.doc_count_all()

    def query(self, q: str, fields: Sequence, highlight: bool = True) -> list[dict]:
        """Search trought all indexed docs

        Args:
            q (str): name to search for
            fields (Sequence): fields to search for
            highlight (bool, optional): highlight where the match is. Defaults to True.

        Returns:
            repr (List[Dict]): all coincidences
        """
        search_results = []
        with self.ix.searcher() as searcher:
            results = searcher.search(
                MultifieldParser(fields, schema=self.schema).parse(q)
            )
            for r in results:
                d = loads(r["raw"])
                if highlight:
                    for f in fields:
                        if r[f] and isinstance(r[f], str):
                            d[f] = r.highlights(f) or r[f]

                search_results.append(d)

        return search_results


def del_jump(base: list[str], allow_blank: bool = False) -> None:
    """Delete __\\n__ and __\\r__ spaces and tab if possible

    Args:
        base (list[str]): a list of lines to delete those keysfrom
        allow_blank (bool, optional): allow tabs don't be deleted. Defaults to False.
    """
    for c in range(0, len(base)):
        base[c] = base[c].replace("\n", "").replace("\r", "")

    if not allow_blank:
        while base.count("") != 0:
            del base[base.index("")]


def add_jump(base: list) -> list[str]:
    """this parses `base` to a `list[str]` adding __\\n__ characters

    Args:
        base (list): base

    Returns:
        list[str]: parsed base
    """
    return [f"{i}\n" for i in base]


def mkr_str(base: list, sep: str = "") -> str:
    """this parses a `base` to a simple `str` using the `sep`

    Args:
        base (list): base
        sep (str, optional): separator. Defaults to "".

    Returns:
        str: parsed base
    """
    return sep.join([str(i) for i in base])


def has_required_keys(base: list[str], reference: StrEnum) -> bool:
    """Check if all `base` keys exits in `reference`, which is a enum

    Args:
        base (list[str]): base
        reference (StrEnum): reference enum

    Returns:
        bool: ¿all `base` exits in `reference`
    """
    for _ in base:
        if not _ in reference:
            print(get_message_translated(MessagesError.ARGUMENT_NOT_FOUND, name=_))
            return False
    return True


########################################################
#
# Path handler zone
#
########################################################
def mkr_dir(what: str, root: Path | str = ROOT_EXE_GAME) -> Path:
    """Basicallt this create the given `what` folder and return the path to it

    .. note::
        this will __not__ evaluate if the given path really exits

    Args:
        what (str): folder(s) to create
        root (Path | str, optional): actual path. Defaults to `ROOT_EXE_GAME`.

    Returns:
        Path: root / what with the path already created
    """
    actual: Path
    if isinstance(root, Path):
        actual = Path(root)
    elif isinstance(root, Path):
        actual = root
    else:
        actual = Path(".").resolve()
    cur: Path = actual / what
    try:
        cur.mkdir()
    except FileExistsError:
        pass
    return cur


def is_reserved(name: str, kind: _literal_fields_files = "file") -> bool:
    """check if the given name is reserved by the tool or not, based on `kind`, will use `RESERVED_GENERIC_FOLD_NAMES` or `RESERVED_GENERIC_FILE_NAMES` and its
    skip variables

    Args:
        name (str): to match
        kind (_literal_fields_files, optional): resource type. Defaults to "file".

    Returns:
        bool: is reserved?
    """
    if kind == "both":
        kind = "file"

    name: str = (
        name.split(".")[0] if len(name.split(".")[0]) != 0 else name.split(".")[1]
    )

    if name[0] in SKIP_SYMBOLS[0] or name in SKIP_GEN_NAMES:
        return True

    if kind == "dir":
        return name in SKIP_FOL_NAMES or name in RESERVED_GENERIC_FOLD_NAMES
    elif kind == "file":
        return name in SKIP_FILE_NAME or name in RESERVED_GENERIC_FILE_NAMES
    else:
        return False


def is_animated_name(name: str) -> TemplateKeys | None:
    """checks if the name is animated and return the key that corresponds to `TemplateKeys`, none if fails

    Args:
        name (str): name to evaluate

    Returns:
        TemplateKeys | None: result
    """

    for part in name.split("_"):

        for key, parts in KEYS_IMPORTED.items():
            if part in parts:
                return key

    return None


def get_list_system_file(
    kind: _literal_fields_files, origin: Path = Path("."), is_normal: bool = True
) -> list[str | list[str]]:
    """similar to `get_list_system_dirs`, but applying `is_reserved` function to determine that, you can get if the function
    return reserved stuff or not based on `is_normal` param, but this shouldn't return both, better use `get_list_system_dirs` to get
    both of them

    Args:
        kind (_literal_fields_files): resource type
        origin (Path, optional): origin path. Defaults to Path(".").
        is_normal (bool, optional): return reserved resources or not, not both. Defaults to True.

    Returns:
        list[str | list[str]]: collection of files/folders/both
    """
    match kind:
        case "both":
            return [
                get_list_system_file("dir", origin, is_normal),
                get_list_system_file("file", origin, is_normal),
            ]
        case y if y in ["file", "dir"]:
            return list(
                filter(
                    lambda x: (
                        not is_reserved(x, kind) if is_normal else is_reserved(x, kind)
                    ),
                    get_list_system_dirs(origin, kind),
                )
            )
        case _:
            return []


def get_list_file_extended(
    extension: str | list[str],
    is_normal: bool = True,
    *,
    origin: Path = Path("."),
    local: list[str] = [],
) -> list[str]:
    """similar to `get_list_system_file`, but this should those files that match their extension with what is
    being expected

    Args:
        extension (str | list[str]): collection of extensions
        is_normal (bool, optional): return reserved resources or not, not both. Defaults to True.
        origin (Path, optional): origin path. Defaults to Path(".").
        local (list[str], optional): collection of names, in case you already have the files. Defaults to [].

    Returns:
        list[str]: those names that matched `extension` list
    """
    local = (
        get_list_system_file("file", origin, is_normal) if len(local) == 0 else local
    )

    @singledispatch
    def extend(extension: str) -> list[str]:
        return [
            i for i in local if i[-len(extension) :] in [extension] + SKIP_EXTENSION
        ]

    @extend.register
    def _(extension: list) -> list[str]:
        a = []
        extension += SKIP_EXTENSION  # HACK
        for i in local:
            for n in extension:
                if i[-len(n) :] in extension:
                    a.append(i)
                    break
        return a

    @extend.register
    def _(extension: tuple) -> list[str]:
        return extend(list(extension))

    return extend(extension)


def get_list_file_named(
    names: str | Sequence[str] | dict[str | Sequence[str]],
    is_normal: bool = True,
    *,
    origin: Path = Path("."),
    local: list[str] = [],
) -> list[str]:
    """Similar to `get_list_system_file`, but for names

    Args:
        names (str | Sequence[str] | dict[str  |  Sequence[str]]): collection of names
        is_normal (bool, optional):  return reserved resources or not, not both. Defaults to True.
        origin (Path, optional):  origin path. Defaults to Path(".").
        local (list[str], optional):  collection of names, in case you already have the files. Defaults to [].

    Returns:
        list[str]: those names that matched `names` collection
    """
    local = (
        get_list_system_file("file", origin, is_normal) if len(local) == 0 else local
    )
    end: list[str] = []

    # NOTE: can we improve this?
    @singledispatch
    def find_file(nm: dict) -> list[str]:
        for file in local:
            name = file.split(".")[0]
            for itm in list(nm.items())[1]:
                if (
                    len(
                        [
                            i
                            for i in name.split(" " if name.count(" ") != 0 else "_")
                            if i in itm
                        ]
                    )
                    == 0
                ):
                    end.append(file)
                    break
        return end

    @find_file.register
    def _(nm: list) -> list[str]:
        for file in local:
            name = file.split(".")[0]
            if not (
                len(
                    [
                        i
                        for i in name.split(" " if name.count(" ") != 0 else "_")
                        if i in nm
                    ]
                )
                == 0
            ):
                end.append(file)
        return end

    @find_file.register
    def _(nm: str) -> list[str]:
        return find_file([nm])

    @find_file.register
    def _(nm: tuple) -> list[str]:
        return find_file(list(nm))

    return find_file(names)


def get_list_files(
    names: list[str],
    extesions: list[str],
    is_normal: bool = True,
    origin: Path = Path("."),
    local: list[str] = [],
) -> list[str]:
    """This is just a shortcut that evaluate names and then extensions for a collection of files

    Args:
        names (list[str]): collection of names
        extesions (list[str]): collection of extensions
        is_normal (bool, optional): return reserved resources or not, not both. Defaults to True.
        origin (Path, optional): origin path. Defaults to Path(".").
        local (list[str], optional):  collection of names, in case you already have the files. Defaults to [].

    Returns:
        list[str]:  those names that matched the given criteria
    """
    local = get_list_file_named(names, is_normal, origin=origin, local=local)
    local = get_list_file_extended(extesions, is_normal, origin=origin, local=local)

    return local


def get_list_subfolders(
    origin: Path = Path("."), exclude: Sequence[str] = []
) -> list[str | Path]:
    """This will recursible get folders and its subfolders within `origin` based on `get_list_system_file`

    Args:
        origin (Path, optional): starter path. Defaults to Path(".").
        exclude (Sequence[str], optional): exclode some name. Defaults to [].

    Returns:
        list[str | Path]: all folders/subfolders within `origin`
    """
    folders = [
        origin / x for x in get_list_system_file("dir", origin) if not x in exclude
    ]
    for x in folders:

        if x.resolve() == origin.resolve():
            continue

        if not x.exists():
            continue

        folders += get_list_subfolders(x, exclude)
    # to avoid some erros due how lists are saved in python
    return folders.copy()


def get_path_parsed(start: str | list[str], origin: Path = Path(".")) -> str:
    """Based on a certain start keywords, this will cut `origin` and return its path if exits, otherwise, it'll return
    `origin` as posix

    Examples
    -------
    -------
    here start is `["assets", "images"]` when a good case

    | input                                                                 | output                       |
    |-----------------------------------------------------------------------|------------------------------|
    |C:/Users/[USER]/Desktop/awesome-game/game/assets/images/Sprites/Xellar | assets/images/Sprites/Xellar |

    here start is `["images"]` when a good case

    | input                                                                 | output                |
    |-----------------------------------------------------------------------|-----------------------|
    |C:/Users/[USER]/Desktop/awesome-game/game/assets/images/Sprites/Xellar | images/Sprites/Xellar |

    <br><br>

    here start is `["assets", "images"]` when a bad case

    - Example 1

    | input                                                          | output                                                          |
    |----------------------------------------------------------------|-----------------------------------------------------------------|
    |C:/Users/[USER]/Desktop/awesome-game/game/images/Sprites/Xellar | C:/Users/[USER]/Desktop/awesome-game/game/images/Sprites/Xellar |

    <br><br>

    - Example 2

    | input                                                  | output                                                  |
    |--------------------------------------------------------|---------------------------------------------------------|
    |C:/Users/[USER]/Desktop/awesome-game/game/assets/Xellar | C:/Users/[USER]/Desktop/awesome-game/game/assets/Xellar |

    Args:
        start (str | list[str]): collection of parts/folders to cut from
        origin (Path, optional): starter path. Defaults to Path(".").

    Returns:
        str: parsed `origin` __OR__ `origin` as posix
    """
    if not origin.is_dir():
        origin = Path(mkr_str(origin.as_posix().split("/")[:-1]))
    normal: list[str] = origin.resolve().as_posix().split("/")

    @singledispatch
    def wrapper(init: str) -> bool:
        nonlocal normal
        return init in normal

    @wrapper.register
    def _(init: list) -> bool:
        nonlocal normal
        checked: list[bool] = []

        while init.count(".") != 0:
            init.remove(".")

        for part in normal:
            if part in init:
                for n in range(len(init)):

                    if not init[n] in normal:
                        checked.append(False)
                        break

                    checked.append(normal[normal.index(part) + n] == init[n])
            if len(checked) != 0 and all(checked):
                return True

            checked = []
        return False

    dir_exits = wrapper(start)
    if not dir_exits:
        logger.warning(
            get_message_translated(
                MessagesError.PATH_NOT_FOUND,
                path=origin.resolve().as_posix() + " for " + str(start),
            )
        )
        return origin.as_posix()

    if isinstance(start, str):
        start = [start]

    return mkr_str(normal if not dir_exits else normal[normal.index(start[0]) :], "/")


def get_name_parsed(file: str) -> str:
    """Given a `file`'s name, this will parse it into something pretty simple, replacing and deleting numbers if needed

    Examples
    --------
    --------

    | input                     | output                       |
    |---------------------------|------------------------------|
    | Xellar normal speak.png   | xellar_normal_speak          |
    | Xellar normal speak 1.png | xellar_normal_speak_1_base   |
    | Xellar!normal!speak.png   | xellar_normal_speak          |

    Args:
        file (str): file

    Returns:
        str: file parsed
    """
    # NOTE: most of devs use VS Code, so replacing the spaces for _, will make the renpy extesion include
    # the file within the context window, cuz using spaces based will make some trouble
    file = file.replace("!", " ").replace(" ", "_")
    lstd: str = ""
    if file.split("_")[-1].isdigit():
        lstd = file.split("_")[-1] + "_base"

    for i in range(0, 10):
        while file.count(str(i)) != 0:
            file = file.replace(str(i), "")
    file: list[str] = file.split("_")
    if lstd != "":
        file.append(lstd)

    file = [i for i in file if len(i) != 0]

    return "_".join(file)


def scan_folder_for(
    folder: str, origin: Path = Path("."), is_normal: bool = True
) -> bool:
    """Scan for a certain folder starting from `origin`, use `is_normal` to indicate if it's
    reserved

    Args:
        folder (str): target folder
        origin (Path, optional): starter path. Defaults to Path(".").
        is_normal (bool, optional): return reserved resources or not, not both. Defaults to True.

    Returns:
        bool: was founded?
    """
    folders: list[str] = get_list_system_file("dir", origin, is_normal)
    if folder in folders:
        return True

    for name in folders:
        origin = origin / name
        if not origin.exists():
            continue

        if scan_folder_for(folder, origin, is_normal):
            return True

        origin = origin / ".."

    return False


def scan_subfolder_do[T](
    what: Callable[[Path], list[T]],
    *args,
    exclude: Sequence[str] = [],
    origin: Path = Path("."),
    **kwargs,
) -> list[T]:
    """Scan between folders and do something while that, this will also send args and kwargs to the `what` function each time

    Args:
        what (Callable[[Path], list[T]]): function that will be called per folder, the first argument will always be the actual folder
        exclude (Sequence[str], optional): names to be excluded. Defaults to [].
        origin (Path, optional): starter path. Defaults to Path(".").

    Returns:
        list[T]: depends on what returns, this will also apply it
    """

    def wrapper(ori: Path = Path(".")) -> list[str]:
        return list(
            filter(lambda x: not x in exclude, get_list_system_file("dir", ori))
        )

    final: list[T] = []
    for name in wrapper(origin):
        origin = origin / name

        if not origin.exists():
            continue

        if len(wrapper(origin)) != 0:
            final += scan_subfolder_do(
                what, exclude=exclude, origin=origin, *args, **kwargs
            )

        if len(get_list_system_file("file", origin)) != 0:
            final += what(origin, *args, **kwargs)

        origin = origin / ".."

    return final


def scan_file_compressed(
    kind: _literal_fields_exten = "image", origin: Path = Path(".")
) -> bool:
    """Scan the actual `origin` and report those files that needs compression

    Args:
        kind (_literal_fields_exten, optional): resource type. Defaults to "image".
        origin (Path, optional): starter path. Defaults to Path(".").

    Returns:
        bool: does `origin` have some file that needs compression?
    """
    if IGNORE_NOT_SUPPORTED:
        return False

    vr: list[str]
    match kind:
        case "image":
            vr = DEFAULT_EXTEND_IMAGE_NOT_SUPPORT
        case "sound":
            vr = DEFAULT_EXTEND_SOUND_NOT_SUPPORT
        case "video":
            vr = DEFAULT_EXTEND_VIDEO_NOT_SUPPORT
        case _:
            logger.warning(
                get_message_translated(MessagesError.ARGUMENT_NOT_FOUND, name=kind)
            )
            vr = DEFAULT_EXTEND_IMAGE_NOT_SUPPORT

    files = get_list_file_extended(vr, origin=origin)
    has_files = len(files) != 0
    if has_files:
        message: list[str] = [get_message_translated(MessagesError.EXTENSION_ERROR)]
        for n in files:
            message.append(
                f"\nN: {len(message)} FILE: {n} BASED {origin.resolve().as_posix()}"
            )
        message: str = mkr_str(message)
        logger.warning(message)

    return has_files


def rm_defaults(origin: Path = Path(".")) -> None:
    """Remove those files reserved by the tool (to avoid overwriting the same data or duplicates)

    Args:
        origin (Path, optional):  starter path. Defaults to Path(".").
    """
    if not __can_edit__:
        print(
            get_message_translated(
                MessagesError.FEATURE_NOT_SUPPORTED,
                name="rm_defaults",
                reason="the program can't edit/manipulate files",
            )
        )
        return

    remove_file: Path = origin

    print(
        get_message_translated(
            MessagesMeta.MESSAGE_FUNCTION_INIT, name="Remove defaults"
        )
    )
    result = "completed"
    # .copy() is fundamental to no add data to RESERVED_GENERIC_FILE_EXTEN or others
    extensions_to_delete: list[str] = RESERVED_GENERIC_FILE_EXTEN.copy()
    for file in tqdm(
        RESERVED_GENERIC_FILE_NAMES,
        colour=ColorPerLevel.INTERNAL,
        desc=get_message_translated(
            MessagesMeta.MESSAGE_FUNCTION_PROGRESS, name="Remove default"
        ),
    ):
        try:
            if file in RESERVED_GENERIC_CREA_NAMES:
                extensions_to_delete += RESERVED_GENERIC_CREA_EXTEN

            for extension in extensions_to_delete:
                remove_file = remove_file.joinpath(file + "." + extension)
                if not (remove_file.exists() and remove_file.is_file()):
                    continue

                remove(remove_file)
        except FileNotFoundError:
            logger.warning(
                get_message_translated(MessagesError.FILE_NOT_FOUND, file=file)
            )
        except Exception as e:
            result = "unknown error"
            logger.warning(
                get_message_translated(
                    MessagesMeta.MESSAGE_INFO,
                    name=file,
                    operation="Remove defaults",
                    result=str(e),
                )
            )
    print(
        get_message_translated(
            MessagesMeta.MESSAGE_FUNCTION_ENDED, name="Remove defaults", result=result
        )
    )


########################################################
#
# Functionally related zone
#
########################################################
def get_name_acron(limit: int = 3, origin: Path = Path(".")) -> str:
    """get the short or acronimun name for a character based either in their folder if the character.rpy couldn't be found... or the
    character.rpy file itself

    Args:
        limit (int, optional): limit of try to get the name before parse the folder. Defaults to 3.
        origin (Path, optional): starter path. Defaults to Path(".").

    Returns:
        str: the shortest name possible (if declared) or the folder's name
    """
    files_waited = RESERVED_GENERIC_FILE_NAMES[
        0:2
    ]  # character.rpy and its plural just in case
    _: Path = origin

    _tmp_file: list[str]
    file_acron: str = ""

    for i in tqdm(
        range(limit),
        colour=ColorPerLevel.INTERNAL,
        desc=get_message_translated(
            MessagesMeta.MESSAGE_FUNCTION_PROGRESS, name="getting acron"
        ),
    ):
        _tmp_file = get_list_file_named(files_waited, False, origin=_)

        if len(_tmp_file) != 0:
            file_acron = _tmp_file[0]
            break
        _ = _ / ".."

    _ = _ / file_acron
    file_found: bool = not i + 1 >= limit or file_acron != ""
    is_empty: bool
    try:
        is_empty = not (_.is_file and _.exists() and _.open().readlines() != 0)
    except PermissionError:
        is_empty = True
    manual_use: bool = False
    if file_found and not is_empty:
        for line in _.open().read().split(","):
            a = line.split("=")
            del_jump(a)
            if a[0].replace(" ", "") == "image":
                file_acron = a[1].replace('"', "").replace(")", "")
                break
    else:
        manual_use = True
        logger.warning(
            get_message_translated(
                MessagesMeta.MESSAGE_FUNCTION_ENDED,
                name="get_character_acron",
                result="character's file couldn't be found in "
                + str(_)
                + " based on "
                + str(origin),
            )
        )

    if manual_use or file_acron == "":
        file_acron = get_path_parsed(DEFAULT_PATH_IMAGE.split("/")[1], origin)[1][:2]
    print(
        get_message_translated(
            MessagesMeta.MESSAGE_FUNCTION_ENDED,
            name="get_character_acron",
            result="founded and used with " + file_acron,
        )
    )
    return file_acron


def get_list_namesimple(origin: Path = Path(".")) -> list[str]:
    """Get the simple part of origin and return it as `list[str]`

    Args:
        origin (Path, optional): starter path. Defaults to Path(".").

    Returns:
        list[str]: simple part
    """
    names: list[str] = []
    for name in get_list_system_file("dir", origin):

        if name in RESERVED_GENERIC_FOLD_NAMES[:-1]:
            continue

        origin = origin / name
        if not origin.exists():
            continue

        [
            names.append(get_path_parsed(DEFAULT_RESOURCE_PATH, origin) + "/" + _name)
            for _name in get_list_file_extended(
                DEFAULT_EXTEND_IMAGE_SUPPORT, origin=origin
            )
        ]

        if len(get_list_system_file("dir")) != 0:
            names += get_list_namesimple(origin)
        origin = origin / ".."
    return names


def get_name_template(
    file: str, path: str, mode: ParseKeywords, limit: int = DEFAULT_NAME_LIMIT
) -> tuple[str, str]:
    """Given the file and path, this will parse it base in the selected mode, this has a limit of character that you
    can customize with the `limit` parameter

    the return mostly depends on `BUILDIN_FILE_TEMPLATES` var

    Args:
        file (str): file
        path (str): path
        mode (ParseKeywords): mode based in `ParseKeywords`.
        limit (int, optional): limit of characters. Defaults to `DEFAULT_NAME_LIMIT`.

    Returns:
        tuple[str, str]: the file and path parsed by `ParseKeywords`
    """
    file, extend = file.split(".", 1)
    file = file.translate(FILE_NAME_REPLACE)
    for origin, to in FILE_NAME_REPLACE_LONG.items():
        file.replace(origin, to)

    info: dict[str, str] = {"path": path, "file": file + "." + extend}
    couldnt_found: bool = False
    match DEFAULT_KIND_IMPORT:
        case "dev":  # normal import
            path = BUILDIN_FILE_TEMPLATES[TemplatePath.NORMAL]
        case "source":  # when encrypted
            path = BUILDIN_FILE_TEMPLATES[TemplatePath.ENCRYPT]
        case (
            "zip"
        ):  # when exported as .zip file, your renpy SDK should support this feature
            if not TemplateKeys.ZIPLOAD in FORMATS_IMPORTED:
                path = BUILDIN_FILE_TEMPLATES[TemplatePath.NORMAL]
                logger.warning(
                    get_message_translated(
                        MessagesError.ARGUMENT_NOT_FOUND, name=TemplateKeys.ZIPLOAD
                    )
                )
                couldnt_found = True
            else:
                path = BUILDIN_FILE_TEMPLATES[TemplatePath.ZIP]
        case _:
            path = BUILDIN_FILE_TEMPLATES[TemplatePath.NORMAL]
            couldnt_found = True

    if couldnt_found:
        logger.warning(
            get_message_translated(
                MessagesError.INCORRECT_ARGUMENTS,
                arguments=DEFAULT_KIND_IMPORT,
                default=TemplatePath.NORMAL,
                message="get_name_template",
            )
        )
    # fix from here:
    # https://github.com/SpikeInterface/spikeinterface/blob/7268ab900443ca3f0239de3007352d05f2d7d875/spikeinterface/sorters/runsorter.py#L203#L203
    if system() == "Windows":
        rt = Path(str(ROOT_EXE_GAME)[str(ROOT_EXE_GAME).find(":") + 1 :])
    else:
        rt = ROOT_EXE_GAME

    path = (path % info).replace(rt.as_posix(), "").replace("C:/", "")
    match mode:
        case ParseKeywords.FILE:
            pass  # ?
        case ParseKeywords.FOLDER:
            ref = []
            if len(path.split("/")) <= limit:
                ref = [path.split("/")[-1]]
            else:
                ref = path.split("/")[limit:]

            file = " ".join(ref).split(".")[0]
        case _:
            pass

    return file, path


def write_chipher_images(origin: Path = Path(".")):
    """Soon

    .. todo::
        this function doesn't exits.... based in 1.0.5.0 version

    Args:
        origin (Path, optional): starter path. Defaults to Path(".").
    """
    pass

########################################################
#
# Writers related zone
#
########################################################

def write_side_image(
    size: tuple[int, int, int, int],
    load: dict[TemplatePathKeys, str | list[str]],
    file_generation_limit: int = 99,
) -> bool:
    """This will create a side folder based from `TemplatePathKeys.BASE` in `load` and skip if the name contains
    certain parts in `TemplatePathKeys.NAME`

    Args:
        size (tuple[int, int, int, int]): dimension in LX, LY, RX, RY
        load (dict[TemplatePathKeys, str  |  list[str]]): basically someone didn't want to use arguments as a normal person, so `TemplatePathKeys` exits
        file_generation_limit (int, optional): limit for files. Defaults to 99.

    Returns:
        bool: did it worked?
    """
    if not __can_edit__ or not (
        has_feature(FeaturesKeywords.IMAGE_CREATION)
        or has_feature(FeaturesKeywords.IMAGE_CREATION, False)
    ):
        logger.warning(
            get_message_translated(
                MessagesError.FEAUTRE_NOT_FOUND, name="write_side_image"
            )
        )
        return False

    try:
        size = [int(i) for i in size]
    except TypeError as msg:
        print(
            get_message_translated(
                MessagesMeta.MESSAGE_INFO,
                name="write_side_image",
                operation="int convertion",
                result=msg.args,
            )
        )
        size = DEFAULT_SIZE_CORP_VAR

    # check the fields required (just in case)
    # if not has_required_keys(load.keys(), TemplatePathKeys):
    #    return False

    if not TemplatePathKeys.BASE in load:
        return False
    origin: Path = Path(DEFAULT_PATH_SIDE % load).resolve()
    if not (origin / "..").exists():
        return False

    _ = (origin / "..").resolve()

    if not _.exists():
        return False

    files: list[str] = get_list_system_file("file", origin=_)[:file_generation_limit]
    try:
        if origin.as_posix().split("/")[-1] == "side":
            rmtree(origin)
        else:
            print(
                get_message_translated(
                    MessagesMeta.MESSAGE_INFO,
                    name="delete",
                    operation="remove side folder",
                    result="cancel by path: " + origin.as_posix(),
                )
            )
    except FileNotFoundError:
        pass

    print(
        get_message_translated(
            MessagesMeta.MESSAGE_FUNCTION_INIT, name="write_side_image"
        )
    )
    mkr_dir("side", _)
    has_error: bool = False

    file_path_side: Path
    file_path_orin: Path

    for file in tqdm(
        files,
        colour=ColorPerLevel.INTERNAL,
        desc=get_message_translated(
            MessagesMeta.MESSAGE_FUNCTION_PROGRESS,
            name="write side images for " + load[TemplatePathKeys.NAME],
        ),
    ):
        file_path_side = origin / file  # with '/side'
        file_path_orin = _ / file  # without '/side'

        if not file_path_orin.exists():
            logger.warning(
                get_message_translated(
                    MessagesError.PATH_NOT_FOUND, path=file_path_orin.as_posix()
                )
            )
            continue

        try:
            Image.open(file_path_orin).crop(size).save(file_path_side)
        except (UnidentifiedImageError, ValueError, OSError) as msg:
            logger.warning(
                get_message_translated(
                    MessagesMeta.MESSAGE_FUNCTION_ENDED,
                    name="write_side_image",
                    result=msg.args,
                )
            )
            has_error = True
    print(
        get_message_translated(
            MessagesMeta.MESSAGE_FUNCTION_ENDED,
            name="write_side_image",
            result=f"ERROR: {"yes" if has_error else "no"}",
        )
    )
    return not has_error


def write_common_file(
    modes: list[str],
    info: ConfigParser,
    origin: Path = Path("."),
    folders: list[str | Path] = [""],
) -> None:
    """this is one of the core functions of this tool, it basically takes a series of modes (mostly based from `TemplatePath`, `ImportKeywords`,
    `ParseKeywords`, `ProccesKeywords` and so on) based on their `origin`, this will apply differents procces for each individual case, but always running as a single function

    this function does actually write a common.rpy file, but it doesn't scan and evaluate files, that's `mkr_lines_list`'s job

    How it works
    --------

    first of all, we need the modes, for example

    ```python
    [
        ParseKeywords.FILE,

        TemplateKeys.NORMAL,

        ImportKeywords.IMAGES,
    ]
    ```

    with these mode, we are telling the function to write in a __file format__ (`ParseKeywords.FILE`), enabling it
    to use a __normal template__ (`TemplateKeys.NORMAL`), and the resources are __images__ (`ImportKeywords.IMAGES`)

    .. tip::
        alway remember to check what each one of these modes/keywords means, since
        in most cases what it says, it's what it does, except if it's explained the otherwise

    then we have the `info`, which is basically a config windows-like file, this makes use of `ImageConfigHead` and hereby  `ImageConfigValue` as well

    `origin` it's the same as `folders`, but `origin` is the starter path, then `folders` are some folders where you want to repliacte the same procces
    using `modes`, these ones could be relative to `origin` or absolute, in whichever case, it's already considered both cases as individuals

    .. note::
        a side note, `modes` basically controlls how the function and `mkr_lines_list` (also the other functions that relies on `modes` and their enums)
        behave, within `origin` and others, there are some mechanism to assume information, such as determine the file of `origin` in case `ImportKeywords` wasn't provided

        an so other part, but esscencialy, you must indicate one `ParseKeywords` and `TemplateKeys` at least to make this function do something

    Args:
        modes (list[str]): modes to work with (based in different enums)
        info (ConfigParser): config window-like file
        origin (Path, optional): starter path. Defaults to Path(".").
        folders (list[str  |  Path], optional): folders to replicate `modes` behavior. Defaults to [""].

    """
    if info == None:
        info = ConfigParser()

    if isinstance(origin, str):
        origin = Path(origin)

    if not origin.exists():
        logger.warning(
            get_message_translated(
                MessagesError.PATH_NOT_FOUND, path=origin.resolve().as_posix()
            )
        )
        return
    kind: _literal_fields_exten
    extend: list[str]

    files: list[str]

    if ImportKeywords.IMAGES in modes:
        kind = "image"
    elif ImportKeywords.SOUNDS in modes:
        kind = "sound"
    elif ImportKeywords.VIDEOS in modes:
        kind = "video"
    else:
        # smart way to get the file's type based
        files = scan_subfolder_do(
            lambda x: (
                get_list_system_file("file")
                if len(get_list_system_file("file")) != 0
                else []
            ),
            origin=origin,
        )
        # yet, not the smartest way possible
        if len(files) != 0 and files[0].count(".") != 0:
            extension: str = files[0].split(".")[1]

            match extension:
                case x if x in DEFAULT_EXTEND_IMAGE_SUPPORT:
                    kind = "image"
                case x if x in DEFAULT_EXTEND_SOUND_SUPPORT:
                    kind = "sound"
                case x if x in DEFAULT_EXTEND_VIDEO_SUPPORT:
                    kind = "video"
                case _:
                    kind = "image"
        else:
            kind = "image"

        logger.warning(
            get_message_translated(
                MessagesError.INCORRECT_ARGUMENTS,
                arguments=str(modes),
                default=kind,
                message=origin.as_posix(),
            )
        )

    match kind:
        case "image":
            extend = DEFAULT_EXTEND_IMAGE_SUPPORT + (
                DEFAULT_EXTEND_IMAGE_NOT_SUPPORT if ProccesKeywords.NOTHING else []
            )
        case "sound":
            extend = DEFAULT_EXTEND_SOUND_SUPPORT + (
                DEFAULT_EXTEND_SOUND_NOT_SUPPORT if ProccesKeywords.NOTHING else []
            )
        case "video":
            extend = DEFAULT_EXTEND_VIDEO_SUPPORT + (
                DEFAULT_EXTEND_VIDEO_NOT_SUPPORT if ProccesKeywords.NOTHING else []
            )
        case _:
            # TODO:
            return

    scan_file_compressed(kind, origin)
    rm_defaults(origin)

    resource_path = (
        DEFAULT_PATH_IMAGE
        if kind == "image"
        else (DEFAULT_PATH_SOUND if kind == "sound" else DEFAULT_PATH_VIDEO)
    )

    if resource_path.count("%(base)s") == 0:
        logger.critical(
            get_message_translated(
                MessagesMeta.MESSAGE_FUNCTION_ENDED,
                name="write_common_file",
                result="%(base)s not found",
            )
        )
        return

    resource_path %= {"base": DEFAULT_RESOURCE_PATH}
    simple_path_base = get_path_parsed(resource_path.split("/"), origin)

    if len(simple_path_base.split("/")) <= 1:
        logger.warning(
            get_message_translated(
                MessagesMeta.MESSAGE_FUNCTION_ENDED,
                name="write_common_file",
                result=simple_path_base,
            )
        )
        return

    size_side: tuple[int, int, int, int] = ()
    size_square: tuple[str, str] = ()
    _size_scale: str = info.get(
        ImageConfigHead.SCALE, ImageConfigValue.DIMENSION, fallback=DEFAULT_SIZE_SCREEN
    )
    if _size_scale.count("x") != 1:
        _size_scale = DEFAULT_SIZE_SCREEN

    size_scale: tuple[int, int]
    try:
        size_scale = tuple([int(x) for x in _size_scale.split("x")])
    except TypeError:
        # TODO: add error message
        size_scale = tuple([int(x) for x in DEFAULT_SIZE_SCREEN.split("x")])
    size_scale = [str(i) for i in size_scale]
    use_side: bool = False

    if ProccesKeywords.SIDE in modes:
        size_side = info.get(
            ImageConfigHead.SIDE,
            ImageConfigValue.SIZE,
            fallback=DEFAULT_SIZE_CORP_VAR,
        )
        size_square = info.get(
            ImageConfigHead.SIDE,
            ImageConfigValue.SQUARE,
            fallback=DEFAULT_SIZE_SIDE_VAR,
        ).split("x")

    if ProccesKeywords.SUBFOLDER in modes:
        folders += get_list_subfolders(origin)
    if has_feature(FeaturesKeywords.SIDE_GENERATION) and ProccesKeywords.SIDE in modes:
        use_side = True
        for folder in folders:
            if folder == "":
                folder = origin
            simple_path = folder.as_posix()
            write_side_image(
                size_side,
                {
                    TemplatePathKeys.BASE: simple_path,
                    TemplatePathKeys.NAME: simple_path.split("/", 1)[1].split("/")[-1],
                },
            )

    _path: Path = origin
    abbr = get_name_acron(origin=origin) if kind == "image" else "etc"
    if abbr == "":
        abbr = "rdnd"
    # HACK: this might be more a TODO than a HACK, but somebody
    # need to take care of those Enums in order to make it similar and not a
    # single letter
    modes.append(
        [
            kind,
            (size_square if len(size_square) != 0 else DEFAULT_SIZE_SIDE_VAR),
            ",".join(size_scale),
            use_side,
        ]
    )
    lines = []

    for folder in folders:
        if folder == "":
            _path /= "."
        else:
            _path = folder
        _path = _path.resolve()

        if not _path.exists():
            continue

        files = (
            get_list_file_extended(
                extend, origin=_path, local=get_list_system_dirs(_path)
            )
            if ProccesKeywords.IGNORE in modes
            else get_list_file_extended(extend, origin=_path)
        )
        # NOTE: yeah, this sucks
        simple_path_base = get_path_parsed(resource_path.split("/"), _path)
        print(Fore.RESET)
        print(
            Fore.BLUE
            + get_message_translated(
                MessagesMeta.MESSAGE_FUNCTION_INIT, name=simple_path_base
            )
        )
        _ = mkr_lines_list(simple_path_base, abbr, files, modes, _path)
        print(
            Fore.RED
            + get_message_translated(
                MessagesMeta.MESSAGE_FUNCTION_ENDED,
                name=simple_path_base,
                result="completed" if len(_) != 0 else "incompleted",
            )
        )
        _.append("\n")
        lines.extend(_)
    print(Fore.RESET)
    if __can_edit__:
        open(
            origin
            / ("common_dist.py" if DEFAULT_KIND_IMPORT == "zip" else "common.rpy"),
            "w",
        ).writelines(lines)
        print("Common created in ", origin, "\n")


_to_change_statements = dict[str, tuple[str, str, str, int]]
_statements_used = dict[str, dict[str, dict[str, list[int]]]]


def write_names(
    sprites: Path = Path("."), game_data: Path = Path(".")
) -> tuple[SearchEngine, _to_change_statements, _statements_used]:
    """this function basically gets all declarations used within the chapters files, basically its a helper to rename
    all declarations used for a certain file

    Args:
        sprites (Path, optional): sprite folder. Defaults to Path(".").
        game_data (Path, optional): game data folder. Defaults to Path(".").

    Returns:
        tuple[SearchEngine, _to_change_statements, _statements_used]: information (maybe not the best return lol)
    """
    # get each character's aliases
    folders = get_list_system_dirs(sprites, "dir")
    alias = []
    for folder in folders:
        alias.append(get_name_acron(origin=(sprites / folder)))

    lines_used = scan_lines_chapters(alias, game_data)
    lines_origin = scan_lines_common(game_data)

    # used to query where the files come from
    engine_origin = SearchEngine(
        Schema(
            path_simple=TEXT(stored=True),
            path_str=TEXT(stored=True),
            name=TEXT(stored=True),
            whole=TEXT(stored=True),
            path_whole=TEXT(stored=True),
        )
    )
    # used to query where the files are being used
    engine_useded = SearchEngine(
        Schema(
            field=TEXT(stored=True),
            file=TEXT(stored=True),
            where=TEXT(stored=True),
        )
    )

    origin_base = []
    # parse the origin info into something woosh can use
    for folder, common in lines_origin.items():
        # path, name, whole, path (whole)
        for line in common:
            s_line = line.replace("\n", "")
            if len(s_line.replace(" ", "")) == 0 or line[0] == "#":
                continue
            # TODO: make checks to ensure this shit have the correct format
            try:
                path = line.split("=", 1)[1].split('"', 1)[1].split('"', 1)[0]
            except IndexError:
                continue

            origin_base.append(
                {
                    "path_simple": path,  # assets/images/Xellar/.....
                    "path_str": " ".join(
                        path.split("/")
                    ),  # same as path_simple, but with spaces
                    "name": line.split("=", 1)[0]
                    .split(" ", 1)[1]
                    .replace("_", " "),  # xellar_normal_speak
                    "whole": line,  # define xellar_normal_speak = ......
                    "path_whole": folder.as_posix(),  # c:/Users/[USER]/.....
                }
            )
    useded_base = []
    for file, field in lines_used.items():

        for zone, use in field.items():

            for s_use in list(use.keys()):
                useded_base.append({"field": zone, "file": file, "where": s_use})
    engine_origin.index_documents(origin_base)
    engine_useded.index_documents(useded_base)

    to_change: dict[str, tuple[str, str, str, int]] = {}
    print(
        Fore.RED
        + "AFTER YOU END THIS PROCCES, THE CHANGES WILL BE APPLIED"
        + Fore.RESET
    )
    while True:

        result = engine_origin.query(
            input("Insert a name or its path\n>..."),
            ["name", "path_simple", "path_str"],
            False,
        )

        if len(result) != 0:
            print("Use -1 to cancel this query")
            print("ID <--------> INFO")
            for _id, info in zip(range(len(result)), result):
                print(
                    "Given the ID"
                    + Fore.GREEN
                    + f" {_id}"
                    + Fore.RESET
                    + ":"
                    + f"\
                    \nDefinition used: {info["name"]} \
                    \nPath used: {info["path_simple"]} \n"
                )

            try:
                _id = int(input("Insert ID to modify\n>..."))
            except (ValueError, TypeError):
                _id = -1

            if _id < 0 or _id > len(result):
                continue

            info = result[_id]

            print(
                "Actual file name: "
                + Fore.BLUE
                + f"{info["path_simple"].split("/")[-1]}"
                + Fore.RESET
                + "\n"
            )
            new_name = input(
                "Insert the new "
                + Fore.RED
                + "file name"
                + Fore.RESET
                + ", just the name, not the extension\n>..."
            )
            to_change[info["name"]] = (  # [file]
                new_name,  # file
                info["path_simple"],  # game/images/Sprites/ailstair/[file].png
                info["path_whole"],  # Path to common (not include common.rpy itself)
                lines_origin[Path(info["path_whole"])].index(
                    info["whole"]
                ),  # line where it's located
            )
        else:
            print("nothing found!")

        if not input("Continue making querys?\n") in ["y", "yes"]:
            break

    if (
        __can_edit__
        and input(
            "Are you 100% you want to rename "
            + str(len(to_change))
            + " files?\
            \n"
            + Fore.RED
            + "TIHS CAN'T BE UNDONE, ARE YOU SURE?"
            + Fore.RESET
            + "\n>..."
        )
        in ["yes", "y"]
    ):

        for values in to_change.values():
            new = values[1].split("/")
            new[-1] = values[0] + "." + new[-1].split(".")[-1]
            new = "/".join(new)
            print(
                f"The file {Fore.RED + values[1].split("/")[-1] + Fore.RESET} will be renamed to {Fore.RED + new.split("/")[-1] + Fore.RESET} in {values[1]}"
            )
            try:
                rename(Path(values[1]).resolve(), Path(new))
            except Exception as e:
                print(e)

    return engine_useded, to_change, lines_used


########################################################
#
# Lines generated related zone
#
########################################################
def mkr_lines_list(
    simple_path: str,
    abbr: str,
    files: list[str],
    modes: list[str],
    folder: Path = Path("."),
) -> list[str]:
    """This function works better when `write_common_file` call it, yet, you can still used, this requires the simple path
    from `origin` (which you can get using `get_path_parsed`), the abbreviation (using `get_name_acron`) and the list of files within the simple
    path, this must be name only the file's name, or folder(s) + file relative to `origin` (or the same, simple_path)

    for more info about modes, check `write_common_file` where it's better explained

    and folder which is used to validate simple_path

    Args:
        simple_path (str): the simpliest representation of a path, being (for example) assets/image/Xellar
        abbr (str): abbreviation of the folder
        files (list[str]): a collection of files
        modes (list[str]): modes to work with (based in different enums)
        folder (Path, optional): the actual folder. Defaults to Path(".").

    Raises:
        TypeError: raised if some template within `FORMATS_IMPORTED` is incorrect formatted or is an unsupported object type

    Returns:
        list[str]: a collection of lines that represent the declaration of a common.rpy file

    """
    # NOTE: well... this is mostly a TODO than a NOTE, but... I think we could do better if we
    # check simple_path and folder, there might be a case where they might are not realted
    # since this function excepts both be related to the other
    lines: list[str] = []
    if abbr in ["", "rdnd"]:
        abbr = get_name_acron(origin=folder)
    kind, size_side, size_scale, use_side = modes[-1]

    all_payload: dict[str, list[dict[str, str]]] = {}
    payload: dict[str, str]
    file_name: str
    file_simple_path: str

    def parse_line_recursive(load: dict[str, str], line: list | str) -> str:
        _tmp = []
        if isinstance(line, list):
            for n in line:
                _tmp.append(parse_line_recursive(load, n))
        elif isinstance(line, str):
            _tmp.append(line % load)
        else:
            raise TypeError("Unsupported type: " + str(type(line)))
        return "\n".join(_tmp)

    print(Fore.RESET)
    result = "not found"
    # get possible payloads
    for file in tqdm(
        files,
        colour=ColorPerLevel.GENERIC,
        desc=get_message_translated(
            MessagesMeta.MESSAGE_FUNCTION_PROGRESS, name="Parsing names..."
        ),
    ):
        file_name, file_simple_path = get_name_template(
            file,
            simple_path,
            (
                ParseKeywords.FILE
                if ParseKeywords.FILE in modes
                else ParseKeywords.FOLDER
            ),
        )
        file_name = get_name_parsed(file_name)

        payload = {
            "name": file_name,
            "path": file_simple_path,
            "abbr": abbr,
            "kind": kind,
            "tab": " " * DEFAULT_TAB,
            "size_side": ", ".join(size_side),
            "size_scale": size_scale,
        }
        is_animated = (
            len(file_name.split("_")) >= 2 and file_name.split("_")[-2].isdigit()
        )
        parsed_name = ""
        if is_animated:
            parsed_name = "_".join(file_name.split("_")[:-2])
        else:
            parsed_name = file_name

        if not parsed_name in all_payload:
            all_payload[parsed_name] = []
        all_payload[parsed_name].append(payload)
        result = "completed"

    print(
        get_message_translated(
            MessagesMeta.MESSAGE_FUNCTION_ENDED, name="Parsing names...", result=result
        )
    )

    real_keys = [key for key in FORMATS_IMPORTED if key in modes]
    if ProccesKeywords.ANIMATED in modes:
        real_keys.append(ProccesKeywords.ANIMATED)

    for group, payloads in all_payload.items():
        can_procces_animations = (
            ProccesKeywords.ANIMATED in real_keys and len(payloads) > 1
        )

        print(
            get_message_translated(
                MessagesMeta.MESSAGE_FUNCTION_INIT, name=f"Creating lines for '{group}'"
            )
        )
        result = "not proccesed"

        for key in FORMATS_IMPORTED:
            if not key in real_keys:
                continue

            anima_key = is_animated_name(group)

            # animation special
            if (
                can_procces_animations
                and anima_key == key
                and isinstance(FORMATS_IMPORTED[key], list)
            ):
                is_animation = FORMATS_IMPORTED[key][0]
                if is_animation == True:
                    _0 = []

                    for line in FORMATS_IMPORTED[key][1:]:

                        if isinstance(line, list):
                            instructions = line[0].split("+")
                            # NOTE: here should more cases
                            if ImageConfigValue.REPEAT in instructions:
                                for info in payloads:
                                    for n in line[1:]:
                                        _0.append(parse_line_recursive(info, n))
                        else:
                            _0.append(
                                line
                                % {
                                    "name": group,
                                    "tab": " " * DEFAULT_TAB,
                                }
                            )
                    _0.append("\n")
                    lines.append("\n".join(_0))
                    continue

            if isinstance(FORMATS_IMPORTED[key], list) and FORMATS_IMPORTED[key][0]:
                continue

            if isinstance(FORMATS_IMPORTED[key][0], bool):
                ref = FORMATS_IMPORTED[key][1:]
            else:
                ref = FORMATS_IMPORTED[key]

            # others
            for payload in tqdm(
                payloads,
                colour=ColorPerLevel.GENERIC,
                desc=get_message_translated(
                    MessagesMeta.MESSAGE_FUNCTION_PROGRESS, name="Writing..."
                ),
            ):
                # special case... lol
                if use_side and key == TemplateKeys.SIDE:
                    payload = payload.copy()
                    _tmp_path = payload["path"].split("/")
                    _tmp_path.insert(-1, "side")
                    payload["path"] = "/".join(_tmp_path)

                lines.append(parse_line_recursive(payload, ref))
            result = "completed"

        print(
            get_message_translated(
                MessagesMeta.MESSAGE_FUNCTION_ENDED,
                name=f"Creating lines for '{group}'",
                result=result,
            )
        )
    return lines

########################################################
#
# Scanner related zone
#
########################################################
IMAGE_KEYWORDS: list[str] = ["scene", "show", "hide"]
"""
Basically this is used as reference by `scan_lines_chapters` to differenciate 
certain statements within the renpy language alonside with `SOUND_KEYWORDS`
"""
SOUND_KEYWORDS: list[str] = ["play"]
"""
Basically this is used as reference by `scan_lines_chapters` to differenciate 
certain statements within the renpy language alonside with `IMAGE_KEYWORDS`
"""


def scan_lines_chapters(
    aliases: list[str], origin: Path = Path(".")
) -> dict[str, dict[str, dict[str, list[int]]]]:
    """This basically takes those chapter files and look for certain statements that used resources (like images, sound, video, etc...) and
    register their locations for later use, the origin should be data folder (or basically ./game) folder

    the structure is basically

    ```python
    {
        "file": {
            "resource type": {
                "statement": [0, 2, 3]
            }
        }#where each number is where the statement is being used
    }
    ```

    Args:
        aliases (list[str]): mostly belongs to character
        origin (Path, optional): path starter. Defaults to Path(".").

    Returns:
        dict[str, dict[str, dict[str, list[int]]]]: the representation of info
    """
    files: list[str] = get_list_file_extended(
        RESERVED_GENERIC_CREA_EXTEN, origin=origin
    )
    all_files_usage: dict[str, dict[str, dict[str, list[int]]]] = {}

    for file in files:
        s_file = file.split(".")[0]
        all_files_usage[s_file] = {}

        for _ in ["image", "video", "sound"]:
            all_files_usage[s_file][_] = {}

        c_l = 0
        for line in open(origin / file, "r", encoding="utf-8").readlines():
            s_line = line.replace("\n", "")
            c_l += 1
            if len(s_line.replace(" ", "")) == 0:
                continue

            c_s = 0
            while s_line[c_s] == " ":
                c_s += 1
            s_line = s_line[c_s:]

            field = ""
            match s_line.split(" ")[0]:
                case x if x in aliases + IMAGE_KEYWORDS:
                    field = "image"
                case x if x in SOUND_KEYWORDS:
                    field = "sound"

            if field == "":
                continue

            if not s_line in all_files_usage[s_file]:
                all_files_usage[s_file][field][s_line] = []

            all_files_usage[s_file][field][s_line].append(c_l)

    return all_files_usage


def scan_lines_common(origin: Path = Path(".")) -> dict[Path, list[str]]:
    """Basically this will search trought the whole `DEFAULT_RESOURCE_PATH` folder to look for commmon files,
    get their content and then save their definitions __individually__ in the form of

    ```python
    {
        "path/to/common/file": [
            "define xellar = ....",
            "define xellar_happy = ...."
        ] # and so for each thing
    }
    ```

    this for later use

    Args:
        origin (Path, optional): path starter. Defaults to Path(".").

    Returns:
        dict[Path, list[str]]: all files with their contents
    """
    all_files_usage = {}
    folders = get_list_subfolders(origin)
    # get all folders that have a common.rpy file
    for folder in folders.copy():
        if (
            len(
                get_list_files(
                    RESERVED_GENERIC_CREA_NAMES,
                    [RESERVED_GENERIC_CREA_EXTEN],
                    False,
                    origin=folder,
                )
            )
            == 0
        ):
            folders.remove(folder)

    # get its contents
    for folder in folders:
        # s_folder = folder.as_posix().split("/")[-1]

        all_files_usage[folder] = open(
            folder
            / (RESERVED_GENERIC_CREA_NAMES[0] + "." + RESERVED_GENERIC_CREA_EXTEN),
            "r",
            encoding="utf-8",
        ).readlines()

    return all_files_usage


########################################################
#
# Import specific related zone (useless)
#
########################################################
def _aux_import_(
    is_audio: bool, origin: Path = Path("."), single: bool = False
) -> None:
    """A generic function with the essecential modes for a simple import for audio & video folders

    Args:
        is_audio (bool): is audio?
        origin (Path, optional): path starter. Defaults to Path(".").
        single (bool, optional): limit `write_common_file` to only the origin. Defaults to False.
    """
    folders: list[str] = [origin]
    if not single:
        folders.extend(get_list_system_file("dir", origin=origin))

    for folder in folders:
        write_common_file(
            [
                ParseKeywords.FOLDER,
                ProccesKeywords.SUBFOLDER,
                ProccesKeywords.NOTHING,
                TemplateKeys.SOUND if is_audio else TemplateKeys.VIDEO,
                ImportKeywords.SOUNDS if is_audio else ImportKeywords.VIDEOS,
            ],
            None,
            folder,
        )


def import_audio(origin: Path = Path("."), single: bool = False) -> None:
    """Entry point to import stuff from `DEFAULT_PATH_SOUND` folder

    Args:
        origin (Path, optional): patyh starter. Defaults to Path(".").
        single (bool, optional):  limit `write_common_file` to only the origin. Defaults to False.
    """
    _aux_import_(True, origin, single)


def import_video(origin: Path = Path("."), single: bool = False) -> None:
    """Entry point to import stuff from `DEFAULT_PATH_VIDEO` folder

    Args:
        origin (Path, optional): patyh starter. Defaults to Path(".").
        single (bool, optional):  limit `write_common_file` to only the origin. Defaults to False.
    """
    _aux_import_(False, origin, single)


# generic function
def import_backgrounds(origin: Path = Path(".")) -> None:
    """Entry point to import stuff from `DEFAULT_PATH_IMAGE` folder, but for background

    Args:
        origin (Path, optional): patyh starter. Defaults to Path(".").
    """
    folders: list[str] = [origin]
    folders.extend(get_list_subfolders(origin))

    for folder in folders:
        write_common_file(
            [
                ParseKeywords.FOLDER,
                ProccesKeywords.SUBFOLDER,
                ProccesKeywords.NOTHING,
                TemplateKeys.SCALE,
                ImportKeywords.IMAGES,
            ],
            None,
            folder,
        )


# specific function
def import_sprites(origin: Path = Path("."), single: bool = False):
    """Entry point to import stuff from `DEFAULT_PATH_IMAGE` folder, but for sprites

    Args:
        origin (Path, optional): patyh starter. Defaults to Path(".").
        single (bool, optional):  limit `write_common_file` to only the origin. Defaults to False.
    """
    folders: list[str] = []
    if single:
        folders.append(origin)
    else:
        folders.extend(get_list_subfolders(origin=origin))

    for folder in folders:
        info = None
        if (Path(folder) / RequiredFiles.INFO).exists():
            info = ConfigParser()
            if len(info.read(Path(folder) / RequiredFiles.INFO, "utf-8")) == 0:
                info = None

        write_common_file(
            [
                ParseKeywords.FILE,
                ProccesKeywords.ANIMATED,
                ProccesKeywords.SIDE,
                TemplateKeys.ANIMATED_BLINK_NORMAL,
                TemplateKeys.ANIMATED_ANIMATED_BODY,
                TemplateKeys.SIDE,
                TemplateKeys.NORMAL,
                ImportKeywords.IMAGES,
            ],
            info,
            folder,
        )

########################################################
#
# Entry points related zone
#
########################################################

_default_audio = Path("./game/" + DEFAULT_PATH_SOUND % {"base": DEFAULT_RESOURCE_PATH})
_default_video = Path("./game/" + DEFAULT_PATH_VIDEO % {"base": DEFAULT_RESOURCE_PATH})
_default_sprite = Path(
    "./game/" + DEFAULT_PATH_IMAGE % {"base": DEFAULT_RESOURCE_PATH} + "/characters"
)
_default_background = Path(
    "./game/" + DEFAULT_PATH_IMAGE % {"base": DEFAULT_RESOURCE_PATH} + "/world"
)


def handler(origin: ArgumentsGiven):
    """Basically a handler that after `frame` was used, checks for the origin arguments and perform certain proccess

    Args:
        origin (ArgumentsGiven): a bunch of arugments
    """
    game_data: Path = origin.game
    _0 = {"base": game_data / DEFAULT_RESOURCE_PATH}

    assets_info = ArgumentsGiven(
        _0["base"],
        Path(
            DEFAULT_PATH_SOUND % _0 if _default_audio == origin.audio else origin.audio
        ),
        Path(
            DEFAULT_PATH_VIDEO % _0 if _default_video == origin.video else origin.video
        ),
        Path(
            (DEFAULT_PATH_IMAGE % _0) + "/characters"
            if _default_sprite == origin.sprite
            else origin.sprite
        ),
        Path(
            (DEFAULT_PATH_IMAGE % _0) + "/world"
            if _default_background == origin.background
            else origin.background
        ),
        None,
        None,
        None,
        None,
        None,
    )

    if origin.can_generate_side:
        add_feature(FeaturesKeywords.SIDE_GENERATION)

    def import_all():
        nonlocal assets_info
        import_audio(assets_info.audio)
        import_video(assets_info.video)
        import_sprites(assets_info.sprite)
        import_backgrounds(assets_info.background)

    change_handler = ()
    if origin.use_renamer:
        change_handler = write_names(assets_info.sprite, game_data)

    # renamer was used
    if len(change_handler) != 0:
        # here we compared all original date with the modded one
        new_steps = scan_lines_common(game_data)

        actual_parts: list[tuple[str, str, str]] = []
        # get the new name already parsed
        for common in change_handler[1]:
            common_path = Path(change_handler[1][common][2])
            if common_path in new_steps:
                actual_parts.append(
                    (
                        common[:-1].replace(" ", "_"),  # [file] old
                        open(common_path / "common.rpy", "r")
                        .readlines()[change_handler[1][common][3]]
                        .split(" ", 1)[1]
                        .split("=")[0][:-1],  # [file] new
                        get_name_acron(origin=common_path),  # alias
                    )
                )
        files_to_rewrite: dict[str, list[str]] = {}
        for sector in actual_parts:
            file: dict[Literal["field", "file", "where"], str]
            for file in change_handler[0].query(sector[0], ["where"], False):

                if not file["file"] in files_to_rewrite:
                    files_to_rewrite[file["file"]] = open(
                        game_data / (file["file"] + ".rpy")
                    ).readlines()

                lines = change_handler[2][file["file"]][file["field"]][file["where"]]

                for n_line in lines:
                    files_to_rewrite[file["file"]][n_line] = files_to_rewrite[
                        file["file"]
                    ][n_line].replace(
                        *[
                            i.replace("_", " ").replace("side ", "").replace(" ", "_")
                            for i in sector[:2]
                        ]
                    )

        if __can_edit__:
            for n in files_to_rewrite:
                open(game_data / (n + ".rpy"), "w").writelines(files_to_rewrite[n])

        origin.can_generate_common = True

    if origin.can_generate_common:
        import_all()


def given_path(path: str) -> Path:
    """just a silly function to check if the given path exits

    Args:
        path (str): a path

    Raises:
        ValueError: raised if the path doesn't exits

    Returns:
        Path: the path as object
    """
    _ = Path(path).resolve()
    if not _.exists():
        raise ValueError
    return _


def frame(parser: ArgumentParser):
    """Basically the entry point to start the tool using the default arguments

    Args:
        parser (ArgumentParser): the parser object (if you have one created)
    """
    global __return__
    logger.info("Starting phase 3: getting arguments")
    # TODO: add translations
    parser.add_argument(
        "-a",
        "--authors",
        action="version",
        version="Thanks to "
        + mkr_str(__author__ if isinstance(__author__, list) else [__author__], ", ")
        + " for make this "
        + __product__
        + " possible!",
        help="Show the authors that made this version",
    )

    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + __version__
    )

    parser.add_argument(
        "--set-game",
        "-s-game",  # yes... I want ass
        action="store",
        help="Set the main folder to look for assets within the proyect",
        default=Path("."),
        metavar="path",
        type=given_path,
        required=True,
    )

    parser.add_argument(
        "--set-audio",
        "-s-audio",
        action="store",
        help="Set the audio's folder path",
        default=_default_audio,
        metavar="path",
        type=given_path,
    )

    parser.add_argument(
        "--set-video",
        "-s-video",
        action="store",
        help="Set the video's folder path",
        default=_default_video,
        metavar="path",
        type=given_path,
    )

    parser.add_argument(
        "--set-sprite",
        "-s-sprite",
        action="store",
        help="Set the sprite's folder path",
        default=_default_sprite,
        metavar="path",
        type=given_path,
    )

    parser.add_argument(
        "--set-background",
        "-s-background",
        action="store",
        help="Set the background's folder path",
        default=_default_background,
        metavar="path",
        type=given_path,
    )

    parser.add_argument(
        "--set-language",
        "-s-lang",
        action="store",
        help="Set the actual language for the session",
        default=os_language,
        choices=list(languages.keys()),
        type=str,
    )

    ###########################
    #
    # Features group
    #
    ###########################

    features_group = parser.add_argument_group(
        "Features",
        "These commands will control how your session behave and respond to differents scenes",
    )

    if has_feature(FeaturesKeywords.IMAGE_CREATION):
        features_group.add_argument(
            "--enable-side",
            "-n-sides",
            action="store_true",
            help="enable side variants generation",
            default=False,
        )

    features_group.add_argument(
        "--enable-common",
        "-n-common",
        action="store_true",
        help="enable common file generation",
        default=False,
    )

    if has_feature(FeaturesKeywords.RENAMING_PROCESS):
        features_group.add_argument(
            "--enable-renamer",
            "-n-renamer",
            action="store_true",
            help="if enable, this will open a procces to rename files before create common.rpy files (useful in big proyects)",
            default=False,
        )

    if has_feature(FeaturesKeywords.ZIP_COMPRESSION):
        features_group.add_argument(
            "--enable-zip-compression",
            "-n-compression",
            action="store_true",
            help="enable compression into a zip... you might use to make updates to the assets",
            default=False,
            deprecated=True,  # just for now
        )

    features_group.add_argument(
        "--set-cipher-number",
        "-s-cipher",
        action="store",
        help="if used, this will enable the assets encryption system, ensure you have our modded renpy SDK",
        default=0,
        type=int,
        deprecated=True,
    )

    features_group.add_argument(
        "--set-import-mode",
        "-s-mode",
        action="store",
        help="set the import mode",
        default="dev",
        type=str,
        choices=["zip", "source", "dev"],
    )

    ###########################
    #
    # Skip group
    #
    ###########################

    skip_group = parser.add_argument_group(
        "Skipper field",
        "These commands will add skips and exceptions when getting different resources",
    )

    skip_group.add_argument(
        "--skip-name",
        "-s-name",
        nargs="+",
        help="Skip the names given (even if it is either file or folder)",
        default=[],
        metavar="names",
    )

    skip_group.add_argument(
        "--skip-file",
        "-s-file",
        nargs="+",
        help="Skip the names given when files are scanned",
        default=[],
        metavar="names",
    )

    skip_group.add_argument(
        "--skip-folder",
        "-s-folder",
        nargs="+",
        help="Skip the names given when folders are scanned",
        default=[],
        metavar="names",
    )

    skip_group.add_argument(
        "--skip-extension",
        "-s-extension",
        nargs="+",
        help="Skip the extesions given",
        default=[],
        metavar="extension",
    )

    args = parser.parse_args()
    logger.info("Argument object: " + str(args))
    logger.info("End phase 3: getting arguments")

    logger.info("========PROGRAM STARED========")
    SKIP_FILE_NAME.extend(args.skip_file)
    SKIP_FOL_NAMES.extend(args.skip_folder)
    SKIP_GEN_NAMES.extend(args.skip_name)
    SKIP_EXTENSION.extend(args.skip_extension)

    global DEFAULT_KIND_IMPORT
    DEFAULT_KIND_IMPORT = args.set_import_mode
    try:
        handler(
            ArgumentsGiven(
                args.set_game,
                args.set_audio,
                args.set_video,
                args.set_sprite,
                args.set_background,
                args.enable_side,
                args.enable_common,
                args.enable_renamer,
                args.set_cipher_number,
                args.enable_zip_compression,
            )
        )
    except Exception as e:
        logger.critical(e)
        __return__ = 3
    logger.info("========PROGRAM ENDED========")


if __name__ == "__main__":
    frame(parser)
    parser.exit(__return__, __return_text__[__return__])
