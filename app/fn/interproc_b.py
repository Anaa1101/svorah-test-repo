"""FN-INTERPROC (file 2/3) | pure pass-through helper. Must NOT stop the taint."""
from app.fn.interproc_c import emit


def forward(value):
    emit(value)
