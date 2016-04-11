"""Settigns discovery assignation."""
from os import environ as env
import re

# Identifier used to recognize auto-generated comments
HIDDEN = "<KGB>"
STATUS_CONTEXT = "Комитет Git'a безопасности"

MAX_STATUS_LENGTH = env.get("MAX_STATUS_LENGTH") or 50
MAX_LINE_LENGTH = env.get("MAX_LINE_LENGTH") or 72

_DEFAULT_TYPES = "revert,feat,perf,fix,docs,refactor,test"
_TYPES = (env.get("AUTHORIZED_TYPES") or _DEFAULT_TYPES).split(",")

STATUS_R = re.compile("(" + "|".join(_TYPES) + ")" +
                      "\(" + "[^)\s]+" + "\):" + ".*")

GH_TOKEN = env.get("GH_TOKEN")