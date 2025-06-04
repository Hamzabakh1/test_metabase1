FROM metabase/metabase:latest
EXPOSE 8080
CMD ["java", "-jar", "metabase.jar"]
