# error code
# 1 -> falta libreria importante
# 2 -> incorrect version
########################################################
#
# Imports general zone
#
########################################################
import sys
import logging
import warnings
from os import listdir, getcwd, remove

########################################################
#
# Meta zone
#
########################################################
__version__  = "1.0.4.6-dev"
__return__   = 0
__product__  = "importer"
__author__   = "Z3R0_GT"
__is_main__  = __name__ == "__main__"
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

#yeah.... 3.15 is not supported cuz locale.getdefaultlocale was marked as 'future removal' for that version and
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

#NOTE: this import is here cuz the section 'Imports specifc zone' is after some code that needs this function working
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
from json import load, loads, dump, dumps
from configparser import ConfigParser

########################################################
#
# Enums zone
#
########################################################

class ImageConfigHead(StrEnum):
    SIDE = "side"
    ANIMATION = "animation"


class ImageConfigValue(StrEnum):
    SIZE = "size"
    DIMENSION = "dimension"
    KEYS = "keys"

class FeaturesKeywords(StrEnum):
    ZIP_COMPRESSION = "z"
    PRETTY_CONSOLE = "t"
    IMAGE_CREATION = "i"
    RENAMING_PROCESS = "s"


class RequiredFiles(StrEnum):
    TEMPLATES = "templates.json"


class ColorPerLevel(StrEnum):
    GENERIC = "#A33838"
    CRITIC = "#BEBC1B"
    INTERNAL = "#922296"


class ProccesKeywords(StrEnum):
    ALL = "a"
    SCALE = "s"
    FLIP = "i"
    ANIMATED = "m"
    NOTHING = "n"

class ParsedFolderMode(StrEnum):
    PARTS_BASED = "p"
    IMAGE_BASED = "i"

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
    DESCRIPTION = "DESCRIPTION",
    MESSAGE_INFO = "MESSAGE_INFO"
    MESSAGE_FUNCTION_INIT = "MESSAGE_FUNCTION_INIT"
    MESSAGE_FUNCTION_PROGRESS = "MESSAGE_FUNCTION_PROGRESS"
    MESSAGE_FUNCTION_ENDED = "MESSAGE_FUNCTION_ENDED"


class TemplateKeys(StrEnum):
    NORMAL = "normal"
    SCALE  = "scale"
    FLIPED = "fliped"
    SIDE   = "side"
    SOUND  = "sound"
    VIDEO  = "video"
    ZIPLOAD= "zip_load"

class TemplatePath(StrEnum):
    NORMAL  = "normal"
    ENCRYPT = "encrypt"
    ZIP     = "zip"


class TemplatePathKeys(StrEnum):
    BASE = "base"
    NAME = "name"

########################################################
#
# Features zone
#
########################################################
features_available: list[str] = []
features_enabled  : list[str] = []

def add_feature(what: FeaturesKeywords, is_internal: bool = True) -> bool:
    global features_available, features_enabled
    ref = features_available if is_internal else features_enabled
    if not what in FeaturesKeywords:
        return False
    ref.append(what)
    return True


def has_feature(what: FeaturesKeywords, is_internal: bool = True) -> bool:
    return what in FeaturesKeywords and what in (features_available if is_internal else features_enabled)


########################################################
#
# Messages/Language built-in zone
#
########################################################
logger.info("Starting language service")
languages: dict[str, dict[str, str]] = {
    "en": {
        MessagesError.MODULE_NOT_FOUND_USING_DEFAULT: "There's not '{name}' installed, using default",
        MessagesError.MODULE_NOT_FOUND     : "There's not '{name}' installed",
        MessagesError.FEAUTRE_NOT_FOUND    : "The {name} feature couldn't be found or used",
        MessagesError.ARGUMENT_NOT_FOUND   : "The {name} argument couldn't be found",
        MessagesError.FILE_NOT_FOUND       : "The {file} file couldn't be found",
        MessagesError.PATH_NOT_FOUND       : "The {path} path couldn't be found",
        MessagesError.USING_BUILT_IN       : "Using {name} built-in instead",
        MessagesMeta.DESCRIPTION           : "This is a simple tool easy-to-use to import assets and stuff from normal files to common.rpy files",
        MessagesError.FEATURE_NOT_SUPPORTED: "The feature '{name}' is not supported due to {reason}",
        MessagesMeta.MESSAGE_INFO          : "Given '{name}' was made the operation '{operation}' with result '{result}'",
        MessagesMeta.MESSAGE_FUNCTION_INIT : "The operation '{name}' was started",
        MessagesMeta.MESSAGE_FUNCTION_PROGRESS: "Resolving '{name}' operation",
        MessagesMeta.MESSAGE_FUNCTION_ENDED: "The operation '{name}' was ended with '{result}' as result",
        MessagesError.EXTENSION_ERROR      : "There are some files that might need change its extension or be compressed:",
        MessagesError.INCORRECT_ARGUMENTS  : "Due a incorrect configuration for '{arguments}', '{default}' will be used, based on '{message}'"
    }
}
logger.info("Built-in languages: " + str(list(languages.keys())))
os_language = getdefaultlocale()[0].split("_")[0] # type: ignore
logger.info("OS language detected: " + os_language)
language: str = os_language if os_language in languages.keys() else "en"
logger.info("Selected language: " + language)
logger.info("Language service ended")


