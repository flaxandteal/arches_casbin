import os
from django.conf import settings

settings.CASBIN_MODEL = getattr(settings, "CASBIN_MODEL", os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'permissions', 'casbin.conf'))
settings.CASBIN_RELOAD_QUEUE = getattr(settings, "CASBIN_RELOAD_QUEUE", os.getenv("CASBIN_RELOAD_QUEUE", "reloadQueue"))
settings.USER_SIGNUP_GROUP = getattr(settings, "USER_SIGNUP_GROUP", "Crowdsource Editor")
settings.ALLOWED_SIGNUP_GROUPS = getattr(settings, "USER_SIGNUP_GROUP", [
    "Crowdsource Editor",
    "Resource Editor",
    "Resource Reviewer",
])

settings.DAUTHZ = getattr(settings, "DAUTHZ", {
    # DEFAULT Dauthz enforcer
    "DEFAULT": {
        # Casbin model setting.
        "MODEL": {
            # Available Settings: "file", "text"
            "CONFIG_TYPE": "file",
            "CONFIG_FILE_PATH": settings.CASBIN_MODEL,
            "CONFIG_TEXT": "",
        },
        # Casbin adapter .
        "ADAPTER": {
            "NAME": "casbin_adapter.adapter.Adapter",
            # 'OPTION_1': '',
        },
        "LOG": {
            # Changes whether Dauthz will log messages to the Logger.
            "ENABLED": False,
        },
    },
})


DEFAULT_GROUPINGS = {
    "groups": {
        "allowed_relationships": {
            "http://www.cidoc-crm.org/cidoc-crm/P107_has_current_or_former_member": (True, True),
        },
        "root_group": "d2368123-9628-49a2-b3dd-78ac6ee3e911",
        "graph_id": "07883c9e-b25c-11e9-975a-a4d18cec433a"
    },
    "permissions": {
        "allowed_relationships": {
            "http://www.cidoc-crm.org/cidoc-crm/P107_has_current_or_former_member": (True, False),
            "http://www.cidoc-crm.org/cidoc-crm/P104i_applies_to": (True, True),
            "http://www.cidoc-crm.org/cidoc-crm/P10i_contains": (True, True),
        },
        "root_group": "74e496c7-ec7e-43b8-a7b3-05bacf496794",
    }
}

def get_groupings():
    return getattr(settings, "GROUPINGS", DEFAULT_GROUPINGS)
