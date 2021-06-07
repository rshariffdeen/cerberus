import sys
import json
import subprocess
import os

KEY_BUG_ID = "bug_id"
KEY_BENCHMARK = "benchmark"
KEY_ID = "id"
KEY_SUBJECT = "subject"
KEY_FIX_FILE = "source_file"
KEY_FIX_LINE = "line_number"
KEY_PASSING_TEST = "passing_test"
KEY_FAILING_TEST = "failing_test"
KEY_CONFIG_TIMEOUT = "timeout"
KEY_CONFIG_FIX_LOC = "fault_location"
KEY_CONFIG_TEST_RATIO = "passing_test_ratio"


ARG_DATA_PATH = "--data-dir="
ARG_TOOL_PATH = "--tool-path="
ARG_TOOL_NAME = "--tool="
ARG_TOOL_PARAMS = "--tool-param="
ARG_DEBUG_MODE = "--debug"
ARG_ONLY_SETUP = "--only-setup"
ARG_BUG_ID = "--bug-id="
ARG_START_ID = "--start-id="
ARG_END_ID = "--end-id="
ARG_SKIP_LIST = "--skip-list="
ARG_BUG_ID_LIST = "--bug-id-list="
ARG_BENCHMARK = "--benchmark="
ARG_CONFIG_ID = "--conf="


CONF_DATA_PATH = "/data"
CONF_TOOL_PATH = "/CPR"
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
CONF_CONFIG_ID = "C1"

FILE_META_DATA = None
FILE_CONFIGURATION = "configuration.json"
FILE_ERROR_LOG = "error-log"
FILE_OUTPUT_LOG = ""
FILE_SETUP_LOG = ""
FILE_INSTRUMENT_LOG = ""


DIR_MAIN = os.getcwd()
DIR_LOGS = DIR_MAIN + "/logs"
DIR_RESULT = DIR_MAIN + "/results"
DIR_EXPERIMENT_RESULT = DIR_RESULT + "/test"


EXPERIMENT_ITEMS = list()
CONFIG_INFO = dict()


def create_directories():
    if not os.path.isdir(DIR_LOGS):
        create_command = "mkdir " + DIR_LOGS
        execute_command(create_command)
    if not os.path.isdir(DIR_RESULT):
        create_command = "mkdir " + DIR_RESULT
        execute_command(create_command)


def execute_command(command):
    if CONF_DEBUG:
        print("\t[COMMAND]" + command)
    process = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    (output, error) = process.communicate()
    return int(process.returncode)


def load_experiment_details(meta_file):
    print("[DRIVER] Loading experiment data\n")
    json_data = None
    if os.path.isfile(meta_file):
        with open(meta_file, 'r') as in_file:
            json_data = json.load(in_file)
    else:
        exit("Meta file does not exist")
    return json_data


def load_configuration_details(config_file_path, config_id):
    print("[DRIVER] Loading configuration setup\n")
    json_data = None
    if os.path.isfile(config_file_path):
        with open(config_file_path, 'r') as conf_file:
            json_data = json.load(conf_file)
    else:
        exit("Configuration file does not exist")
    return json_data[config_id]


def setup_experiment(script_path, bug_id):
    global FILE_ERROR_LOG, CONF_DATA_PATH, FILE_SETUP_LOG
    print("\t[INFO] running script for setup")
    FILE_SETUP_LOG = DIR_LOGS + "/" + str(bug_id) + "-setup.log"
    setup_command = "cd " + script_path + "; { "
    setup_command += "bash setup.sh; "
    setup_command += "bash config.sh; "
    setup_command += "bash build.sh; "
    setup_command += "bash test.sh; "
    setup_command += " } >" + FILE_SETUP_LOG + " 2>&1"
    execute_command(setup_command)


def clean_results(exp_dir):
    if os.path.isdir(exp_dir):
        rm_command = "rm -rf " + exp_dir + "*"
        execute_command(rm_command)
    mk_command = "mkdir " + exp_dir
    execute_command(mk_command)


def archive_results(exp_dir):
    # copy logs
    copy_command = "cp " + FILE_SETUP_LOG + " " + DIR_EXPERIMENT_RESULT + ";"
    if os.path.isfile(FILE_OUTPUT_LOG):
        copy_command += "cp " + FILE_OUTPUT_LOG + " " + DIR_EXPERIMENT_RESULT + ";"
    if os.path.isfile(FILE_INSTRUMENT_LOG):
        copy_command += "cp " + FILE_INSTRUMENT_LOG + " " + DIR_EXPERIMENT_RESULT + ";"
    execute_command(copy_command)
    result_dir = "/".join(str(exp_dir).split("/")[:-1])
    exp_dir_id = str(exp_dir).split("/")[-1]
    archive_command = "cd " + result_dir + "; tar cvzf " + exp_dir_id + ".tar.gz " + exp_dir_id
    execute_command(archive_command)


