import behave

import features.support.helpers as helpers
import features.support.config_helper as config_helper


behave.use_step_matcher("re")

def before_all(context):
    context.config.logging_level="ERROR"
    context.config.setup_logging()

def before_scenario(context, scenario):
    context.app_path = "./main.py"
    context.app_process = None
    context.poll_rate = 10
    context.fake_ci_servers = []
    helpers.rebuild_config_file(context)

def after_scenario(context, scenario):
    helpers.kill_ci_screen(context)
    config_helper.restore_config_file()
    for ci_server in context.fake_ci_servers:
        ci_server.stop()
