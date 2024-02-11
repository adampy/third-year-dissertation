# Start the director
$LOAD_INTENSITY_PROFILE = "./MYLOADINTENSITYPROFILE.csv"
$REQUEST_PROFILE = "./MYREQUESTPROFILE.lua"
$OUTPUT = "MYOUTPUTFILENAME.csv"
java -jar httploadgenerator.jar director -s localhost -a $LOAD_INTENSITY_PROFILE -l $REQUEST_PROFILE -o $OUTPUT -t 256

#java -jar httploadgenerator.jar director -a ./increasingLowIntensity.csv -l teastore_browse.lua -o output.csv -t 256