def get_message_translated(name: str, /,**kwargs: dict[str, str]) -> str:
    if not name in languages[language]:
        logger.debug(
            "The key '{}' couldn't be found base in the language {}".format(
                name, language
            )
        )
        return ""
    try:
        return languages[language][name].format(**kwargs) if len(kwargs) != 0 else languages[language][name]
    except KeyError:
        print(get_message_translated(MessagesMeta.MESSAGE_INFO, name=name, operation="get_message_translated", result="key not found"))
        return "Unkown error"

########################################################
#
# Imports specifc zone
#
#
# NOTE: all modules (except for those that are require adove) MUST be declared here, 
# in case is required and this doesn't is delivered with python, use __return__ variable
# to make the program die after the error is launched (typing_extensions module section is an example of how-to)
#
# NOTE 2.0: if some class/module is required/used by the program, but there's could an alternative or workaround, don't use  
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
    from typing import (
        overload
    )
    
    logger.fatal(get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="typing_extensions"))
    __return__ = 1
#let's add some arguments to this
@overload
def compress_multiple(src_file: list[Path | str], src_path: list[Path, str], output_path: str | Path, password: str, level: int, do_during: Callable[[int], None]) -> None:...

try:
    from pyminizip import compress_multiple

    if not add_feature(FeaturesKeywords.ZIP_COMPRESSION):
        logger.info(get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name=FeaturesKeywords.ZIP_COMPRESSION))
except ModuleNotFoundError:
    def compress_multiple(src_file: list[Path | str], src_path: list[Path, str], output_path: str | Path, password: str, level: int, do_during: Callable[[int], None]) -> None:
        logger.warning(get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="pyminizip"))
    warnings.warn(get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="pyminizip"))

try:
    from tqdm import tqdm

    if not add_feature(FeaturesKeywords.PRETTY_CONSOLE):
        logger.info(get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name=FeaturesKeywords.PRETTY_CONSOLE))
except ModuleNotFoundError:
    class tqdm[T]:
        
        def __init__(self, a: Sequence[T], **kwargs):
            self.iterable = a
        
        def __iter__(self) -> T:
            for n in self.iterable:
                yield n
    
    logger.warning(get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="tqdm"))
    warnings.warn(get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="tqdm"))
try:
    from PIL import Image, UnidentifiedImageError

    if not add_feature(FeaturesKeywords.IMAGE_CREATION):
        logger.info(get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name=FeaturesKeywords.IMAGE_CREATION))
except ModuleNotFoundError:
    #copy paste lol
    class UnidentifiedImageError(OSError):
        """
        Raised in :py:meth:`PIL.Image.open` if an image cannot be opened and identified.

        If a PNG image raises this error, setting :data:`.ImageFile.LOAD_TRUNCATED_IMAGES`
        to true may allow the image to be opened after all. The setting will ignore missing
        data and checksum failures.
        """

        pass
    
    logger.warning(get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="pillow"))
    warnings.warn(get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="pillow"))

try:
    from whoosh.filedb.filestore import RamStorage
    from whoosh.qparser import MultifieldParser
    from whoosh.fields import TEXT, Schema

    if not add_feature(FeaturesKeywords.RENAMING_PROCESS):
        logger.info(get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name=FeaturesKeywords.RENAMING_PROCESS))
except ModuleNotFoundError:
    logger.warning(get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="whoosh"))
    warnings.warn(get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="whoosh"))

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

    logger.warning(get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="platformdirs"))
    warnings.warn(get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="platformdirs"))

