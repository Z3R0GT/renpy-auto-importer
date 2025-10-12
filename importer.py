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
from os import listdir, chdir, getcwd, remove

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
    FEATURE_NOT_SUPPORTED = "FEATURE_NOT_SUPPORTED"
    ARGUMENT_NOT_FOUND = "ARGUMENT_NOT_FOUND"
    EXTENSION_ERROR = "EXTENSION_ERROR"


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
        MessagesError.MODULE_NOT_FOUND_USING_DEFAULT: "There's not '{name}' installed, using default",
        MessagesError.MODULE_NOT_FOUND     : "There's not '{name}' installed",
        MessagesError.FEAUTRE_NOT_FOUND    : "The {name} feature couldn't be found",
        MessagesError.ARGUMENT_NOT_FOUND   : "The {name} argument couldn't be found",
        MessagesError.FILE_NOT_FOUND       : "The {file} file couldn't be found",
        MessagesError.USING_BUILT_IN       : "Using {name} built-in instead",
        MessagesMeta.DESCRIPTION           : "This is a simple tool easy-to-use to import assets and stuff from normal files to common.rpy files",
        MessagesError.FEATURE_NOT_SUPPORTED: "The feature '{name}' is not supported due to {reason}",
        MessagesMeta.MESSAGE_INFO          : "Given '{name}' was made the operation '{operation}' with result '{result}'",
        MessagesMeta.MESSAGE_FUNCTION_INIT : "The operation '{name}' was started",
        MessagesMeta.MESSAGE_FUNCTION_PROGRESS: "Resolving '{name}' operation",
        MessagesMeta.MESSAGE_FUNCTION_ENDED: "The operation '{name}' was ended with '{result}' as result",
        MessagesError.EXTENSION_ERROR      : "There are some files that might need change its extension or be compressed:"
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

BUILDIN_TEMPLATES: dict[TemplateKeys, dict[str, dict[str, list[str] | str] | list[str]] | str] = {
    TemplateKeys.NORMAL: "image %(name)s = %(path)s\n",
    TemplateKeys.SCALE: "image %(name)s = im.Scale(%(path)s, %(size)s)\n",
    TemplateKeys.FLIPED: "image %(name)s flip = im.Flip(%(path)s, horizontal=True)\n",
    TemplateKeys.SIDE: "image side {abbr} %(name)s = im.Scale(%(path)s, %(size)s)\n",
    TemplateKeys.SOUND: "define audio.%(name)s = %(path)s\n",
    TemplateKeys.VIDEO: "image %(name)s = Movie(play=%(path)s, bypass=True)\n",
    TemplateKeys.ZIPLOAD: "renpy.loadbytes(' %(file)s', '%(path)s', '%(kind)s')"
}
BUILDIN_PATH_TEMPLATES: dict[TemplatePath, str] = {
    TemplatePath.ENCRYPT: "%(path)s/%(file)s.enc",
    TemplatePath.NORMAL : "%(path)s/%(file)s",
    TemplatePath.ZIP    : "%(path)s/%(file)s.zip"
    
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
FORMATS_IMPORTED: dict[TemplateKeys, dict[str, dict[str, list[str] | str] | list[str]] | str]
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

def get_path_parsed(start: str, origin: Path = Path(".")) -> str:
    if not origin.is_dir():
        origin = Path(mkr_str(origin.as_posix().split("/")[:-1]))
    normal: list[str] = origin.as_posix().split("/")
    dir_exits = start in normal
    if not dir_exits:
        #TODO: mensaje de error
        return origin.as_posix()
    return mkr_str(normal if not dir_exits else normal[normal.index(start):] , "/") 

def scan_folder_for(folder: str, origin: Path = Path("."), is_normal: bool = True) -> bool:
    folders: list[str] = get_list_system_file("dir", origin, is_normal)
    if folder in folders:
        return True
    
    for name in folders:
        origin = origin / name
        if not origin.exists():
            #TODO: add error
            continue
        
        if scan_folder_for(folder, origin, is_normal):
            return True
        
        origin = origin / ".."
    
    return False

def scan_subfolder_do[T](
    what: Callable[[], T],
    exclude: Sequence[str],
    origin: Path = Path("."),
    *args,
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
            scan_subfolder_do(what, exclude, origin, *args, **kwargs)
    
        if len(get_list_system_file("file", origin)) != 0:
            final+=what(*args, **kwargs)
    
        origin = origin / ".."
    
    return final

def scan_file_compressed(kind: _literal_fields_exten = "image", origin: Path = Path(".")) -> bool:
    
    vr: list[str]
    match kind:
        case "image": vr = DEFAULT_EXTEND_IMAGE_NOT_SUPPORT
        case "sound": vr = DEFAULT_EXTEND_SOUND_NOT_SUPPORT
        case "video": vr = DEFAULT_EXTEND_VIDEO_NOT_SUPPORT
        case _:
            print(get_message_translated(MessagesError.ARGUMENT_NOT_FOUND, name=vr))
            vr = DEFAULT_EXTEND_IMAGE_NOT_SUPPORT
    
    files = get_list_file_extended(vr, origin=origin)
    has_files = len(files) != 0
    if has_files:
        message: list[str] = [get_message_translated(MessagesError.EXTENSION_ERROR)]
        for n in files:
            message.append(f"N: {len(message)} FILE: {n} BASED {origin.resolve().as_posix()}")
        message: str = mkr_str(add_jump(message))
        print(message)
        logger.warning(message)
        
    return has_files

def rm_defaults(origin: Path = Path(".")) -> None:
    if not __can_edit__:
        logger.warning(get_message_translated(MessagesError.FEATURE_NOT_SUPPORTED, name="rm_defaults", reason="the program can't edit/manipulate files"))
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
            print(get_message_translated(MessagesError.FILE_NOT_FOUND, file=file))
        except Exception as e:
            result = "unknown error"
            print(get_message_translated(MessagesMeta.MESSAGE_INFO, name=file, operation="Remove defaults", result=str(e)))
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
        print(get_message_translated(MessagesMeta.MESSAGE_FUNCTION_ENDED, name="get_character_acron", result="character's file couldn't be found in "+str(_)+" based on "+str(origin)))

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
        kind: _literal_fields_exten = "images",
        mode: tuple[bool, int] = (False, 0)
    ) -> tuple[str, str]:
    
    file = file.split(".")[0].translate(FILE_NAME_REPLACE)
    for origin, to in FILE_NAME_REPLACE_LONG.items():
        file.replace(origin, to)

    info: dict[str, str] = {
        "path": path,
        "file": file
    }

    match DEFAULT_KIND_IMPORT:
        case "dev": #normal import
            path = BUILDIN_PATH_TEMPLATES[TemplatePath.NORMAL]
        case "source": #when encrypted
            path = BUILDIN_PATH_TEMPLATES[TemplatePath.ENCRYPT]
        case "zip": #when exported as .zip file, your renpy SDK should support this feature
            if not TemplateKeys.ZIPLOAD in FORMATS_IMPORTED:
                path = BUILDIN_PATH_TEMPLATES[TemplatePath.NORMAL]
            else:
                path = BUILDIN_PATH_TEMPLATES[TemplatePath.ZIP]
            

    path = path % info

    return file, path


