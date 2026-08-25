"""Non-person objects and look-alike sinks used by the FP-resistance corpus.
None of these should ever produce a finding. Defined in-repo for resolvability."""


class Config:            # non-person; `ipAddress` has an `ip` qualifier
    def __init__(self):
        self.ipAddress = "0.0.0.0"


class Table:             # non-person receiver for the `.name` gate
    def __init__(self):
        self.name = ""


class Challenge:         # non-person receiver for the `.name` gate
    def __init__(self):
        self.name = ""


class Dobson:            # `.value` on a receiver whose name merely contains "dob"
    def __init__(self):
        self.value = ""


class Catalog:           # substring "log" trap, and a non-DB `.save`
    def save(self):
        pass


class Dialog:            # substring "log" trap
    def show(self, x=None):
        pass


class Backlog:           # substring "log" trap
    def add(self, x=None):
        pass


class Doc:               # SQL look-alike on a non-DB receiver
    def text(self, x=None):
        pass


class Res:               # response object: .raw / .render / .write are not sinks here
    def raw(self, x=None):
        pass

    def render(self, payload=None):
        pass

    def write(self, x=None):
        pass


class Pdf:
    def render(self, x=None):
        pass


class Stream:
    def write(self, x=None):
        pass


class ApiClient:         # unknown vendor: fires as HTTP but residency must NOT be guessed
    def post(self, url, json=None):
        pass


def expand(x):           # token "pan" appears inside the word — must not match
    return x


config = Config()
table = Table()
challenge = Challenge()
dobson = Dobson()
catalog = Catalog()
dialog = Dialog()
backlog = Backlog()
doc = Doc()
res = Res()
pdf = Pdf()
stream = Stream()
api_client = ApiClient()

# field-name-not-value traps
email_regex = r".*@.*"
email_template_id = "tpl_42"
nameField = "name"
