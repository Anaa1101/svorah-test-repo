"""Person entity. Every field here is personal data of a data principal.
Defined in-repo so Joern can resolve the flows that read from it (cross-file)."""


class User:
    def __init__(self):
        self.aadhaar = ""        # severe tier  -> CRITICAL
        self.pan = ""            # elevated tier -> HIGH
        self.password = ""       # severe tier  -> CRITICAL
        self.email = ""          # standard tier -> MEDIUM
        self.phone = ""          # standard tier -> MEDIUM
        self.name = ""           # standard tier -> MEDIUM (person-noun)
        self.address = ""
        self.income = 0          # elevated tier -> HIGH
        self.gender = ""
        # naming variants (camelCase / snake / suffix) — same PII, must still match
        self.aadhaarNumber = ""  # CRITICAL
        self.emailAddress = ""   # MEDIUM
        self.user_phone = ""     # MEDIUM
        # Indian-ID moat
        self.upi = ""            # upi_id  -> HIGH
        self.ifsc = ""           # public bank-branch code (not an account number) -> MEDIUM
        self.voterId = ""        # voter_id -> HIGH
        self.token = ""          # auth_token -> HIGH


def load_user() -> "User":
    return User()
