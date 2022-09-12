import inquirer
import json
from os import system
from glob import glob
import requests
import git

install_path = "/usr/local/lib/kepm/"

print("Welcome to Kapsulon's Epitech Project Manager")
print("This program will help you to create a new project or edit an existing one\n")

def ask_for_choice(question="", answers=[]):
    questions = [
        inquirer.List("action",
                      message=question,
                      choices=answers,
                      ),
    ]
    result = inquirer.prompt(questions)
    system("clear")
    return result["action"]

def ask_for_text(question=""):
    questions = [
        inquirer.Text("text",
                      message=question,
                      ),
    ]
    result = inquirer.prompt(questions)
    system("clear")
    return result["text"]

def get_project_name(path="."):
    if not is_project(path):
        return False
    return json.loads(open(".kepm.json", "r").read())["project_name"]

def is_project(path="."):
    if not glob(path + "/.kepm.json"):
        return False
    return True

def create_project():
    action = ask_for_choice("What do you want to do?", ["Initialize a new project", "Create KEPM project file"])
    if action == "Initialize a new project":
        print("Initializing a new project")
        init_project()
    elif action == "Create KEPM project file":
        print("Creating KEPM project file")
        create_kepm_file()

def init_project():
    pass

def create_kepm_file():
    project = {
        "project_name": ask_for_text("Project name")
    }
    open(".kepm.json", "w").write(json.dumps(project))

def edit_project():
    system("clear")
    if not is_project():
        print("Project file not found")
        return
    print("Project file found.")
    print("Project name: " + get_project_name())
    choice = ask_for_choice("What do you want to do?", ["Edit project name", "Check norm errors", "Quit"])
    if choice == "Edit project name":
        create_kepm_file()
    elif choice == "Check norm errors":
        check_norm()
    elif choice == "Quit":
        exit(0)

def check_norm():
    system("python " + install_path + "Bubulle-Norminette/bubulle-py/bubulle.py -p .")

def check_bubulle() -> bool:
    if not glob(install_path + "Bubulle-Norminette/VERSION"):
        print("Bubulle not found, do you want to install it ?")
        ask = inquirer.prompt([inquirer.Confirm("install", message="Install bubulle ?")])
        if ask["install"]:
            git.Git(install_path).clone("https://github.com/aureliancnx/Bubulle-Norminette.git")
            print("Bubulle installed")
            with open(install_path + "error_catcher_patch", "r") as patch:
                f = open(install_path + "Bubulle-Norminette/bubulle-py/utils/error_handling.py", "w")
                content = patch.read()
                f.write(content)
                f.close()
                patch.close()
            print("Bubulle patched")
            return True
        else:
            print("Bubulle not installed.")
            return False
    else:
        version = open(install_path + "Bubulle-Norminette/VERSION", "r").read()
        latest = requests.get("https://raw.githubusercontent.com/aureliancnx/Bubulle-Norminette/master/VERSION")
        if version != latest.text:
            print("Bubulle is outdated. Do you want to update it ?")
            ask = inquirer.prompt([inquirer.Confirm("update", message="Update bubulle ?")])
            if ask["update"]:
                g = git.cmd.Git(install_path + "Bubulle-Norminette")
                g.pull()
                print("Bubulle updated")
                with open(install_path + "error_catcher_patch", "r") as patch:
                    f = open(install_path + "Bubulle-Norminette/bubulle-py/utils/error_handling.py", "w")
                    content = patch.read()
                    f.write(content)
                    f.close()
                    patch.close()
                print("Bubulle patched")
                return True
            else:
                print("Bubulle not updated.")
                return False
        else:
            return True

def check_version():
    with open(install_path + "VERSION", "r") as f:
        version = f.read()
        f.close()
    latest = requests.get("https://raw.githubusercontent.com/Kapsulon/kepm/main/VERSION")
    if version != latest.text:
        print("You are not using the latest version of KEPM. Do you want to update it ?")
        ask = inquirer.prompt([inquirer.Confirm("update", message="Update KEPM ?")])
        if ask["update"]:
            g = git.cmd.Git(install_path)
            g.pull()
            print("KEPM updated")
        else:
            print("KEPM not updated.")

def main():
    check_version()
    check_bubulle()
    action = ask_for_choice("What do you want to do?", ["Create a new project", "Edit an existing project", "Quit"])
    if action == "Create a new project":
        print("Creating a new project")
        create_project()
    elif action == "Edit an existing project":
        print("Editing an existing project")
        edit_project()
    elif action == "Quit":
        exit(0)

if __name__ == '__main__':
    while True:
        main()
