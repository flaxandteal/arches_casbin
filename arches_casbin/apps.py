from pathlib import Path
import threading
import tomllib
import time
import os
from django.apps import AppConfig
from django.dispatch import receiver
from arches.app.models.resource import resource_indexed
from arches_orm.wkrm import WELL_KNOWN_RESOURCE_MODELS


class ArchesCasbinConfig(AppConfig):
    name = "arches_casbin"
    is_arches_application = True

    def ready(self):
        global WELL_KNOWN_RESOURCE_MODELS
        existing_wkrms = {str(model.graphid) for model in WELL_KNOWN_RESOURCE_MODELS}
        with (Path(__file__).parent / "wkrm.toml").open("rb") as wkrm_f:
            CASBIN_WELL_KNOWN_RESOURCE_MODELS = [model for _, model in tomllib.load(wkrm_f).items() if model.graphid not in existing_wkrms]
        WELL_KNOWN_RESOURCE_MODELS += CASBIN_WELL_KNOWN_RESOURCE_MODELS

RUNNING = False
@receiver(resource_indexed)
def update_permissions(sender, instance, **kwargs):
    from arches_casbin.utils.casbin import SetApplicator
    # This may run too quickly
    # Instead, it should trigger a (debounced) recalc.
    # This may still require delays _between_ the upserts also.
    def _exec():
        global RUNNING
        set_applicator = SetApplicator(print_statistics=True, wait_for_completion=True)
        if RUNNING:
            return
        RUNNING = True
        try:
            set_applicator.apply_sets(resourceinstanceid=instance.resourceinstanceid)
        except Exception as exc:
            print("Apply sets failed with", exc)
            time.sleep(3.0)
        finally:
            RUNNING = False
    threading.Timer(3.0, _exec).start()

if os.getenv("CASBIN_LISTEN", False):
    print("Casbin is listening")
    from arches_casbin.permissions.casbin import trigger
    t = threading.Thread(target=trigger.listen)
    t.setDaemon(True)
    t.start()
    print("Thread started", t)
