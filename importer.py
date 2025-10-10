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
from os import listdir, path, chdir

########################################################
#
# Meta zone
#
########################################################
__version__ = "1.0.4.6-dev"
__return__ = 0
__product__ = "importer"
__author__ = "Z3R0_GT"
__is_main__ = __name__ == "__main__"
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

if sys.version_info >= (3, 15):
    __return__ = 2
    logger.fatal(
        "The python version used is actually unsupported and shouldn't be used due some problems"
    )
    if __is_main__:
        raise Exception(
            "The python version used actually unsupported due a library incompatibility"
        )

from enum import IntEnum, StrEnum

# We ignore 'locale.getdefaultlocale' watning
warnings.filterwarnings("ignore", ".*is deprecated and slated for removal in.*")
try:
    from locale import getdefaultlocale
except ImportError:
    def getdefaultlocale() -> tuple:
        return ("en", 0)


from argparse import ArgumentParser
from shutil import rmtree


from functools import singledispatch
from types import FunctionType

from pathlib import Path
from subprocess import run
from json import load, loads, dump, dumps


########################################################
#
# Enums zone
#
########################################################
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
    USING_BUILT_IN = "USING_BUILT_IN"


class MessagesMeta(StrEnum):
    DESCRIPTION = "DESCRIPTION"

########################################################
#
# Features zone
#
########################################################
features: list[str] = []


def add_feature(what: FeaturesKeywords) -> bool:
    global features
    if not what in FeaturesKeywords:
        return False
    features.append(what)
    return True


def has_feature(what: FeaturesKeywords) -> bool:
    return what in FeaturesKeywords and what in features


########################################################
#
# Messages/Language built-in zone
#
########################################################
logger.info("Starting language service")
languages: dict[str, dict[str, str]] = {
    "en": {
        MessagesError.MODULE_NOT_FOUND: "There's not '{name}' installed",
        MessagesError.MODULE_NOT_FOUND_USING_DEFAULT: "There's not '{name}' installed, using default",
        MessagesError.FEAUTRE_NOT_FOUND: "The {name} feature couldn't be found",
        MessagesError.FILE_NOT_FOUND: "The {file} file couldn't be found",
        MessagesError.USING_BUILT_IN: "Using {name} built-in instead",
        MessagesMeta.DESCRIPTION: "This is a simple tool easy-to-use to import assets and stuff from normal files to common.rpy files"
    }
}
logger.info("Built-in languages: " + str(list(languages.keys())))
os_language = getdefaultlocale()[0].split("_")[0] # type: ignore
logger.info("OS language detected: " + os_language)
language: str = os_language if os_language in languages.keys() else "en"
logger.info("Selected language: " + language)
logger.info("Language service ended")


def get_message_translated(name: str) -> str:
    if not name in languages[language]:
        logger.debug(
            "The key '{}' couldn't be found base in the language {}".format(
                name, language
            )
        )
        return ""

    return languages[language][name]


########################################################
#
# Imports specifc zone
#
########################################################
logger.info("Starting phase 1: Importing extra module")
try:
    from typing_extensions import (
        Sequence,
        overload,
        Literal,
        Any,
    )
except ModuleNotFoundError:
    logger.fatal(get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="typing_extensions"))
    __return__ = 1

try:
    from pyminizip import compress_multiple

    if not add_feature(FeaturesKeywords.ZIP_COMPRESSION):
        logger.info(get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name=FeaturesKeywords.ZIP_COMPRESSION))
except ModuleNotFoundError:

    def compress_multiple(*args, **kwargs):
        logger.warning(get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="pyminizip"))


try:
    from tqdm import tqdm

    if not add_feature(FeaturesKeywords.PRETTY_CONSOLE):
        logger.info(get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name=FeaturesKeywords.PRETTY_CONSOLE))
except ModuleNotFoundError:
    logger.warning(get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="tqdm"))

try:
    from PIL import Image, UnidentifiedImageError

    if not add_feature(FeaturesKeywords.IMAGE_CREATION):
        logger.info(get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name=FeaturesKeywords.IMAGE_CREATION))
except ModuleNotFoundError:
    logger.warning(get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="pillow"))

try:
    from whoosh.filedb.filestore import RamStorage
    from whoosh.qparser import MultifieldParser
    from whoosh.fields import TEXT, Schema

    if not add_feature(FeaturesKeywords.RENAMING_PROCESS):
        logger.info(get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name=FeaturesKeywords.RENAMING_PROCESS))
