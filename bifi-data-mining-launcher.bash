#!/bin/bash 
mysql=/usr/bin/mysql; ifconfig=/sbin/ifconfig; iface=eth0; mysql_password="root"; mysql_host="localhost"; mysql_user="root"; limit=1; db="smmart_20"; table="tw_user"
debug=1
log=foo.log
getoptions(){
    while getopts "hi:t:d:p:x:u:l:" OPTION; do 
        case "$OPTION" in
            h) usage ;;
            p) export mysql_password="$OPTARG";;
            x) export mysql_host="$OPTARG";;
            u) export mysql_user="$OPTARG";;
            i) export iface="$OPTARG";;
            d) export db="$OPTARG";;
            t) export table="$OPTARG";;
            l) export limit="$OPTARG";;
        esac
    done
}

usage(){ cat <<EOF
$0 [OPTION]
    -p PASSWD   set mysql password
    -x HOST     set mysql host
    -u USER     set mysql user
    -l LIMIT    limit of results to get/set 
    -i IFACE    network interface to get ip from
    -d DB       database to use
    -t table    table to use
    -h          show this menu
EOF
exit
}

get_mysql_opts(){
    opts=" "
    [[ "${mysql_password}" != "" ]] && opts="${opts} -p${mysql_password}"
    [[ "${mysql_host}" != "" ]] && opts="${opts} -h${mysql_host}"
    [[ "${mysql_user}" != "" ]] && opts="${opts} -u${mysql_user}"
    echo "${opts}"
}

get_ip(){ awk '/inet addr/ {print substr($2, 6)}' <<< "$($ifconfig $iface)"; } # WARN: This might not be nicely ported... but hell, the rest of the script isn't either.
execute_mysql_query(){ $mysql $(get_mysql_opts) -N $db <<< "${1}" ; }
set_myself_in_database(){ execute_mysql_query "update $table set task_host='$1', task_status=1 where task_status=0 limit $limit"; }
get_from_database(){ execute_mysql_query "select name from $table where task_host='$1' and task_status=1"; }

ip=$(get_ip)
getoptions "${@}"

main(){
    echo "Connecting to $mysql_host with user $mysql_user and limit $limit for ip $ip and password $mysql_password"

for i in `seq 1 3`; do
    for i in `seq 1 10`; do
    	set_myself_in_database $ip
	rm $ip.csv; create_csv;
	echo "Getting users:"
	cat $ip.csv
        python RealLifeTweeter.py --destfile foo  --save_file --user_info --external_users $ip.csv --no-auth --enable_mysql $mysql_host,$mysql_user,$mysql_password,$db &> $log # Note: You can delete desfile and save_file
    done 
    sleep 600 # Sleep 10m foreach 10 users. This way we won't reach the limits
done
}

create_csv(){
    csv="$(get_from_database ${ip})"
    echo "Got $csv"
    echo $csv | sed "s/ /,/g" >> $ip.csv
}

[[ $debug ]] && { [[ $log ]] && main &> $log || main ; } || main &>/dev/null 

