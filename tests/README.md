### Running tests

These are currently running against the `flaxandteal/arches:docker-7.6` branch with the following command:

    docker exec -ti CONTAINERID  /bin/bash -c ". ../ENV/bin/activate; cd ../arches/; PYTHONPATH=/web_root/PROJECT/tests:\$PYTHONPATH python -W default::DeprecationWarning manage.py test ../PROJECT/tests/casbin_tests/permissions --settings='test_settings'"

Note that lines such as:

    COULD NOT FIND ROOT NODE FOR <class 'abc.DigitalObjectWrapper'>. Does the graph a535a235-8481-11ea-a6b9-f875a44e0e11 still exist?

are not usually problematic, and indicate that the settings are being loaded despite only a subset of the models being included in the `tests/` folder.