sys.exit(__return__) if __return__ != 0 else None
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

DEFAULT_PATH_VIDEO = "%(base)s/video" # base
DEFAULT_PATH_SOUND = "%(base)s/sound" # base
DEFAULT_PATH_IMAGE = "%(base)s/image" # base

DEFAULT_PATH_SIDE = f"%({TemplatePathKeys.BASE})s/%({TemplatePathKeys.NAME})s/side" #mostly for images


########################################################
#
# Extensions zone
#
########################################################
IGNORE_NOT_SUPPORTED: bool = False
DEFAULT_EXTEND_IMAGE_NOT_SUPPORT: list[str] = ["png", "jpg"]
DEFAULT_EXTEND_VIDEO_NOT_SUPPORT: list[str] = ["mp4"]
DEFAULT_EXTEND_SOUND_NOT_SUPPORT: list[str] = ["mp3"]


DEFAULT_EXTEND_IMAGE_SUPPORT: list[str] = ["webp"]
DEFAULT_EXTEND_VIDEO_SUPPORT: list[str] = ["webm"]
DEFAULT_EXTEND_SOUND_SUPPORT: list[str] = ["ogg"]

SKIP_SYMBOLS  : list[str] = ["_"]
SKIP_GEN_NAMES: list[str] = []
SKIP_FILE_NAME: list[str] = []
SKIP_FOL_NAMES: list[str] = ["gui", "credits", "logos", "fonts"]


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
RESERVED_GENERIC_CREA_NAMES: tuple[str, str, str] = ("common", "common_test", "common_dist")
RESERVED_GENERIC_CREA_EXTEN: tuple[str] = ("rpy")

########################################################
#
# Etc zone
#
########################################################
ZIP_PASSWORD: str = ""
DEFAULT_TAB: int = 4
INPUT_FORM: str = f"\n>{"."*DEFAULT_TAB}"
DEFAULT_KIND_IMPORT: Literal["source", "dev", "zip"] = "dev"
FILE_NAME_REPLACE: dict[int, str] = str.maketrans(
    {
        "("    : "",
        "!"    : " ",
        ")"    : "",
        "-"    :"_"
    }
)
FILE_NAME_REPLACE_LONG: dict[str, str] = {
    "scene": "scn",
}

BUILDIN_TEMPLATES: dict[TemplateKeys | str, str | list[str]] = {
    TemplateKeys.NORMAL: "image %(name)s = %(path)s\n",
    TemplateKeys.SCALE: "image %(name)s = im.Scale(%(path)s, %(size)s)\n",
    TemplateKeys.FLIPED: "image %(name)s flip = im.Flip(%(path)s, horizontal=True)\n",
    TemplateKeys.SIDE: "image side {abbr} %(name)s = im.Scale(%(path)s, %(size)s)\n",
    TemplateKeys.SOUND: "define audio.%(name)s = %(path)s\n",
    TemplateKeys.VIDEO: "image %(name)s = Movie(play=%(path)s, bypass=True)\n",
    TemplateKeys.ZIPLOAD: "renpy.loadbytes(' %(file)s', '%(path)s', '%(kind)s')"
}
BUILDIN_FILE_TEMPLATES: dict[TemplatePath, str] = {
    TemplatePath.ENCRYPT: "%(path)s/%(file)s.enc",
    TemplatePath.NORMAL : "%(path)s/%(file)s",
    TemplatePath.ZIP    : "%(path)s/%(file)s.zip"
    
}

