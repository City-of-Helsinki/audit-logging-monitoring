# audit-logging-monitoring

Elasticsearch cloud monitoring application. Works by simply adding and getting last 24h entries from elasticloud


# Configuring


Env variables 

name                      | type         |         default              | description
------------------------- | ------------ | -----------------            |-------------------------------------------------
ELASTICSEARCH_APP_AUDIT_LOG_INDEX | str  | "app_audit_log"              | Index to write to
ELASTICSEARCH_APP_AUDIT_DATA_STREAM | str  | "app_audit_log"            | Data stream to write to
ELASTICSEARCH_HOST        | str          | ""                           | Elastic host name to write to. You can also include port separated by colon.
ELASTICSEARCH_PORT        | int          | 0                            | Elastic port to write to. This can be also given as part of the host.
ELASTICSEARCH_USERNAME    | str          | ""                           | User name for auth
ELASTICSEARCH_PASSWORD    | str          | ""                           | Password for auth



# Running tests
Prerequisites: Setting up neccesary environment variables

Running the tests: 

python3 manage.py tests audit_logging_monitoring

All tests should be successfull
