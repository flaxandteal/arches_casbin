"""
ARCHES - a program developed to inventory and manage immovable cultural heritage.
Copyright (C) 2013 J. Paul Getty Trust and World Monuments Fund

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import time
import logging
import readline
import psycopg2
from arches.app.models.system_settings import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group as DjangoGroup

logging.basicConfig()

COOLOFF_S = 10

class Command(BaseCommand):
    """Recalculate ES resource->set mapping.

    """

    print_statistics = False

    def add_arguments(self, parser):
        parser.add_argument(
            "-s",
            "--statistics",
            action="store_true",
            dest="print_statistics",
            help="Do extra searches to provide relevant statistics?",
        )


    def handle(self, *args, **options):
        # Cannot be imported until Django ready
        from arches_casbin.permissions.casbin import CasbinPermissionFramework
        from arches_casbin.utils.casbin import SetApplicator

        print_statistics = True if options["print_statistics"] else False

        set_applicator = SetApplicator(print_statistics=print_statistics, wait_for_completion=True)
        try:
            set_applicator.apply_sets()
        except psycopg2.OperationalError:
            time.sleep(COOLOFF_S)

        framework = CasbinPermissionFramework()
        framework.recalculate_table()