# TODO: Make sure to copy the artifacts (patches) to DIR_EXPERIMENT_RESULT
def cpr(setup_dir_path, deploy_path, bug_id, passing_test_list, failing_test_list, fix_location):
    global CONF_TOOL_PARAMS, CONF_TOOL_PATH, CONF_TOOL_NAME, DIR_LOGS
    print("\t[INFO] instrumentation for CPR")
    conf_path = deploy_path + "/repair.conf"
    script_path = "instrument.sh"
    log_path = str(conf_path).replace(".conf", ".log")
    if not os.path.isfile(conf_path):
        setup_dir_path = setup_dir_path + "/cpr"
        instrument_command = "cd " + setup_dir_path + "; bash " + script_path + " " + CONF_DATA_PATH + " > /dev/null 2>&1"
        execute_command(instrument_command)
    print("\t[INFO] running CPR")
    tool_command = "{ " + CONF_TOOL_NAME + " --conf=" + conf_path + " " + CONF_TOOL_PARAMS + ";} 2> " + FILE_ERROR_LOG
    execute_command(tool_command)
    exp_dir = DIR_EXPERIMENT_RESULT + "/" + str(bug_id)
    if os.path.isdir(exp_dir):
        rm_command = "rm -rf " + exp_dir
        execute_command(rm_command)
    mk_command = "mkdir " + exp_dir
    execute_command(mk_command)
    copy_output = "{ cp -rf " + CONF_TOOL_PATH + "/output/" + bug_id + " " + exp_dir + ";} 2> " + FILE_ERROR_LOG
    execute_command(copy_output)
    copy_log = "{ cp " + CONF_TOOL_PATH + "/logs/log-latest " + exp_dir + ";} 2> " + FILE_ERROR_LOG
    execute_command(copy_log)
    copy_log = "cp " + FILE_ERROR_LOG + " " + exp_dir
    execute_command(copy_log)


def angelix(setup_dir_path, deploy_path, bug_id, timeout, passing_test_list, failing_test_list, fix_location):
    global CONF_TOOL_PARAMS, CONF_TOOL_PATH, CONF_TOOL_NAME, DIR_LOGS
    global FILE_INSTRUMENT_LOG, FILE_OUTPUT_LOG
    print("\t[INFO] instrumentation for angelix")
    script_path = "angelix/instrument.sh"
    FILE_INSTRUMENT_LOG = DIR_LOGS + "/" + bug_id + "-instrument.log"
    if not os.path.isfile(deploy_path + "/src/INSTRUMENTED_ANGELIX"):
        instrument_command = "cd " + setup_dir_path + "; bash " + script_path + " " + deploy_path + " > " + FILE_INSTRUMENT_LOG + " 2>&1"
        execute_command(instrument_command)
    print("\t[INFO] running Angelix")
    line_number = ""
    if fix_location:
        source_file, line_number = fix_location.split(":")
    else:
        with open(deploy_path + "/manifest.txt", "r") as man_file:
            source_file = man_file.readlines()[0].strip().replace("\n", "")

    src_path = deploy_path + "/src"
    gold_path = deploy_path + "/src-gold"
    angelix_dir_path = deploy_path + '/angelix'
    oracle_path = angelix_dir_path + "/oracle"
    config_script_path = angelix_dir_path + '/config'
    build_script_path = angelix_dir_path + '/build'
    timeout_s = int(timeout) * 3600
    syn_timeout = int(0.25 * timeout_s * 1000)
    FILE_OUTPUT_LOG = DIR_LOGS + "/" + bug_id + "-output.log"
    test_id_list = ""
    for test_id in failing_test_list:
        test_id_list += test_id + " "
    if passing_test_list:
        for test_id in passing_test_list:
            test_id_list += test_id + " "
    # initialize_command = "source /angelix/activate"
    # execute_command(initialize_command)
    angelix_command = "angelix {0} {1} {2} {3}  " \
                      "--configure {4}  " \
                      "--golden {5}  " \
                      "--build {6} " \
                      "--synthesis-timeout {7} ".format(src_path, source_file, oracle_path,
                                                        test_id_list, config_script_path, gold_path,
                                                        build_script_path, str(syn_timeout))

    if fix_location:
        angelix_command += " --lines {0}  --generate-all ".format(line_number)

    angelix_command += " {0} " \
                       " --timeout {1} > {2} 2>&1 ".format(CONF_TOOL_PARAMS, str(timeout_s), FILE_OUTPUT_LOG)
    execute_command(angelix_command)

    # move patches to result directory
    copy_command = "mv src-2021-* " + DIR_EXPERIMENT_RESULT
    execute_command(copy_command)