BUILDIN_NAME_ANIMATION : dict[str, list[str]] = {
    "walk" : ["walking"],
    "blink": ["blink", "e"]
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

_literal_image_argumt = Literal["acron"]

def get_list_system_dirs(
    origin: Path = Path("."), kind: _literal_fields_files = "file", **kwargs
) -> list[str | list[str]]:
    match kind:
        case "both":
            return [
                get_list_system_dirs(origin, "dir"),
                get_list_system_dirs(origin, "file")
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
logger.info("Ended phase 2")


########################################################
#
# Utils zone
#
########################################################
class SearchEngine:

    """Buscador ligero basado en whoosh"""

    def __init__(self):
        sc = Schema(path=TEXT(stored=True), content=TEXT(stored=True))
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

def has_required_keys(base: list[str], reference: StrEnum, name : str) -> bool:
    for _ in base:
        if not _ in reference:
            print(get_message_translated(MessagesError.ARGUMENT_NOT_FOUND, name=_))
            return False
    return True


parser: ArgumentParser = ArgumentParser(
    "Importer",
    description=get_message_translated(MessagesMeta.DESCRIPTION)
)

########################################################
#
# Path handler zone
#
########################################################
def mkr_dir(what: str, root: Path | str = ROOT_EXE_GAME) -> Path:
    actual: Path 
    if root is str:
        actual = Path(root)
    elif root is Path:
        actual = root
    else:
        actual = Path(".")
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
        return (
            name in SKIP_FOL_NAMES
            or name in RESERVED_GENERIC_FOLD_NAMES
        )
    elif kind == "file":
        return (
            name in SKIP_FILE_NAME
            or name in RESERVED_GENERIC_FILE_NAMES
        )
    else:
        return False

def get_list_system_file(
    kind: _literal_fields_files,
    origin: Path = Path("."),
    is_normal: bool = True
) -> list[str | list[str]]:
    
    match kind:
        case "both":
            return [
                list(filter(lambda x: not is_reserved(x, "file") if is_normal else  is_reserved(x, "file"), get_list_system_dirs(origin, "file"))),
                list(filter(lambda x: not is_reserved(x, "dir") if is_normal else  is_reserved(x, "dir"), get_list_system_dirs(origin, "dir")))
            ]
        case y if y in ["file", "dir"]:
            return list(filter(lambda x: not is_reserved(x, kind) if is_normal else  is_reserved(x, kind), get_list_system_dirs(origin, kind)))
        case _:
            return []

def get_list_file_extended(
    extension: str | list[str],
    is_normal: bool = True,
    *,
    origin: Path = Path("."),
    local : list[str] = []
) -> list[str]:
    local = (
        get_list_system_file("file", origin, is_normal) if len(local) == 0 else local
    )
    
    @singledispatch
    def extend(extension: str) -> list[str]:
        return [i for i in local if i[-len(extension) :] == extension]

    @extend.register
    def _(extension: list) -> list[str]:
        a = []
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
    local : list[str] = []
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
    local : list[str] = []
) -> list[str]:
    
    local = get_list_file_named(names, is_normal, origin=origin, local=local)
    local = get_list_file_extended(extesions, is_normal, origin=origin, local=local)
    
    return local

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
        checked : list[bool] = []
        
        while init.count(".") != 0:
            init.remove(".")
        
        for part in normal:
            if part in init:
                for n in range(len(init)):
                    
                    if not init[n] in normal:
                        checked.append(False)
                        break
                    
                    checked.append(normal[normal.index(part)+n] == init[n])
            if len(checked) != 0 and all(checked):
                return True
            
            checked = []
        return False
    
    dir_exits = wrapper(start)
    if not dir_exits:
        logger.warning(get_message_translated(MessagesError.PATH_NOT_FOUND, path=origin.resolve().as_posix()+" for "+str(start)))
        return origin.as_posix()
    return mkr_str(normal if not dir_exits else normal[normal.index("/".join(start)):] , "/") 

def scan_folder_for(folder: str, origin: Path = Path("."), is_normal: bool = True) -> bool:
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
    **kwargs
) -> list[T]:
    def wrapper(ori: Path = Path(".")) -> list[str]:
        return list(filter(lambda x: not x in exclude, get_list_system_file("dir", ori)))
    
    final: list[T] = []
    for name in wrapper(origin):
        origin = origin / name

        if not origin.exists():
            continue
    
        if len(wrapper(origin)) != 0:
            final += scan_subfolder_do(what, exclude=exclude, origin=origin, *args, **kwargs)
    
        if len(get_list_system_file("file", origin)) != 0:
            final += what(origin, *args, **kwargs)
    
        origin = origin / ".."
    
    return final

