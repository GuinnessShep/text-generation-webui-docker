# merge_dockerfiles.py

import os
import json
import requests

def download_dockerfile(url, filename):
    response = requests.get(url)
    with open(filename, 'w') as file:
        file.write(response.text)

def read_dockerfile(filename):
    with open(filename, 'r') as file:
        return file.readlines()

def write_dockerfile(filename, lines):
    with open(filename, 'w') as file:
        file.writelines(lines)

def extract_commands(lines, commands_order):
    extracted_commands = {command: [] for command in commands_order}
    for line in lines:
        for command in commands_order:
            if line.startswith(command):
                extracted_commands[command].append(line)
                break
    return extracted_commands

def merge_commands(base_commands, additional_commands, commands_order):
    for command in commands_order:
        base_commands[command] += additional_commands.get(command, [])
    return base_commands

def merge_dockerfiles(dockerfiles):
    base_file = read_dockerfile('Dockerfile')
    base_commands = extract_commands(base_file, dockerfiles[0]['commands_order'])

    for dockerfile in dockerfiles[1:]:
        download_dockerfile(dockerfile['url'], 'DockerfileTemp')
        lines = read_dockerfile('DockerfileTemp')
        additional_commands = extract_commands(lines, dockerfile['commands_order'])
        base_commands = merge_commands(base_commands, additional_commands, dockerfile['commands_order'])

    merged_lines = [command for sublist in base_commands.values() for command in sublist]
    write_dockerfile('DockerfileMerged', merged_lines)

# Usage:
dockerfiles_info = json.loads(os.getenv('DOCKERFILES_INFO', '[]'))
merge_dockerfiles(dockerfiles_info)
