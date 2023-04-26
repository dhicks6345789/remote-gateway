while getopts servername:databasepw:guacpw: flag
do
  case "${flag}" in
    servername) servername=${OPTARG};;
    databasepw) databasepw=${OPTARG};;
    guacpw) guacpw=${OPTARG};;
  esac
done
echo "Servername: $servername";
echo "Database password: $databasepw";
echo "Guacamole password: $guacpw";
