- FROM metabase/metabase:latest
+ FROM metabase/metabase-enterprise:v1.55.9

- EXPOSE 8080
+ # Variables Railway Postgres
+ ENV MB_DB_TYPE=postgres
+ ENV MB_DB_DBNAME=metabase
+ ENV MB_DB_PORT=5432
+ ENV MB_DB_USER=metabase
+ ENV MB_DB_PASS=${MB_DB_PASS}
+ ENV MB_DB_HOST=${MB_DB_HOST}
+ # Licence Pro injectée en Secret Railway
+ ENV MB_LICENSE_TOKEN=${MB_LICENSE_TOKEN}
+ EXPOSE 8080