def scan_file_compressed(kind: _literal_fields_exten = "image", origin: Path = Path(".")) -> bool:
    if IGNORE_NOT_SUPPORTED:
        return False
    
    vr: list[str]
    match kind:
        case "image": vr = DEFAULT_EXTEND_IMAGE_NOT_SUPPORT
        case "sound": vr = DEFAULT_EXTEND_SOUND_NOT_SUPPORT
        case "video": vr = DEFAULT_EXTEND_VIDEO_NOT_SUPPORT
        case _:
            logger.warning(get_message_translated(MessagesError.ARGUMENT_NOT_FOUND, name=kind))
            vr = DEFAULT_EXTEND_IMAGE_NOT_SUPPORT
    
    files = get_list_file_extended(vr, origin=origin)
    has_files = len(files) != 0
    if has_files:
        message: list[str] = [get_message_translated(MessagesError.EXTENSION_ERROR)]
        for n in files:
            message.append(f"N: {len(message)} FILE: {n} BASED {origin.resolve().as_posix()}")
        message: str = mkr_str(add_jump(message))
        logger.warning(message)
        
    return has_files

def rm_defaults(origin: Path = Path(".")) -> None:
    if not __can_edit__:
        print(get_message_translated(MessagesError.FEATURE_NOT_SUPPORTED, name="rm_defaults", reason="the program can't edit/manipulate files"))
        return
    
    remove_file: Path = origin
    
    print(get_message_translated(MessagesMeta.MESSAGE_FUNCTION_INIT, name="Remove defaults"))
    result = "completed"
    #.copy() is fundamental to no add data to RESERVED_GENERIC_FILE_EXTEN or others
    extensions_to_delete: list[str] = RESERVED_GENERIC_FILE_EXTEN.copy()
    for file in tqdm(RESERVED_GENERIC_FILE_NAMES, colour=ColorPerLevel.INTERNAL, desc=get_message_translated(MessagesMeta.MESSAGE_FUNCTION_PROGRESS, name="Remove default")):
        try:
            if file in RESERVED_GENERIC_CREA_NAMES:
                extensions_to_delete+=RESERVED_GENERIC_CREA_EXTEN
            
            for extension in extensions_to_delete:
                remove_file = remove_file.joinpath(file+"."+extension)
                if not (remove_file.exists() and remove_file.is_file()):
                    continue
                
                remove(remove_file)
        except FileNotFoundError:
            logger.warning(get_message_translated(MessagesError.FILE_NOT_FOUND, file=file))
        except Exception as e:
            result = "unknown error"
            logger.warning(get_message_translated(MessagesMeta.MESSAGE_INFO, name=file, operation="Remove defaults", result=str(e)))
    print(get_message_translated(MessagesMeta.MESSAGE_FUNCTION_ENDED, name="Remove defaults", result=result))


########################################################
#
# Functionally related zone
#
########################################################
def get_name_acron(limit: int = 3, origin: Path = Path(".")) -> str:
    files_waited = RESERVED_GENERIC_FILE_NAMES[0:2] #character.rpy and its plural just in case
    _: Path = origin
    
    _tmp_file: list[str]
    file_acron: str = ""
    
    for i in tqdm(range(limit), colour=ColorPerLevel.INTERNAL, desc=get_message_translated( MessagesMeta.MESSAGE_FUNCTION_PROGRESS, name="getting acron")):
        _tmp_file = get_list_file_named(files_waited, False, origin=_)
        
        if len(_tmp_file) != 0:
            file_acron = _tmp_file[0]
            break
        _ = _ / ".."
    
    _ = _ / file_acron
    file_found: bool = not i + 1 >= limit or file_acron != ""
    is_empty  : bool = not (_.is_file and _.exists() and _.open().readlines() != 0)
    manual_use: bool = False
    if file_found and not is_empty:
        for line in _.open().read().split(","):
            a = line.split("=")
            del_jump(a)
            if a[0].replace(" ", "") == "image":
                file_acron = a[1].replace("\"", "").replace(")", "")
                break
    else:
        manual_use = True
        logger.warning(get_message_translated(MessagesMeta.MESSAGE_FUNCTION_ENDED, name="get_character_acron", result="character's file couldn't be found in "+str(_)+" based on "+str(origin)))

    if manual_use or file_acron == "":
        file_acron = get_path_parsed("images", origin)[1][:2]
    print(get_message_translated(MessagesMeta.MESSAGE_FUNCTION_ENDED, name="get_character_acron", result="founded and used with "+file_acron))
    return file_acron

def get_list_namesimple(origin: Path = Path(".")) -> list[str]:
    names: list[str] = []
    for name in get_list_system_file("dir", origin):
        
        if name in RESERVED_GENERIC_FOLD_NAMES[:-1]:
            continue
        
        origin = origin / name
        if not origin.exists():
            continue
        
        [names.append(get_path_parsed("assets", origin) + "/" + _name ) for _name in get_list_file_extended(DEFAULT_EXTEND_IMAGE_SUPPORT, origin=origin)]

        if len(get_list_system_file("dir")) != 0:
            names+= get_list_namesimple(origin)
        origin = origin / ".."
    return names