except ModuleNotFoundError:
    logger.warning(get_message_translated(MessagesError.MODULE_NOT_FOUND).format(name="whoosh"))

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

########################################################
#
# Extensions zone
#
########################################################
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
RESERVED_GENERIC_FOLD_NAMES: tuple[str, str, str, str] = (
    "generic_template",
    "side",
    "logs",
    "interactive",
)
RESERVED_GENERIC_CREA_NAMES: tuple[str, str, str] = ("common", "common_test", "common_dist")

########################################################
#
# Etc zone
#
########################################################
ZIP_PASSWORD: str = ""
DEFAULT_TAB: int = 4
INPUT_FORM: str = f"\n>{"."*DEFAULT_TAB}"
DEFAULT_KIND_IMPORT: Literal["source", "dev", "zip"] = "dev"


BUILDIN_TEMPLATES: dict[str, dict[str, dict[str, list[str] | str] | list[str]] | str] = {
    "normal": "image %(name)s = %(path)s\n",
    "scale": "image %(name)s = im.Scale(%(path)s, %(size)s)\n",
    "fliped": "image %(name)s flip = im.Flip(%(path)s, horizontal=True)\n",
    "side": "image side {abbr} %(name)s = im.Scale(%(path)s, %(size)s)\n",
    "sound": "define audio.%(name)s = %(path)s\n",
    "video": "image %(name)s = Movie(play=%(path)s, bypass=True)\n",
}

########################################################
#
# Path handlers zone
#
########################################################
ROOT_EXE_GAME: Path = Path(".")
ROOT_RES_SOFT: Path = Path(user_data_dir(__product__, __author__))

_literal_fields = Literal["dir", "file", "both"]
def get_from_directory(
    origin: Path = Path("."), kind: _literal_fields = "file", **kwargs
) -> list[str | list[str]]:
    match kind:
        case "both":
            return [
                list(filter(path.isfile, listdir(origin))),
                list(filter(path.isdir, listdir(origin))),
            ]
        case "dir":
            return list(filter(path.isdir, listdir(origin)))
        case "file":
            return list(filter(path.isfile, listdir(origin)))


logger.info("Starting phase 2: importing config files")
FORMATS_IMPORTED: dict[str, dict[str, dict[str, list[str] | str] | list[str]] | str]
if RequiredFiles.TEMPLATES in get_from_directory(ROOT_EXE_GAME, "file"):
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
    chdir(cur)
    return cur

def is_reserved(name: str, kind: _literal_fields = "file") -> bool:
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

def get_name_as(
    kind: _literal_fields,
    origin: Path = Path("."),
    is_normal: bool = True
) -> list[str | list[str]]:
    
    match kind:
        case "both":
            return [
                list(filter(lambda x: not is_reserved(x, "file") if is_normal else  is_reserved(x, "file"), get_from_directory(origin, "file"))),
                list(filter(lambda x: not is_reserved(x, "dir") if is_normal else  is_reserved(x, "dir"), get_from_directory(origin, "dir")))
            ]
        case y if y in ["file", "dir"]:
            list(filter(lambda x: not is_reserved(x, kind) if is_normal else  is_reserved(x, kind), get_from_directory(origin, kind)))
        case _:
            return []

def get_names_end_with(
    extension: str | list[str],
    is_normal: bool = True,
    *,
    origin: Path = Path("."),
    local : list[str] = []
) -> list[str]:
    local = (
        get_name_as("file", origin, is_normal) if len(local) == 0 else local
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

def get_names_named_with(
    names: str | Sequence[str] | dict[str | Sequence[str]],
    is_normal: bool = True,
    *,
    origin: Path = Path("."),
    local : list[str] = []
) -> list[str]:
    local = (
        get_name_as("file", origin, is_normal) if len(local) == 0 else local
    )
    end: list[str]
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

def get_names_filtered(
    names: list[str],
    extesions: list[str],
    is_normal: bool = True,
    origin: Path = Path("."),
    local : list[str] = []
) -> list[str]:
    
    local = get_names_named_with(names, is_normal, origin=origin, local=local)
    local = get_names_end_with(extesions, is_normal, origin=origin, local=local)
    
    return local

def get_parsed_path(start: str, origin: Path = Path(".")) -> str:
    normal: list[str] = origin.as_posix().split("/")
    dir_exits = start in normal
    if not dir_exits:
        #TODO: mensaje de error
        pass
    return mkr_str(normal if not dir_exits else normal[normal.index(start):] , "/") 
    


