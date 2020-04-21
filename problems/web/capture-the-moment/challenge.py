from hacksport.problem import (
    Challenge,
    File,
)

class Problem(Challenge):
    files = [File("image.pcap", 0o644)]

    def generate_flag(self, _):
        return "a_thousand_words"

    def setup(self):
        pass
