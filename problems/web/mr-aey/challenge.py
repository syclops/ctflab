from hacksport.problem import (
    Challenge,
    File,
)

class Problem(Challenge):
    files = [File("curling.pcap", 0o644)]

    def generate_flag(self, _):
        return "dQw4w9WgXcQ"

    def setup(self):
        pass
