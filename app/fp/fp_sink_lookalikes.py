"""FP-SINKLOOKALIKE | 'log' substrings, non-DB SQL look-alikes, and bare .write are not sinks."""
from app.lib.noise import backlog, catalog, dialog, doc, pdf, res, stream
from app.models.user import User


def log_substring_traps(user: User):
    catalog.save()             # 'log' substring; not a log sink
    dialog.show(user.email)    # 'log' substring; not a log sink
    backlog.add(user.email)    # 'log' substring; not a log sink


def sql_lookalikes(user: User):
    doc.text(user.email)       # not a DB execute
    res.raw(user.email)        # not a DB execute
    pdf.render(user.email)     # not a DB execute


def bare_write(user: User):
    response = res
    response.write(user.pan)   # bare .write excluded
    stream.write(user.pan)     # bare .write excluded
