import re
import time
from enum import Enum

import subprocess

active_projects_config_filename = ''
active_projects_config_data_delimiter = '::'


class Git:
    IS_VALID_DIRECTORY = 'git rev-parse --is-inside-work-tree'
    HAS_COMMITS = 'git rev-list --count origin/main..@'
    REMOTE_BRANCHES = 'git branch -r'

    ADD_ALL = 'git add .'
    RESTORE_STAGED = 'git restore --staged .'
    REBASE = 'git pull --rebase'
    COMMIT = 'git commit -m'
    SOFT_RESET_1 = 'git reset --soft HEAD~1'
    PUSH = 'git push origin'
    DELETE_REMOTE = 'git push origin -d'

    SAVE_STASH = 'git stash push -m'
    APPLY_STASH = 'git stash apply'
    DROP_STASH = 'git stash drop'

    STASH_SAVE_NO_OP_MESSAGE = 'No local changes to save'

    PREFIX_MESSAGE = 'GitHelper_'
    STAGED_MESSAGE = PREFIX_MESSAGE + 'staged_changes'
    UNSTAGED_MESSAGE = PREFIX_MESSAGE + 'unstaged_changes'

    PREFIX_HEAD = 'HEAD'
    BRANCH_NAME = 'backup_branch'


class ProjectType(Enum):
    # The directory is the git package and is private (no collaboration; can be rebased which is obviously superior)
    DEFAULT = 'default'
    # The directory is work related java workspace
    JAVA_WORKSPACE = 'javaWorkspace'


def get_active_project_details():
    # TODO use 'with' thingy
    active_project_file = open(active_projects_config_filename, 'r')
    active_project_paths = []
    active_project_types = []

    for active_project_detail in active_project_file:
        active_project_data = active_project_detail.split(active_projects_config_data_delimiter)
        if len(active_project_data) == 2:
            active_project_paths.append(active_project_data[0])
            active_project_types.append(active_project_data[1])

    return active_project_types, active_project_paths


def handle_active_projects(function):
    active_project_details = zip(*get_active_project_details())
    for active_project_type, active_project_path in active_project_details:
        successful, _ = run_command(Git.IS_VALID_DIRECTORY)
        if successful:
            if active_project_type.lower() == ProjectType.DEFAULT.value:
                successful, _ = run_command('cd', active_project_path)
                if successful:
                    function()


def rebase_project():
    staged_changes_present = stash(Git.STAGED_MESSAGE)

    run_command(Git.ADD_ALL)
    unstaged_changes_present = stash(Git.UNSTAGED_MESSAGE)

    commits_present = has_commits()
    successful, _ = run_command(Git.REBASE)
    if not commits_present or successful:
        if unstaged_changes_present:
            successful, _ = run_command(Git.APPLY_STASH)
            if successful:
                run_command(Git.RESTORE_STAGED)
                run_command(Git.DROP_STASH)
            else:
                return

        if staged_changes_present:
            run_command(Git.APPLY_STASH)
            run_command(Git.DROP_STASH)


def rebase_projects():
    handle_active_projects(rebase_project)


def push_local_work():
    timestamp = str(int(time.time()))

    commits_present = has_commits()

    staged_changes_present = run_command(Git.COMMIT, Git.STAGED_MESSAGE)

    run_command(Git.ADD_ALL)
    unstaged_changes_present = run_command(Git.COMMIT, Git.UNSTAGED_MESSAGE)

    pushed_changes = False
    if commits_present or staged_changes_present or unstaged_changes_present:
        pushed_changes = run_command(Git.PUSH,
                                     Git.PREFIX_HEAD + ':' + Git.PREFIX_MESSAGE + Git.BRANCH_NAME + '_' + timestamp)

    if unstaged_changes_present:
        run_command(Git.SOFT_RESET_1)
        run_command(Git.RESTORE_STAGED)

    if staged_changes_present:
        run_command(Git.SOFT_RESET_1)

    # TODO This will keep moving the remote commit even if it is not needed instead of being efficient
    if pushed_changes:
        cleanup_remote_branches(timestamp)


def push_local_works():
    handle_active_projects(push_local_work)


def cleanup_remote_branches(timestamp='0', delete_all=False):
    if not delete_all:
        if timestamp == '0':
            return

    successful, output = run_command(Git.REMOTE_BRANCHES)
    if successful:
        for remote_branch_name in output:
            remote_branch_name = remote_branch_name.strip()
            if 'origin/main' != remote_branch_name:
                pattern = re.compile(r'^origin/(GitHelper_backup_branch_(\d+))$')
                match = pattern.match(remote_branch_name)
                if match:
                    remote_branch_timestamp = int(match.group(2))
                    latest_timestamp = int(timestamp)
                    if delete_all or remote_branch_timestamp < latest_timestamp:
                        run_command(Git.DELETE_REMOTE, match.group(1))


def wrapup_remote_branches():
    cleanup_remote_branches(delete_all=True)


def stash(message):
    _, output = run_command(Git.SAVE_STASH, message)
    return Git.STASH_SAVE_NO_OP_MESSAGE not in output


def has_commits():
    successful, output = run_command(Git.HAS_COMMITS)
    if not successful:
        raise Exception('Could not successfully run command to figure out if local repository has commits')
    return int(output[0]) > 0


def run_command(command, args=None):
    if args is None:
        args = []
    process = subprocess.run([*command.split(), *args], capture_output=True, text=True)
    return process.returncode == 0, process.stdout.splitlines()


if __name__ == "__main__":
    cleanup_remote_branches('1676224409')