def get_name_template(
        file: str,
        path: str,
    ) -> tuple[str, str]:
    
    file = file.split(".")[0].translate(FILE_NAME_REPLACE)
    for origin, to in FILE_NAME_REPLACE_LONG.items():
        file.replace(origin, to)

    info: dict[str, str] = {
        "path": path,
        "file": file
    }
    couldnt_found: bool = False
    match DEFAULT_KIND_IMPORT:
        case "dev": #normal import
            path = BUILDIN_FILE_TEMPLATES[TemplatePath.NORMAL]
        case "source": #when encrypted
            path = BUILDIN_FILE_TEMPLATES[TemplatePath.ENCRYPT]
        case "zip": #when exported as .zip file, your renpy SDK should support this feature
            if not TemplateKeys.ZIPLOAD in FORMATS_IMPORTED:
                path = BUILDIN_FILE_TEMPLATES[TemplatePath.NORMAL]
                logger.warning(get_message_translated(MessagesError.ARGUMENT_NOT_FOUND, name=TemplateKeys.ZIPLOAD))
                couldnt_found = True
            else:
                path = BUILDIN_FILE_TEMPLATES[TemplatePath.ZIP]
        case _:
            path = BUILDIN_FILE_TEMPLATES[TemplatePath.NORMAL]
            couldnt_found = True

    if couldnt_found:
        logger.warning(get_message_translated(MessagesError.INCORRECT_ARGUMENTS, arguments=DEFAULT_KIND_IMPORT, default=TemplatePath.NORMAL, message="get_name_template" ))

    path = path % info

    return file, path

def write_side_image(
    size: tuple[int, int, int, int],
    load: dict[TemplatePathKeys, str | list[str]],
    file_generation_limit: int = 99,
    custom: dict[str, list[str]] = BUILDIN_NAME_ANIMATION
) -> bool:
    if not __can_edit__ or not ( has_feature(FeaturesKeywords.IMAGE_CREATION) or has_feature(FeaturesKeywords.IMAGE_CREATION, False) ):
        logger.warning(get_message_translated(MessagesError.FEAUTRE_NOT_FOUND, name="write_side_image"))
        return False
    
    try:
        size = [int(i) for i in size]
    except TypeError as msg:
        print(get_message_translated(MessagesMeta.MESSAGE_INFO, name="write_side_image", operation="int convertion", result=msg.args))
        size = DEFAULT_SIZE_SIDE_VAR
    
    #check the fields required (just in case)
    if not has_required_keys(load.keys(), TemplatePathKeys, "write_side_image"):
        return False
    
    origin: Path = Path(DEFAULT_PATH_SIDE % load)
    if not origin.exists():
        return False
    
    _ = origin / ".."
    
    if not _.exists():
        return False
    
    files: list[str] = get_list_file_named(custom, origin=_)[:file_generation_limit]
    
    try:
        rmtree(origin)
    except FileNotFoundError:
        pass
    
    print(get_message_translated(MessagesMeta.MESSAGE_FUNCTION_INIT, name="write_side_image"))
    mkr_dir("side", _)
    has_error: bool = False
    
    file_path_side: Path
    file_path_orin: Path
    
    for file in tqdm(files, colour=ColorPerLevel.INTERNAL, desc=get_message_translated(MessagesMeta.MESSAGE_FUNCTION_PROGRESS, name="write side images for "+ load[TemplatePathKeys.NAME][-1])):
        file_path_side = origin / file # include '/side'
        file_path_orin = _ / file      # just its base without '/side'
        
        if not file_path_orin.exists():
            logger.warning(get_message_translated( MessagesError.PATH_NOT_FOUND, path=file_path_orin.as_posix()))
            continue
        
        try:
            Image.open(file_path_orin).crop(size).save(file_path_side)
        except (UnidentifiedImageError, ValueError, OSError) as msg:
            logger.warning(get_message_translated(MessagesMeta.MESSAGE_FUNCTION_ENDED, name="write_side_image", result=msg.args))
            has_error = True
    print(get_message_translated(MessagesMeta.MESSAGE_FUNCTION_ENDED, name="write_side_image", result=f"ERROR: {str(has_error)}"))

