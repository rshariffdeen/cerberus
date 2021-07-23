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
CONF_DEBUG = False
CONF_BUG_ID = None
CONF_START_ID = None
CONF_END_ID = None
CONF_SETUP_ONLY = False
CONF_BUG_ID_LIST = None
CONF_SKIP_LIST = None
CONF_BENCHMARK = None
CONF_CONFIG_ID_LIST = ["C1"]
CONF_SUBJECT_NAME = None
CONF_PURGE = False

DEFAULT_STACK_SIZE = 15000
DEFAULT_DISK_SPACE = 5  # 5GB
CONF_ARG_PASS = False
ITERATION_NO = -1