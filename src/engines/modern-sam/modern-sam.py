import subprocess
import re
ConfigStructure = {
    "voice": {
        "speed": {"type": "int", "min": 1, "max": 255, "default": 72},
        "pitch": {"type": "int", "min": 0, "max": 255, "default": 64},
        "mouth": {"type": "int", "min": 0, "max": 255, "default": 128},
        "throat": {"type": "int", "min": 0, "max": 255, "default": 128}
    },
    "pronunciation": {
        "phonetic": {"type": "bool", "default": False},
        "sing": {"type": "bool", "default": False},
        "moderncmu": {"type": "bool", "default": False}
    },
    "engine": {
        "path_to_executable": {"type": "string", "default": ""}
    }
}

class SapphoneEngine:
    def __init__(self, config):
        self.config = config

    def build_command_args(self):
        voice = self.config["voice"]
        args = [self.config["engine"]["path_to_executable"]]
        args += ["--speed", str(voice["speed"]),
                "--pitch", str(voice["pitch"]),
                "--mouth", str(voice["mouth"]),
                "--throat", str(voice["throat"])]
        if self.config["pronunciation"]["phonetic"] is True:
            args.append("--phonetic")
        if self.config["pronunciation"]["sing"] is True:
            args.append("--singmode")
        if self.config["pronunciation"]["moderncmu"] is True:
            args.append("--moderncmu")
        return args


    def speak_to_file(self, script, output):
        # ensure script string does not add arguments to the command
        script = re.sub(r"^-+", "", script)
        command = self.build_command_args()
        command += ["--wav", output]
        command.append(script)

        subprocess.run(command, shell=False, check=True)

