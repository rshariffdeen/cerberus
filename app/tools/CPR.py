import os
import shutil

from app.tools import AbstractTool
from app.utilities import execute_command, error_exit
from app import definitions, values, emitter


class CPR(AbstractTool):
    def __init__(self):
        self.name = os.path.basename(__file__).lower()

    def repair(self, dir_logs, dir_expr, dir_setup, bug_id, timeout, passing_test_list,
               failing_test_list, fix_location, subject_name, binary_path, additional_tool_param, binary_input_arg):
        emitter.normal("\t\t\t running repair with " + self.name)
        self.log_output_path = dir_logs + "/" + self.name.lower() + "-" + bug_id + "-output.log"
        conf_path = dir_expr + "/cpr/repair.conf"
        timeout_m = str(timeout * 60)
        test_id_list = ""
        for test_id in failing_test_list:
            test_id_list += test_id + ","
        seed_id_list = ""
        if passing_test_list:
            for test_id in passing_test_list:
                seed_id_list += test_id + ","
        timestamp_command = "echo $(date) > " + self.log_output_path
        execute_command(timestamp_command)
        cpr_command = "timeout -k 5m {0}h cpr --conf=".format(timeout) + conf_path + " "
        cpr_command += " --seed-id-list=" + seed_id_list + " "
        cpr_command += " --test-id-list=" + test_id_list + " "
        cpr_command += "{0} --time-duration={1} >> {2} 2>&1 ".format(additional_tool_param, str(timeout_m),
                                                                     self.log_output_path)
        execute_command(cpr_command)
        timestamp_command = "echo $(date) >> " + self.log_output_path
        execute_command(timestamp_command)
        return

    def save_logs(self, dir_results, dir_setup, bug_id):
        super(CPR, self).save_logs(dir_results)
        dir_logs = "/CPR/logs/" + bug_id
        shutil.copy2(dir_logs, dir_results)

    def save_artefacts(self, dir_results, dir_expr, dir_setup, bug_id):
        self.save_logs(dir_results)
        dir_patches = "/CPR/output/" + bug_id
        if os.path.isdir(dir_patches):
            shutil.copy2(dir_patches, dir_results + "/patches")
        shutil.copy(dir_setup + "/cpr/instrument.sh", dir_results)
        return

    def post_process(self, dir_expr, dir_results):
        emitter.normal("\t\t\t post-processing for {}".format(self.name))
        super(CPR, self).post_process(dir_expr)
        clean_command = "rm -rf " + dir_results + "/output/klee-out-*"
        execute_command(clean_command)

