import os

DIR_MAIN = os.getcwd()
DIR_LOGS = "/logs"
DIR_RESULT = "/results"
DIR_EXPERIMENT = "/experiment"

TOOL_NAME = "Cerberus"

CONF_DATA_PATH = "/data"
CONF_TOOL_PATH = ""
CONF_TOOL_PARAMS = ""
CONF_TOOL_NAME = None
CONF_TOOL_LIST = []
CONF_DEBUG = False
CONF_BUG_INDEX = None
CONF_BUG_ID = None
CONF_START_INDEX = None
CONF_END_INDEX = None
CONF_SETUP_ONLY = False
CONF_BUG_INDEX_LIST = None
CONF_BUG_ID_LIST = None
CONF_SKIP_LIST = None
CONF_BENCHMARK = None
CONF_CONFIG_ID_LIST = ["C1"]
CONF_SUBJECT_NAME = None
CONF_PURGE = False
CONF_RUN_TESTS_ONLY = False
CONF_INSTRUMENT_ONLY = False
CONF_ANALYSE_ONLY = False
CONF_SHOW_DEV_PATCH = False
CONF_USE_CONTAINER = False
CONF_DUMP_PATCHES = False
CONF_USE_VALKYRIE = False


DEFAULT_STACK_SIZE = 15000
DEFAULT_TEST_TIMEOUT = 5
DEFAULT_VALKYRIE_TIMEOUT = 1
DEFAULT_VALKYRIE_WAIT_TIME = 0.1
DEFAULT_DISK_SPACE = 5  # 5GB
DEFAULT_DUMP_PATCHES = False
CONF_ARG_PASS = False
ITERATION_NO = -1
DEFAULT_RUN_TESTS_ONLY = False
DEFAULT_ANALYSE_ONLY = False
DEFAULT_SETUP_ONLY = False
DEFAULT_USE_CONTAINER = True
ANALYSIS_RESULTS = dict()
CONFIG_ID = None
DEFAULT_USE_VALKYRIE = False

APR_TOOL_RUNNING = False
LIST_CONSUMED = []
LIST_PROCESSING = []
LIST_PROCESSED = []
LIST_VALID = []
LIST_INVALID = []
LIST_ERROR = []