def write_common_file(modes: list[str], info: ConfigParser, origin: Path = Path(".")) -> None:
    if not origin.exists():
        logger.warning(get_message_translated(MessagesError.PATH_NOT_FOUND, path=origin.resolve().as_posix()))
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
        #smart way to get the file's type based 
        files = scan_subfolder_do(lambda: get_list_system_file("file") if len(get_list_system_file("file")) != 0 else [], origin=origin)
        #yet, not the smartest way possible
        if len(files) != 0 and files[0].count(".") != 0:
            extension: str = files[0].split(".")[1]
            
            match extension:
                case x if x in DEFAULT_EXTEND_IMAGE_SUPPORT: kind = "image"
                case x if x in DEFAULT_EXTEND_SOUND_SUPPORT: kind = "sound"
                case x if x in DEFAULT_EXTEND_VIDEO_SUPPORT: kind = "video"
                case _:
                    kind = "image"
        else:
            kind = "image"
        
        logger.warning(get_message_translated(MessagesMeta.INCORRECT_ARGUMENTS, arguments=str(modes), default=kind, message=origin.as_posix()))
    
    scan_file_compressed(kind, origin)
    rm_defaults(origin)

    resource_path = (DEFAULT_PATH_IMAGE if kind == "image" else (DEFAULT_PATH_SOUND if kind == "sound" else DEFAULT_PATH_VIDEO) ) 
    
    if resource_path.count("%(base)s") == 0:
        logger.critical(get_message_translated(MessagesMeta.MESSAGE_FUNCTION_ENDED, name="write_common_file", result="%(base)s not found"))
        return
    
    resource_path %= {"base": DEFAULT_RESOURCE_PATH}
    simple_path_base = get_path_parsed(resource_path.split("/"), origin)
    if len(simple_path_base.split("/")) <= 1:
        logger.warning(get_message_translated(MessagesMeta.MESSAGE_FUNCTION_ENDED, name="write_common_file", result=simple_path_base))
        return
    
    extra_import: str            = simple_path_base.split("/")[-2] if len(simple_path_base.split("/")) >= 2 else ""
    from_name   : list[str]      = simple_path_base.split("/", 1)[1].split("/")
    #NOTE: maybe if use an Enum instead of Literal... that might be useful
    local_vars  : dict[_literal_image_argumt, str] = {}
    
    load_util: dict[TemplatePathKeys, str | list[str]] = {
        TemplatePathKeys.BASE: simple_path_base,
        TemplatePathKeys.NAME: from_name
    }
    
    match extra_import:
        case "side":
            acron = get_name_acron(origin=origin)
            local_vars["acron"] = acron
            size: tuple[int, int, int, int] = info.get(ImageConfigHead.SIDE, ImageConfigValue.SIZE, fallback=lambda: DEFAULT_SIZE_CORP_VAR)
            
            animation_keys: dict[str, list[str]] | str = info.get(ImageConfigHead.ANIMATION, ImageConfigValue.KEYS, fallback=lambda: BUILDIN_NAME_ANIMATION)
            
            if isinstance(animation_keys, str):
                fields: list[str] = animation_keys.split(";")
                for part in fields:
                    
                    if part.count(":") == 0:
                        continue
                    #TODO: add check in case this fails
                    animation_keys[part.split(":")[0]] = part.split(":")[1].split(",")
            
            write_side_image(size, load_util, custom=animation_keys)


########################################################
#
# Lines generated related zone
#
########################################################
def mkr_lines_list(simple_path: str, files: list[str], modes: list[str], folder: Path = Path(".")) -> list[str]:
    #NOTE: well... this is mostly a TODO than a NOTE, but... I think we could do better if we
    # check simple_path and folder, there might be a case where they might are not realted
    # since this funciton excepts both be related to the other
    lines: list[str] = []
    print(get_message_translated(MessagesMeta.MESSAGE_FUNCTION_INIT, name=simple_path))
    file_parts: list[tuple[str, str]] = []
    
    for file in tqdm(files, colour=ColorPerLevel.GENERIC, desc=get_message_translated(MessagesMeta.MESSAGE_FUNCTION_PROGRESS, name="Parsing names...")):
        file_parts.append(get_name_template(file, simple_path))
    
    
    return lines
    )
