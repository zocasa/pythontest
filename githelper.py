import re
import time
from enum import StrEnum

import subprocess

active_projects_config_filename = ''


class ProjectType(StrEnum):
    # The directory is the git package and is private (no collaboration; can be rebased which is obviously superior)
    DEFAULT = 'default'
    # The directory is work related java workspace
    JAVA_WORKSPACE = 'javaWorkspace'


def get_active_project_details():
    # use with thingy
    active_project_file = open(active_projects_config_filename, 'r')
    active_project_paths = []
    active_project_types = []

    for active_project_detail in active_project_file:
        active_project_data = active_project_detail.split('::')
        if len(active_project_data) == 2:
            active_project_paths.append(active_project_data[0])
            active_project_types.append(active_project_data[1])

    return active_project_types, active_project_paths
    # return ['default'], ['']


def handle_active_projects(function):
    active_project_details = zip(*get_active_project_details())
    for active_project_type, active_project_path in active_project_details:
        process = subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'])
        if process.returncode == 0:
            if active_project_type.lower() == ProjectType.DEFAULT:
                process = subprocess.run(['cd', active_project_path])
                if process.returncode == 0:
                    function()


def rebase_project():
    subprocess.run(['git', 'stash', 'push', '-m', '[logOffAutoStasher] staged changes'])
    subprocess.run('git add .')
    subprocess.run(['git', 'stash', 'push', '-m', '[logOffAutoStasher] unstaged changes'])
    process = subprocess.run(['git', 'pull', '--rebase'])
    if process.returncode == 0:
        process = subprocess.run(['git', 'stash', 'apply'])
        if process.returncode == 0:
            subprocess.run(['git', 'restore', '--staged', '.'])
            subprocess.run(['git', 'stash', 'drop'])
            process = subprocess.run(['git', 'stash', 'apply'])
            if process.returncode == 0:
                subprocess.run(['git', 'stash', 'drop'])


def rebase_projects():
    handle_active_projects(rebase_project)


def push_local_work():
    timestamp = str(int(time.time()))
    process1 = subprocess.run(['git', 'push', 'origin', 'HEAD:logOffAutoPusher_committedChanges_', timestamp])
    subprocess.run(['git', 'commit', '-m', '[logOffAutoPusher] staged changes'])
    process2 = subprocess.run(['git', 'push', 'origin', 'HEAD:logOffAutoPusher_stagedChanges_', timestamp])
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', '[logOffAutoPusher] unstaged changes'])
    process3 = subprocess.run(['git', 'push', 'origin', 'HEAD:logOffAutoPusher_unstagedChanges_', timestamp])
    if process3.returncode == 0:
        subprocess.run(['git', 'reset', '--soft', 'HEAD~1'])
        subprocess.run(['git', 'restore', '--staged', '.'])
        if process2.returncode == 0:
            subprocess.run(['git', 'reset', '--soft', 'HEAD~1'])

    if process1.returncode == 0 and process2.returncode == 0 and process3.returncode == 0:
        cleanup_remote(timestamp)


def push_local_works():
    handle_active_projects(push_local_work)


def cleanup_remote(timestamp):
    process = subprocess.run(['git', 'branch', '-r'], capture_output=True, text=True)
    if process.returncode == 0:
        output = process.stdout.splitlines()
        for remote_branch_name in output:
            if 'origin/main' not in remote_branch_name:
                pattern = re.compile(r'^\s+origin/(logOffAutoPusher_(committed|staged|unstaged)Changes_(\d+))$')
                match = pattern.match(remote_branch_name)
                if match:
                    remote_branch_timestamp = int(match.group(3))
                    latest_timestamp = int(timestamp)
                    if remote_branch_timestamp < latest_timestamp:
                        subprocess.run(['git', 'push', 'origin', '-d', match.group(1)])


if __name__ == "__main__":
    cleanup_remote('1676224409')
