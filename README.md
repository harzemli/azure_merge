"# slot_race_track" 
## Cloning 
Clone this repository locally with git using the following command in a (Git Bash) terminal:

git clone https://gitlab.sogeticloudservices.com/sogetilabs/slotracer.git

If access denied then you need to create personal access token: 

After Login to Gitlab click on Profile>>edit profile>>Access Tokens 
Give any token-name you want
Select expiration date atleast one month from current day (recommended)
Select the scope (select all)
Click on 'Create personal access token'. Your personal acess token is ready to use.
With Personal access token:
git clone https://<username>:<token>@gitlab.sogeticloudservices.com/sogetilabs/slotracer.git
 

The above process was to clone main branch. if you want to clone any other branch

git clone --branch <branch name>  https://<token-name>:<token>@gitlab.sogeticloudservices.com/sogetilabs/slotracer.git

You can also clone the main branch, and then checkout another branch using the following command:

git checkout <branch name>

To confirm your current branch and compare it with the main branch, you can use the command

git status

The code for the digital twin (in Godot) is available on this Github.

The code for the virtual simulation of the racetrack is also available on this Github, and is named track_logic.py

To allow communication between track_logic.py and Godot make sure to:
1. Open track_logic.py
2. Open the Godot project in Godot (2D navigation demo)
3. Run the python file (track_logic.py)
4. Start the Godot game


# Pipenv
To make it easier to install all the required packages for the slot race track project, a pipenv
environment has been made. See below on how to make sure you install the virtual environment
properly.

## requirements
- Pip installed (should be included in the Python installation)
- Pipenv package is installed: `pip install pipenv`

## Installing the virtual environment
To install the pipenv environment, the following command needs to be executed in a command line:
- `pipenv install`

To access the virtual environment and see the installed packages, the following command is used:
- `pipenv shell`

To see which packages are installed, the following command is used:
- `pip list`

After executing the `pipenv shell` command, the python files can now be executed within the virtual
environment. Simply run them like you normally would run a python file. for example:
- `python track_logic.py`

## IDE interpreter
When using an IDE to run your Python files, make sure you change the interpreter to the
virtual environment. When using a different IDE as described below, please add the steps on how to
do this.

### VS Code
Assuming the Python extension has already been installed:
1. Press `f1` key
1. Type `Python: Select Interpreter` and select the option
1. Select the SlotRacer virtual environment in the list
1. When running code, Select `Run Python File in Terminal` (you may need to reload the VS code
   window first)
