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

########################################################
#
# Meta zone
#
########################################################
__version__ = "1.0.5.0"
__return__ = 0
__return_text__ = [
    "completed",
    "missing library, check the logs",
    "you have an unsupported python version",
    "Unkwon error, check the logs"
]
__product__ = "importer"
__author__ = "Z3R0_GT"
__is_main__ = __name__ == "__main__"
__can_edit__ = True
########################################################
#
# Logger zone
#
########################################################
FORMAT = (
    "%(asctime)s <%(name)s> in %(funcName)s launched %(levelname)s with: %(message)s"
)
logger = logging.getLogger(__name__ if not __is_main__ else "import.py")
logging.basicConfig(
    filename="importer.log", level=logging.INFO, format=FORMAT, filemode="w"
)

if __name__ == "__main__":
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

from enum import IntEnum, StrEnum
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
    ]
)
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
from subprocess import run
from json import load, loads, dumps
from configparser import ConfigParser

########################################################
#
# Enums zone
#
########################################################


class ImageConfigHead(StrEnum):
    SIDE = "side"
    SCALE = "scale"
    TEMPLATE = "template"


class ImageConfigValue(StrEnum):
    SIZE = "size"
    SQUARE = "square"
    DIMENSION = "dimension"
    KEYS = "keys"
    REPEAT = "repeat"


class FeaturesKeywords(StrEnum):
    ZIP_COMPRESSION = "z"
    PRETTY_CONSOLE = "t"
    IMAGE_CREATION = "i"
    RENAMING_PROCESS = "s"
    SIDE_GENERATION = "ms"
    PRETTY_PRINT = "m"


class RequiredFiles(StrEnum):
    TEMPLATES = "templates.json"
    ANIMATED = "keys.json"
    INFO = "info.cgf"


class ColorPerLevel(StrEnum):
    GENERIC = "#A33838"
    CRITIC = "#BEBC1B"
    INTERNAL = "#922296"


class ProccesKeywords(StrEnum):
    ALL = "a"
    SCALE = "s"
    FLIP = "i"
    SIDE = "k"
    ANIMATED = "m"
    NOTHING = "n"
    IGNORE = "g"
    SUBFOLDER = "r"


class ParseKeywords(StrEnum):
    FILE = "f"
    FOLDER = "o"


class ImportKeywords(StrEnum):
    IMAGES = "i"
    VIDEOS = "v"
    SOUNDS = "s"


class MessagesError(StrEnum):
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
    DESCRIPTION = ("DESCRIPTION",)
    MESSAGE_INFO = "MESSAGE_INFO"
    MESSAGE_FUNCTION_INIT = "MESSAGE_FUNCTION_INIT"
    MESSAGE_FUNCTION_PROGRESS = "MESSAGE_FUNCTION_PROGRESS"
    MESSAGE_FUNCTION_ENDED = "MESSAGE_FUNCTION_ENDED"


class TemplateKeys(StrEnum):
    NORMAL = "normal"
    SCALE = "scale"
    FLIPED = "fliped"
    SIDE = "side"
    SOUND = "sound"
    VIDEO = "video"
    ZIPLOAD = "zip_load"
    ANIMATED_BLINK_NORMAL = "animated_blink_normal"
    ANIMATED_ANIMATED_BODY = "animated_body"


class TemplatePath(StrEnum):
    NORMAL = "normal"
    ENCRYPT = "encrypt"
    ZIP = "zip"


class TemplatePathKeys(StrEnum):
    BASE = "base"
    NAME = "name"


########################################################
#
# Features zone
#
########################################################
features_available: list[str] = []
features_enabled: list[str] = []


def add_feature(what: FeaturesKeywords, is_internal: bool = True) -> bool:
    global features_available, features_enabled
    ref = features_available if is_internal else features_enabled
    if not what in FeaturesKeywords:
        return False
    ref.append(what)
    return True


def has_feature(what: FeaturesKeywords, is_internal: bool = True) -> bool:
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
logger.info("Built-in languages: " + str(list(languages.keys())))
os_language = getdefaultlocale()[0].split("_")[0]  # type: ignore
logger.info("OS language detected: " + os_language)
language: str = os_language if os_language in languages.keys() else "en"
logger.info("Selected language: " + language)
logger.info("Language service ended")


