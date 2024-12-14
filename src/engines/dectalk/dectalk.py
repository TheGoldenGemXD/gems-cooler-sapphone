import subprocess
import sys

ConfigStructure = {
    "advanced": {
        "prefix": {"type": "string", "default": ""},
        "suffix": {"type": "string", "default": ""}
    },
    "engine": {
        "path_to_executable": {"type": "string", "default": ""}
    }
}


class SapphoneEngine:
    def __init__(self, config):
        self.config = config

    def dectalk_windows(self, script, output):
        args = []
        args += [self.config["engine"]["path_to_executable"]]
        if self.config["advanced"]["prefix"] != "":
            args += ["-pre", self.config["advanced"]["prefix"]]
        if self.config["advanced"]["suffix"] != "":
            args += ["-post", self.config["advanced"]["suffix"]]
        args += ["-w", output]
        #args.append(script)
        subprocess.run(args, shell=False, check=True, input=script, text=True)
    def dectalk_linux(self, script, output):
        args = []
        args += [self.config["engine"]["path_to_executable"]]
        if self.config["advanced"]["prefix"] != "":
            args += ["-pre", self.config["advanced"]["prefix"]]
        if self.config["advanced"]["suffix"] != "":
            args += ["-post", self.config["advanced"]["suffix"]]
        args += ["-fo", output]
        args += ["-a", script]
        subprocess.run(args, shell=False, check=True)

    def speak_to_file(self, script, output):
        if sys.platform in ["win32", "cygwin"]:
            return self.dectalk_windows(script, output)
        elif sys.platform in ["linux", "darwin"]:
            return self.dectalk_linux(script, output)