def prophet(setup_dir_path, deploy_path, bug_id, timeout, passing_test_list, failing_test_list, fix_location):
    # TODO: Make sure to copy the artifacts (logs/patches) to DIR_EXPERIMENT_RESULT
    print("\t[INFO] running Prophet")


def genprog(setup_dir_path, deploy_path, bug_id, timeout, passing_test_list, failing_test_list, fix_location):
    # TODO: Make sure to copy the artifacts (logs/patches) to DIR_EXPERIMENT_RESULT
    print("\t[INFO] running GenProg")


def fix2fit(setup_dir_path, deploy_path, bug_id, timeout, passing_test_list, failing_test_list, fix_location):
    # TODO: Make sure to copy the artifacts (logs/patches) to DIR_EXPERIMENT_RESULT
    print("\t[INFO] running Fix2Fit")


def repair(deploy_path, setup_dir_path, experiment_info):
    global CONF_TOOL_NAME, CONF_CONFIG_ID, FILE_CONFIGURATION, CONFIG_INFO, DIR_EXPERIMENT
    bug_id = str(experiment_info[KEY_BUG_ID])
    fix_source_file = str(experiment_info[KEY_FIX_FILE])
    fix_line_number = str(experiment_info[KEY_FIX_LINE])
    passing_test_list = experiment_info[KEY_PASSING_TEST].split(", ")
    failing_test_list = experiment_info[KEY_FAILING_TEST].split(", ")
    timeout = CONFIG_INFO[KEY_CONFIG_TIMEOUT]
    test_ratio = float(CONFIG_INFO[KEY_CONFIG_TEST_RATIO])
    passing_test_list = passing_test_list[:int(len(passing_test_list) * test_ratio)]
    fix_location = None

    if CONFIG_INFO[KEY_CONFIG_FIX_LOC] == "dev":
        fix_location = fix_source_file + ":" + fix_line_number

    if CONF_TOOL_NAME == "cpr":
        cpr(setup_dir_path, deploy_path, bug_id, timeout, test_ratio)
    elif CONF_TOOL_NAME == "angelix":
        angelix(setup_dir_path, deploy_path, bug_id, timeout, passing_test_list, failing_test_list, fix_location)
    elif CONF_TOOL_NAME == "prophet":
        prophet(setup_dir_path, deploy_path, bug_id, timeout, passing_test_list, failing_test_list, fix_location)
    elif CONF_TOOL_NAME == "fix2fit":
        fix2fit(setup_dir_path, deploy_path, bug_id, timeout, passing_test_list, failing_test_list, fix_location)
    elif CONF_TOOL_NAME == "genprog":
        genprog(setup_dir_path, deploy_path, bug_id, timeout, passing_test_list, failing_test_list, fix_location)
    else:
        exit("Unknown Tool Name")


def print_help():
    print("Usage: python driver.py [OPTIONS] --benchmark={manybugs} --tool={cpr/genprog/angelix/prophet/fix2fit} ")
    print("Options are:")
    print("\t" + ARG_DATA_PATH + "\t| " + "directory for experiments")
    print("\t" + ARG_TOOL_NAME + "\t| " + "name of the tool")
    print("\t" + ARG_BENCHMARK + "\t| " + "name of the benchmark")
    print("\t" + ARG_TOOL_PATH + "\t| " + "path of the tool")
    print("\t" + ARG_TOOL_PARAMS + "\t| " + "parameters for the tool")
    print("\t" + ARG_DEBUG_MODE + "\t| " + "enable debug mode")
    print("\t" + ARG_BUG_ID + "\t| " + "run only the specified experiment")
    print("\t" + ARG_BUG_ID_LIST + "\t| " + "runs a list of experiments")
    print("\t" + ARG_START_ID + "\t| " + "specify a range of experiments starting from ID")
    print("\t" + ARG_END_ID + "\t| " + "specify a range of experiments that ends at ID")
    print("\t" + ARG_CONFIG_ID + "\t| " + "specify a different configuration using config ID")
    exit()