def get_message_translated(name: str, /, **kwargs: dict[str, str]) -> str:
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
    epilog="You can search for more help here! --> https://github.com/Z3R0GT/renpy-auto-importer"
)

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
        Any,
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
) -> None: ...


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
DEFAULT_SIZE_SIDE_VAR: str = (
    "300x350"  # usado para la dimensión de las imagenes de marco (side)
)
DEFAULT_SIZE_CORP_VAR: tuple[int, int, int, int] = (675, 5, 1067, 480)

DEFAULT_RESOURCE_PATH = "assets"

DEFAULT_PATH_VIDEO = "%(base)s/video"  # base
DEFAULT_PATH_SOUND = "%(base)s/audio"  # base
DEFAULT_PATH_IMAGE = "%(base)s/images"  # base

DEFAULT_PATH_SIDE = f"%({TemplatePathKeys.BASE})s/side"  # mostly for images


########################################################
#
# Extensions zone
#
########################################################
IGNORE_NOT_SUPPORTED: bool = False
DEFAULT_EXTEND_IMAGE_NOT_SUPPORT: list[str] = ["png", "jpg"]
DEFAULT_EXTEND_VIDEO_NOT_SUPPORT: list[str] = ["mp4"]
DEFAULT_EXTEND_SOUND_NOT_SUPPORT: list[str] = ["mp3"]


DEFAULT_EXTEND_IMAGE_SUPPORT: list[str] = ["webp", "png"]
DEFAULT_EXTEND_VIDEO_SUPPORT: list[str] = ["webm"]
DEFAULT_EXTEND_SOUND_SUPPORT: list[str] = ["ogg"]

SKIP_SYMBOLS: list[str] = ["_"]
SKIP_GEN_NAMES: list[str] = []
SKIP_FILE_NAME: list[str] = ["gui", "options", "screens"]
SKIP_FOL_NAMES: list[str] = ["gui", "credits", "logos", "fonts"]
SKIP_EXTENSION: list[str] = []

RESERVED_GENERIC_FILE_NAMES: tuple[str, str, str, str, str, str] = (
    "character",
    "characters",
    "noncommon",
    "common",
    "common_test",
    "common_dist",
)
RESERVED_GENERIC_FILE_EXTEN: list[str] = ["rpyc"]
RESERVED_GENERIC_FOLD_NAMES: tuple[str, str, str, str] = (
    "generic_template",
    "side",
    "logs",
    "interactive",
)
RESERVED_GENERIC_CREA_NAMES: tuple[str, str, str] = (
    "common",
    "common_test",
    "common_dist",
)
RESERVED_GENERIC_CREA_EXTEN: tuple[str] = "rpy"

########################################################
#
# Etc zone
#
########################################################
ZIP_PASSWORD: str = ""
DEFAULT_TAB: int = 4
DEFAULT_NAME_LIMIT: int = 3
INPUT_FORM: str = f"\n>{"."*DEFAULT_TAB}"
DEFAULT_KIND_IMPORT: Literal["source", "dev", "zip"] = "dev"
FILE_NAME_REPLACE: dict[int, str] = str.maketrans(
    {"(": "", "!": " ", ")": "", "-": "_"}
)
FILE_NAME_REPLACE_LONG: dict[str, str] = {
    "scene": "scn",
}

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

BUILDIN_FILE_TEMPLATES: dict[TemplatePath, str] = {
    TemplatePath.ENCRYPT: "%(path)s/%(file)s.enc",
    TemplatePath.NORMAL: "%(path)s/%(file)s",
    TemplatePath.ZIP: "%(path)s/%(file)s.zip",
}

BUILDIN_ANIMATION_KEYS: dict[TemplateKeys, list[str]] = {
    TemplateKeys.ANIMATED_ANIMATED_BODY: ["walking"],
    TemplateKeys.ANIMATED_BLINK_NORMAL: ["blink", "e"],
}

########################################################
#
# Path handlers zone
#
########################################################
ROOT_EXE_GAME: Path = Path(getcwd())
ROOT_RES_SOFT: Path = Path(user_data_dir(__product__, __author__))

_literal_fields_files = Literal["dir", "file", "both"]

_literal_fields_exten = Literal["image", "sound", "video"]


