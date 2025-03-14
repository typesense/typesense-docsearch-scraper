import sys
from os import getcwd, path, environ
from dotenv import load_dotenv
from builtins import input

env_file = getcwd() + "/.env"
load_dotenv(env_file)

from .helpers import get_color
from .helpers import printer
from .helpers import print_error
from .helpers import print_command_help

from .commands.bootstrap_config import BootstrapConfig
from .commands.playground_config import PlaygroundConfig
from .commands.build_docker_scraper import BuildDockerScraper
from .commands.run_tests import RunTests
from .commands.run_config import RunConfig
from .commands.deploy_docker_scraper_images import DeployDockerScraperImages
from .commands.deploy_config import DeployConfig
from .commands.run_config_docker import RunConfigDocker

if not path.isfile(env_file):
    print("")
    print("No .env found. Let's create one.")

    f = open(env_file, "w")

    ans = input("What is your TYPESENSE_API_KEY: ")
    f.write("TYPESENSE_API_KEY=" + ans + "\n")

    ans = input("What is your TYPESENSE_HOST: ")
    f.write("TYPESENSE_HOST=" + ans + "\n")

    ans = input("What is your TYPESENSE_PORT: ")
    f.write("TYPESENSE_PORT=" + ans + "\n")

    ans = input("What is your TYPESENSE_PROTOCOL (http|https): ")
    f.write("TYPESENSE_PROTOCOL=" + ans + "\n")

    f.close()

    print("")

load_dotenv(env_file)

REQUIRED_CONFIGS = True

if "TYPESENSE_API_KEY" not in environ or len(environ["TYPESENSE_API_KEY"]) == 0:
    REQUIRED_CONFIGS = False

cmds = []

cmds.append(BootstrapConfig())
cmds.append(BuildDockerScraper())
cmds.append(RunTests())
cmds.append(PlaygroundConfig())

cmds.append(RunConfig())
cmds.append(RunConfigDocker())
cmds.append(DeployConfig())
cmds.append(DeployDockerScraperImages())

def print_usage(no_ansi=False):
    printer("Docsearch CLI", 1, no_ansi)
    printer("", 4, no_ansi)
    printer("Usage:", 2, no_ansi)
    printer("  ./docsearch command [options] [arguments]", 4, no_ansi)
    printer("", 4, no_ansi)
    printer("Options:", 2, no_ansi)

    if no_ansi:
        printer("  " + "--help" + (" " * 4) + "Display help message", 4,
                no_ansi)
    else:
        printer("  " + get_color(1) + "--help" + get_color() + (
            " " * 4) + "Display help message", 4)

    printer("", 4, no_ansi)

    groups = {}

    longest_cmd_name = 0

    for cmd in cmds:
        longest_cmd_name = max(longest_cmd_name, len(cmd.get_name()))
        group = ""

        if ":" in cmd.get_name():
            group = cmd.get_name().split(":")[0]

        if group not in groups:
            groups[group] = []

        groups[group].append(cmd)

    printer("Available commands:", 2, no_ansi)

    for key in sorted(groups.keys()):
        if key != "":
            printer(" " + key, 2, no_ansi)
        for cmd in groups[key]:
            nb_spaces = longest_cmd_name + 2 - len(cmd.get_name())
            if no_ansi:
                printer("  " + cmd.get_name() + (
                    " " * nb_spaces) + cmd.get_description(), 4, no_ansi)
            else:
                printer("  " + get_color(1) + cmd.get_name() + get_color() + (
                    " " * nb_spaces) + cmd.get_description(),
                        no_ansi)


def find_command(name, cmds):
    for cmd in cmds:
        if cmd.get_name().find(name) == 0:
            return cmd

    return None


def run():
    help_needed = "--help" in sys.argv

    if help_needed:
        del sys.argv[sys.argv.index("--help")]

    no_ansi = "--no-ansi" in sys.argv

    if no_ansi:
        del sys.argv[sys.argv.index("--no-ansi")]

    if len(sys.argv) == 1:
        print_usage(no_ansi)
    else:
        command = find_command(sys.argv[1], cmds)

        if command is not None:
            if help_needed:
                print_command_help(command)
            else:
                if len(sys.argv[2:]) < command.nb_options():
                    printer("")
                    print_error("Missing at least one argument")
                    printer("")
                    print_command_help(command)
                else:
                    exit(command.run(sys.argv[2:]))
        else:
            print_error("Command \"" + sys.argv[1] + "\" not found")

    exit(1)
