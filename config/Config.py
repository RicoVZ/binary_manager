import ConfigParser
import os.path

class Config:
    binaries_full_dir = ""
    binaries_dir      = "downloadables"
    samples_dir       = "buildables"
    listen_ip         = "127.0.0.1"
    listen_port       = 42424
    max_upload_size   = 16 * 1024 * 1024
    
    def __init__(self):
        
        self.config_file = "config.cfg"
        self.config      = ConfigParser.RawConfigParser()
        
        if not os.path.isfile(self.config_file):
            self._create_default()

        self._read_config()

        #Get current directory, so we can set the correct upload directory for
        #Flask to use.
        Config.binaries_full_dir = str(os.getcwd()) + "//" + Config.binaries_dir

    def _create_default(self):
        
        self.config.add_section("server")
        self.config.set("server", "listen_ip", "127.0.0.1")
        self.config.set("server", "listen_port", "42424")
        self.config.set("server", "max_upload_size_mb", "16")
        
        print("Creating default config")
        with open(self.config_file, "wb") as fp:
            self.config.write(fp)

    def _read_config(self):
        
        self.config.read(self.config_file)
        
        Config.listen_ip   = self.config.get("server", "listen_ip")
        Config.listen_port = self.config.getint("server", "listen_port")
        Config.max_upload_size = self.config.getint("server", "max_upload_size_mb") * 1024 * 1024
