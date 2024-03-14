# Wrapper script adapted from https://docs.docker.com/config/containers/multi-service_container/#use-a-wrapper-script

# Run generator
java -jar httploadgenerator.jar loadgenerator &

# Run director
java -jar httploadgenerator.jar director -a ./new.csv -l teastore_browse.lua -o output.csv -t 256 &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?