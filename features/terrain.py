import copy
import os
import subprocess
import sys

from lettuce import *
import pqaut.client as pqaut

import features.support.fake_ci_server as ci
import features.support.config_helper as config_helper


world.app_path = "./main.py"
world.app_process = None

@world.absorb
def kill_ci_screen():
    if world.app_process:
        subprocess.Popen.kill(world.app_process)

@world.absorb
def launch_ci_screen():
    if os.getenv("DEBUG"):
        world.app_process = subprocess.Popen([world.app_path, "--automation_server"])
    else:
        world.app_process = subprocess.Popen([world.app_path, "--automation_server"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    pqaut.wait_for_automation_server()

@before.all
def before_all():
    world.fake_ci_server = ci.FakeCIServer(port=1234)
    world.fake_ci_server.start()

@after.all
def after_all(obj):
    world.fake_ci_server.stop()

@before.each_scenario
def before_each(obj):
    kill_ci_screen()

@after.each_scenario
def after_each(obj):
    kill_ci_screen()
    config_helper.restore_config_file()
    world.fake_ci_server.projects = []