def read_arg(argument_list):
    global CONF_DATA_PATH, CONF_TOOL_NAME, CONF_TOOL_PARAMS, CONF_START_ID, CONF_END_ID, CONF_CONFIG_ID
    global CONF_TOOL_PATH, CONF_DEBUG, CONF_SETUP_ONLY, CONF_BUG_ID, CONF_SKIP_LIST, CONF_BUG_ID_LIST, CONF_BENCHMARK
    global FILE_META_DATA
    print("[DRIVER] Reading configuration values")
    if len(argument_list) > 0:
        for arg in argument_list:
            if ARG_DATA_PATH in arg:
                CONF_DATA_PATH = str(arg).replace(ARG_DATA_PATH, "")
            elif ARG_TOOL_NAME in arg:
                CONF_TOOL_NAME = str(arg).replace(ARG_TOOL_NAME, "").lower()
            elif ARG_TOOL_PATH in arg:
                CONF_TOOL_PATH = str(arg).replace(ARG_TOOL_PATH, "")
            elif ARG_TOOL_PARAMS in arg:
                CONF_TOOL_PARAMS = str(arg).replace(ARG_TOOL_PARAMS, "")
            elif ARG_DEBUG_MODE in arg:
                CONF_DEBUG = True
            elif ARG_ONLY_SETUP in arg:
                CONF_SETUP_ONLY = True
            elif ARG_CONFIG_ID in arg:
                CONF_CONFIG_ID = str(arg).replace(ARG_CONFIG_ID, "")
            elif ARG_BUG_ID in arg:
                CONF_BUG_ID = int(str(arg).replace(ARG_BUG_ID, ""))
            elif ARG_START_ID in arg:
                CONF_START_ID = int(str(arg).replace(ARG_START_ID, ""))
            elif ARG_END_ID in arg:
                CONF_END_ID = int(str(arg).replace(ARG_END_ID, ""))
            elif ARG_BENCHMARK in arg:
                CONF_BENCHMARK = str(arg).replace(ARG_BENCHMARK, "")
            elif ARG_SKIP_LIST in arg:
                CONF_SKIP_LIST = str(arg).replace(ARG_SKIP_LIST, "").split(",")
            elif ARG_BUG_ID_LIST in arg:
                CONF_BUG_ID_LIST = str(arg).replace(ARG_BUG_ID_LIST, "").split(",")
            else:
                print("Unknown option: " + str(arg))
                print_help()
    if not CONF_SETUP_ONLY:
        if CONF_TOOL_NAME is None:
            print("[invalid] --tool-name is missing")
            print_help()
    if CONF_START_ID is None and CONF_BUG_ID is None and CONF_BUG_ID_LIST is None:
        print("[info] experiment id is not specified, running all experiments")
    if CONF_BENCHMARK is None:
        print("[invalid] --benchmark is missing")
        print_help()
    else:
        FILE_META_DATA = "benchmark/" + CONF_BENCHMARK + "/meta-data.json"


def run(arg_list):
    global EXPERIMENT_ITEMS, DIR_MAIN, CONF_DATA_PATH, CONF_TOOL_PARAMS, CONFIG_INFO
    global CONF_CONFIG_ID, CONF_BUG_ID_LIST, CONF_BENCHMARK, DIR_EXPERIMENT_RESULT
    print("[DRIVER] Running experiment driver")
    read_arg(arg_list)
    EXPERIMENT_ITEMS = load_experiment_details(FILE_META_DATA)
    CONFIG_INFO = load_configuration_details(FILE_CONFIGURATION, CONF_CONFIG_ID)
    create_directories()
    index = 1
    for experiment_item in EXPERIMENT_ITEMS:
        if CONF_BUG_ID and index != CONF_BUG_ID:
            index = index + 1
            continue
        if CONF_BUG_ID_LIST and str(index) not in CONF_BUG_ID_LIST:
            index = index + 1
            continue
        if CONF_SKIP_LIST and str(index) in CONF_SKIP_LIST:
            index = index + 1
            continue
        if CONF_START_ID and index < CONF_START_ID:
            index = index + 1
            continue
        if CONF_END_ID and index > CONF_END_ID:
            break

        experiment_name = "Experiment-" + str(index) + "\n-----------------------------"
        print(experiment_name)
        bug_name = str(experiment_item[KEY_BUG_ID])
        subject_name = str(experiment_item[KEY_SUBJECT])
        directory_name = CONF_BENCHMARK + "/" + subject_name + "/" + bug_name
        DIR_EXPERIMENT_RESULT = DIR_RESULT + "/" + "-".join([CONF_CONFIG_ID, CONF_BENCHMARK,
                                                                   CONF_TOOL_NAME, subject_name, bug_name])
        setup_dir_path = DIR_MAIN + "/benchmark/" + directory_name
        deploy_path = CONF_DATA_PATH + "/" + directory_name + "/"
        print("\t[META-DATA] benchmark: " + CONF_BENCHMARK)
        print("\t[META-DATA] project: " + subject_name)
        print("\t[META-DATA] bug ID: " + bug_name)
        print("\t[INFO] setup directory: " + deploy_path)
        clean_results(DIR_EXPERIMENT_RESULT)
        if os.path.isdir(deploy_path):
            print("\t[INFO] deployment path exists, skipping setup")
        else:
            setup_experiment(setup_dir_path, bug_name)
        if not CONF_SETUP_ONLY:
            repair(deploy_path, setup_dir_path, experiment_item)
        archive_results(DIR_EXPERIMENT_RESULT)
        index = index + 1


if __name__ == "__main__":
    import sys
    try:
        run(sys.argv[1:])
    except KeyboardInterrupt as e:
        print("[DRIVER] Program Interrupted by User")
        exit()
