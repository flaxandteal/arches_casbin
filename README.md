# Arches Casbin

(credit to @chiatt for the template)

Arches Casbin is a permissions plugin for Arches to use Casbin
permissions. This assumes RBAC-based permissions where *all* of
your plugin and resource permission rules are based on groups of
users mapping to sets of resources, possibly with only one member.

(For practical reasons, each resource can have a single, changeable
principal user who can bypass group permissions)

You can add Casbin to an Arches project as follows.

1. Install if from this repo (or clone this repo and pip install it locally). 
```
pip install git+https://github.com/flaxandteal/arches_casbin.git
```

2. Add `"arches_casbin"` to the INSTALLED_APPS setting in the demo project's settings.py file below the demo project:
```
INSTALLED_APPS = [
    ...
    "arches_casbin",
]
```

3. Version your dependency on `"arches_casbin"` in `pyproject.toml`:
```
dependencies = [
    "arches>=7.6.0,<7.7.0",
    "arches_casbin==0.0.1",
]
```

4. Run the following to import the `permissions`:
```
python manage.py packages -o load_package -a arches_casbin
```

5. Next be sure to rebuild your project's frontend to include the plugin:
```
npm run build_development
```

## Settings

The following settings may be added to your project settings file:

    USE_CASBIN = os.getenv("USE_CASBIN", "true").lower() == "true"
    if USE_CASBIN:
        AUTHENTICATION_BACKENDS = (
            *AUTHENTICATION_BACKENDS,
            "dauthz.backends.CasbinBackend",
        )
        PERMISSION_FRAMEWORK = "casbin.CasbinPermissionFramework"
        INSTALLED_APPS = (
            *INSTALLED_APPS,
            "casbin_adapter.apps.CasbinAdapterConfig"
        )
    else:
        PERMISSION_FRAMEWORK = "arches_allow_with_credentials.ArchesAllowWithCredentialsFramework"

    # If True, allows for user self creation via the signup view. If False, users can only be created via the Django admin view.
    ENABLE_USER_SIGNUP = False
    ENABLE_PERSON_USER_SIGNUP = True

Optionally, you can add:

    GROUPINGS = {
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
    USER_SIGNUP_GROUP = "Crowdsource Editor"
    ALLOWED_SIGNUP_GROUPS = [
        "Crowdsource Editor",
        "Resource Editor",
        "Resource Reviewer",
    ]