def get_list_system_dirs(
    origin: Path = Path("."), kind: _literal_fields_files = "file", **kwargs
) -> list[str | list[str]]:

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
if RequiredFiles.TEMPLATES in get_list_system_dirs(ROOT_EXE_GAME, "file"):
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
    """Buscador ligero basado en whoosh"""

    def __init__(self, sc: Schema):
        #sc = sc#Schema(path=TEXT(stored=True), content=TEXT(stored=True))
        self.schema = sc
        sc.add("raw", TEXT(stored=True))
        self.ix = RamStorage().create_index(self.schema)

    def index_documents(self, docs: Sequence):
        """Ingresa documentos a la RAM

        Args:
            docs (Sequence): documentos
        """
        writer = self.ix.writer()
        for doc in docs:
            d = {k: v for k, v in doc.items() if k in self.schema.stored_names()}
            d["raw"] = dumps(doc)  # raw version of all of doc
            writer.add_document(**d)
        writer.commit(optimize=True)

    def get_index_size(self) -> int:
        """Obtiene el total de documentos indexados actualmente

        Returns:
            repr (int): total de documentos ingresados
        """
        return self.ix.doc_count_all()

    def query(self, q: str, fields: Sequence, highlight: bool = True) -> list[dict]:
        """Busca de entre los documentos ingresados

        Args:
            q (str): nombre a buscar
            fields (Sequence): donde debe buscar (partes)
            highlight (bool, optional): resaltar las zonas de coincidencia. Defaults to True.

        Returns:
            repr (List[Dict]): coincidencias finales
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


def generator(num: int = 99):
    """Basicamente hace un generador de N numeros

    Args:
        num (int): numeros a generar

    Yields:
        int: numero XD
    """
    for i in range(num):
        yield i


def del_jump(base: list[str], allow_blank: bool = False) -> None:
    for c in range(0, len(base)):
        base[c] = base[c].replace("\n", "").replace("\r", "")

    if not allow_blank:
        while base.count("") != 0:
            del base[base.index("")]


def add_jump(base: list) -> list[str]:
    return [f"{i}\n" for i in base]


def mkr_str(base: list, sep: str = "") -> str:
    return sep.join([str(i) for i in base])


def compare_string(str_from: str, str_to: str, limit_try: int = 3) -> bool:
    if str_from == str_to:
        return False

    str_to_copy: list[str] = str_to.split(" " if str_to.count(" ") != 0 else "_")
    str_from_copy: list[str] = str_from.split(" " if str_from.count(" ") != 0 else "_")

    c = 0
    for name in str_from_copy:
        if name in str_to_copy:
            c += 1
            str_to_copy.remove(name)

    return c > limit_try


def has_required_keys(base: list[str], reference: StrEnum) -> bool:
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
    if kind == "both":
        kind = "file"

    name = name.split(".")[0] if len(name.split(".")[0]) != 0 else name.split(".")[1]

    if name[0] in SKIP_SYMBOLS[0] or name in SKIP_GEN_NAMES:
        return True

    if kind == "dir":
        return name in SKIP_FOL_NAMES or name in RESERVED_GENERIC_FOLD_NAMES
    elif kind == "file":
        return name in SKIP_FILE_NAME or name in RESERVED_GENERIC_FILE_NAMES
    else:
        return False


def is_animated_name(name: str) -> TemplateKeys:
    for part in name.split("_"):

        for key, parts in KEYS_IMPORTED.items():
            if part in parts:
                return key

    return None


def get_list_system_file(
    kind: _literal_fields_files, origin: Path = Path("."), is_normal: bool = True
) -> list[str | list[str]]:

    match kind:
        case "both":
            return [
                list(
                    filter(
                        lambda x: (
                            not is_reserved(x, "file")
                            if is_normal
                            else is_reserved(x, "file")
                        ),
                        get_list_system_dirs(origin, "file"),
                    )
                ),
                list(
                    filter(
                        lambda x: (
                            not is_reserved(x, "dir")
                            if is_normal
                            else is_reserved(x, "dir")
                        ),
                        get_list_system_dirs(origin, "dir"),
                    )
                ),
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
    local = (
        get_list_system_file("file", origin, is_normal) if len(local) == 0 else local
    )
    
    @singledispatch
    def extend(extension: str) -> list[str]:
        return [i for i in local if i[-len(extension) :] in [extension] + SKIP_EXTENSION]

    @extend.register
    def _(extension: list) -> list[str]:
        a = []
        extension += SKIP_EXTENSION #HACK
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
    local = (
        get_list_system_file("file", origin, is_normal) if len(local) == 0 else local
    )
    end: list[str] = []

    # NOTE: quizas aqui podamos "mejorar" el procedimiento
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

    local = get_list_file_named(names, is_normal, origin=origin, local=local)
    local = get_list_file_extended(extesions, is_normal, origin=origin, local=local)

    return local


def get_list_subfolders(
    origin: Path = Path("."), exclude: Sequence[str] = []
) -> list[str | Path]:
    folders = [
        origin / x for x in get_list_system_file("dir", origin) if not x in exclude
    ]
    for x in folders:

        if x.resolve() == origin.resolve():
            continue

        if not x.exists():
            continue

        folders += get_list_subfolders(x, exclude)

    return folders.copy()


def get_path_parsed(start: str | list[str], origin: Path = Path(".")) -> str:
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
    
    return mkr_str(
        normal if not dir_exits else normal[normal.index(start[0]) :], "/"
    )


def get_name_parsed(file: str) -> str:
    # NOTE: most of dev use VS Code, so replacing the spaces for _, will make the extesion include
    # the file within the context window, cuz using spaces based, it will make some trouble
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


#############################ssw###########################
#
# Functionally related zone
#
########################################################
def get_name_acron(limit: int = 3, origin: Path = Path(".")) -> str:
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
    pass


def write_side_image(
    size: tuple[int, int, int, int],
    load: dict[TemplatePathKeys, str | list[str]],
    file_generation_limit: int = 99,
) -> bool:
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
        file_path_side = origin / file  # include '/side'
        file_path_orin = _ / file  # just its base without '/side'

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

    size_scale: tuple[str, str]
    try:
        size_scale = tuple([int(x) for x in _size_scale.split("x")])
    except TypeError:
        # TODO: add error message
        size_scale = tuple([int(x) for x in DEFAULT_SIZE_SCREEN.split("x")])

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
            size_scale,
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


def write_names(sprites: Path = Path("."), game_data: Path = Path(".")):

    #get each character's aliases
    folders = get_list_system_dirs(sprites, "dir")
    alias = []
    for folder in folders:
        alias.append( get_name_acron(origin=(sprites / folder)) )

    lines_used = scan_lines_chapters(alias, game_data)
    lines_origin = scan_lines_common(game_data)

    #used to query where the files come from
    engine_origin = SearchEngine(
        Schema(
            path_simple=TEXT(stored=True), 
            path_str=TEXT(stored=True),
            name=TEXT(stored=True), 
            whole=TEXT(stored=True), 
            path_whole=TEXT(stored=True)
        )
    )
    #used to query where the files are being used
    engine_useded = SearchEngine(
        Schema(
            field=TEXT(stored=True), 
            file =TEXT(stored=True), 
            where=TEXT(stored=True),
        )
    )
    
    origin_base = []
    #parse the origin info into something woosh can use
    for folder, common in lines_origin.items():
        # path, name, whole, path (whole)
        for line in common:
            s_line = line.replace("\n", "")
            if len(s_line.replace(" ", "")) == 0 or line[0] == "#":
                continue
            #TODO: make checks to ensure this shit have the correct format
            try: 
                path = line.split("=", 1)[1].split("\"", 1)[1].split("\"", 1)[0]
            except IndexError:
                continue
            
            origin_base.append(
                {
                    "path_simple": path,
                    "path_str": " ".join(path.split("/")),
                    "name": line.split("=", 1)[0].split(" ", 1)[1].replace("_", " "),
                    "whole": line,
                    "path_whole": folder.as_posix()
                }
            )
    useded_base = []
    for file, field in lines_used.items():
        
        for zone, use in field.items():
            
            for s_use in list(use.keys()):
                useded_base.append(
                    {
                        "field": zone,
                        "file" : file,
                        "where": s_use
                    }
                )
    engine_origin.index_documents(origin_base)
    engine_useded.index_documents(useded_base)
    
    to_change: dict[str, tuple[str, str, str, int]] = {}
    print(Fore.RED + "AFTER YOU END THIS PROCCES, THE CHANGES WILL BE APPLIED"+Fore.RESET)
    while True:
        
        result = engine_origin.query(
            input("Insert a name or its path\n>..."),
            ["name", "path_simple", "path_str"],
            False
        )
        
        if len(result) != 0:
            print("Use -1 to cancel this query")
            print("ID <--------> INFO")
            for _id, info in zip(range(len(result)), result):
                print("Given the ID" + Fore.GREEN + f" {_id}" + Fore.RESET + ":" +f"\
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
            
            print("Actual file name: "+ Fore.BLUE + f"{info["path_simple"].split("/")[-1]}" + Fore.RESET + "\n")
            new_name = input("Insert the new " + Fore.RED + "file name" + Fore.RESET + ", just the name, not the extension\n>...")
            to_change[info["name"]] = ( # [file] 
                new_name,            # file
                info["path_simple"], # game/images/Sprites/ailstair/[file].png
                info["path_whole"],  #Path to common (not include common.rpy itself)
                lines_origin[Path(info["path_whole"])].index(info["whole"])  #line where it's located
            )
        else:
            print("nothing found!")
            
        if not input("Continue making querys?\n") in ["y", "yes"]:
            break
    
    if __can_edit__ and input(
            "Are you 100% you want to rename " + str(len(to_change)) + " files?\
            \n" + Fore.RED + "TIHS CAN'T BE UNDONE, ARE YOU SURE?" + Fore.RESET + "\n>..."
        ) in ["yes", "y"]:
        
        for values in to_change.values():
            new = values[1].split("/")
            new[-1] = values[0] + "." + new[-1].split(".")[-1]
            new = "/".join(new)
            print(f"The file {Fore.RED + values[1].split("/")[-1] + Fore.RESET} will be renamed to {Fore.RED + new.split("/")[-1] + Fore.RESET} in {values[1]}")
            try:
                rename(
                    Path(values[1]).resolve(),
                    Path(new)
                )  
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


IMAGE_KEYWORDS: list[str] = ["scene", "show", "hide"]
SOUND_KEYWORDS: list[str] = ["play"]


def scan_lines_chapters(
    aliases: list[str], origin: Path = Path(".")
) -> dict[str, dict[str, dict[str, list[int]]]]:

    files = get_list_file_extended(RESERVED_GENERIC_CREA_EXTEN, origin=origin)
    all_files_usage = {}

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
        #s_folder = folder.as_posix().split("/")[-1]

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
def _aux_import_(is_audio: bool, origin: Path = Path("."), single: bool = False):
    folders: list[str] = [ origin ]
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


def import_audio(origin: Path = Path("."), single: bool = False):
    _aux_import_(True, origin, single)


def import_video(origin: Path = Path("."), single: bool = False):
    _aux_import_(False, origin, single)


# generic function
def import_backgrounds(origin: Path = Path(".")):
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

_default_audio = Path("./game/" + DEFAULT_PATH_SOUND % {"base": DEFAULT_RESOURCE_PATH})
_default_video = Path("./game/" + DEFAULT_PATH_VIDEO % {"base": DEFAULT_RESOURCE_PATH})
_default_sprite= Path("./game/" + DEFAULT_PATH_IMAGE % {"base": DEFAULT_RESOURCE_PATH} + "/characters")
_default_background = Path("./game/" + DEFAULT_PATH_IMAGE % {"base": DEFAULT_RESOURCE_PATH} + "/world")
def handler(origin: ArgumentsGiven):
    game_data: Path = origin.game
    _0 = {"base" : game_data / DEFAULT_RESOURCE_PATH }
    
    assets_info = ArgumentsGiven(
        _0["base"],
        Path(DEFAULT_PATH_SOUND % _0 if _default_audio == origin.audio else origin.audio),
        Path(DEFAULT_PATH_VIDEO % _0 if _default_video == origin.video else origin.video),
        Path((DEFAULT_PATH_IMAGE % _0) + "/characters" if _default_sprite == origin.sprite else origin.sprite) ,
        Path((DEFAULT_PATH_IMAGE % _0) + "/world"      if _default_background == origin.background else origin.background),
        None,
        None,
        None,
        None,
        None
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
    
    #1st import 
    if origin.can_generate_common:
        import_all()
    
    #renamer was used
    if len(change_handler) != 0:
        #here we compared all original date with the modded one
        new_steps = scan_lines_common(game_data)
        
        actual_parts: list[tuple[str, str, str]] = []
        #get the new name already parsed
        for common in change_handler[1]:
            common_path = Path(change_handler[1][common][2])
            if common_path in new_steps:
                actual_parts.append(
                    (
                        common[:-1].replace(" ", "_"),     # [file] old
                        open(common_path / "common.rpy", "r").readlines()[change_handler[1][common][3]].split(" ",1)[1].split("=")[0][:-1], # [file] new
                        get_name_acron(origin=common_path) #alias
                    ) 
                )
        files_to_rewrite: dict[str, list[str]] = {}
        for sector in actual_parts:
            file: dict[Literal["field", "file", "where"], str]
            for file in change_handler[0].query(sector[0], ["where"], False):
                
                if not file["file"] in files_to_rewrite:
                    files_to_rewrite[file["file"]] = open(game_data / (file["file"] + ".rpy")).readlines()
                
                lines = change_handler[2][file["file"]][file["field"]][file["where"]]
                
                for n_line in lines:
                    files_to_rewrite[file["file"]][n_line] = files_to_rewrite[file["file"]][n_line].replace(*[i.replace("_", " ").replace("side ", "").replace(" ", "_") for i in sector[:2]])

        if __can_edit__:
            for n in files_to_rewrite:
                open(game_data / (n + ".rpy"), "w" ).writelines(files_to_rewrite[n])
        
        #2nd import (in case renamer was used, to ensure everything is fine)
        import_all()
    

def given_path(path: str) -> Path:
    _ = Path(path).resolve()
    if not _.exists():
        raise ValueError
    return _

def frame():
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
        "-v",
        "--version",
        action="version",
        version="%(prog)s " + __version__
    )

    parser.add_argument(
        "--set-game",
        "-s-ass", #yes... I want ass
        action="store",
        help="Set the main folder to look for assets within the proyect",
        default=Path("."),
        metavar="path",
        type=given_path,
        required=True
    )

    parser.add_argument(
        "--set-audio",
        "-s-audio",
        action="store",
        help="Set the audio's folder path",
        default= _default_audio,
        metavar="path",
        type=given_path
    )

    parser.add_argument(
        "--set-video",
        "-s-video",
        action="store",
        help="Set the video's folder path",
        default= _default_video,
        metavar="path",
        type=given_path
    )

    parser.add_argument(
        "--set-sprite",
        "-s-sprite",
        action="store",
        help="Set the sprite's folder path",
        default= _default_sprite,
        metavar="path",
        type=given_path
    )
    
    parser.add_argument(
        "--set-background",
        "-s-background",
        action="store",
        help="Set the background's folder path",
        default= _default_background,
        metavar="path",
        type=given_path
    )

    parser.add_argument(
        "--set-language",
        "-s-lang",
        action="store",
        help="Set the actual language for the session",
        default=os_language,
        choices=list(languages.keys()),
        type=str
    )

    ###########################
    #
    # Features group
    #
    ###########################

    features_group = parser.add_argument_group(
        "Features", 
        "These commands will control how your session behave and respond to differents scenes"
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
            deprecated=True #just for now
        )

    features_group.add_argument(
        "--set-cipher-number",
        "-s-cipher",
        action="store",
        help="if used, this will enable the assets encryption system, ensure you have our modded renpy SDK",
        default=0,
        type=int,
        deprecated=True
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
        "These commands will add skips and exceptions when getting different resources"
    )
    
    skip_group.add_argument(
        "--skip-name",
        "-s-name",
        nargs="+",
        help="Skip the names given (even if it is either file or folder)",
        default=[],
        metavar="names"
    )

    skip_group.add_argument(
        "--skip-file",
        "-s-file",
        nargs="+",
        help="Skip the names given when files are scanned",
        default=[],
        metavar="names"
    )

    skip_group.add_argument(
        "--skip-folder",
        "-s-folder",
        nargs="+",
        help="Skip the names given when folders are scanned",
        default=[],
        metavar="names"
    )

    skip_group.add_argument(
        "--skip-extension",
        "-s-extension",
        nargs="+",
        help="Skip the extesions given",
        default=[],
        metavar="extension"
    )

    args = parser.parse_args()
    logger.info("Argument object: "+str(args))
    logger.info("End phase 3: getting arguments")

    logger.info("========PROGRAM STARED========")
    SKIP_FILE_NAME.extend(
        args.skip_file
    )
    SKIP_FOL_NAMES.extend(
        args.skip_folder
    )
    SKIP_GEN_NAMES.extend(
        args.skip_name
    )
    SKIP_EXTENSION.extend(
        args.skip_extension
    )
    
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
                args.enable_zip_compression
            )
        )
    except Exception as e:
        logger.critical(e)
        __return__ = 3
    logger.info("========PROGRAM ENDED========")

if __name__ == "__main__":
    frame()
    parser.exit(__return__, __return_text__[__return__])
