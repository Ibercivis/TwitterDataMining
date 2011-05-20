#!/bin/bash - 
#===============================================================================
#
#          FILE:  ScriptProposal.sh
# 
#         USAGE:  ./ScriptProposal.sh 
# 
#   DESCRIPTION: RealLifeTwitter Oriented to spanish revolution 
# 
#       OPTIONS:  ---
#  REQUIREMENTS:  ---
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR: David Francos Cuartero (XayOn), 
#       COMPANY: 
#       CREATED: 19/05/11 15:29:07 CEST
#      REVISION:  0.1
#===============================================================================


# You need to enable directory listing on your webserver, and add this script to your crontab.
hashtags=("democraciarealya" "spanishrevolution" "acampadamalaga" "acampadasol" "spanishrevolution" )
users=("barcelonarealya")

#filter_cmd="--filter filter"
script=RealLifeTweeter.py
timeout=1
#file=`mktemp -p.`

file="democraciarealya"

for i in "${hashtags[@]}"; do 
    hash_cmd="$hash_cmd --hashtag $i "
done
for i in "${users[@]}"; do 
    user_cmd="$user_cmd --user $i "
done


python $script --destfile $file $user_cmd $hash_cmd $filter_cmd --timeout $timeout
DISPLAY=:0 wkhtmltopdf $file.html $file.pdf
