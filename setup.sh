# this file doesnt work as a script (yet)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate

RANDOM=tr -dc A-Za-z0-9 </dev/urandom | head -c 32;

echo MySQL Server Login (<user>:<password>@<address>:<port>):
read MYSQL_ADDRESS

export SECRET_KEY=$RANDOM
export DATABASE_URL='mysql+pymysql://${MYSQL_ADDRESS}/'
export LEAGUE_MANAGER_DB=league_manager
export API_ACCESS_DB=api_access
export MAIL_SERVER=localhost
export MAIL_PORT=8025