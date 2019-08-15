import os
import csv
import copy
from pathlib import Path


def load_command():
    """
    load command informations from file.
    :returns:
        - original_commans: dict, command name : Command
        - command_group: dict, group_name: command_names
    """
    outter = os.path.dirname(os.path.abspath(__file__))
    syntax_path = Path(outter) / ".." / "command_syntax.csv"

    group = {}
    first_line = True
    with open(syntax_path) as command_syntax:
        csvreader = csv.reader(command_syntax)
        for line in csvreader:
            if first_line:
                first_line = False
                continue
            syntax, command, syntax = line
            group.setdefault(syntax, []).append(command)

    group2commands = copy.deepcopy(group)

    # add lowercase commands
    group2command_res = {}
    for syntax in group.keys():
        commands = group[syntax]
        lower_commands = [command.lower() for command in commands]
        commands += lower_commands
        # Space in command cam be mutiple spaces
        re_commands = [command.replace(" ", "\s+") for command in commands]
        group2command_res[syntax] = "|".join(re_commands)

    return group2commands, group2command_res


group2commands, group2command_res = load_command()