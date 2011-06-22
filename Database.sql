create table user if not exists (task_status int, task_host int, created_at text, 
         tw_id=\'%s\', task_status=\'%s\', task_host=\'%s\', created_at=\'%s\', statuses_count=\'%s\', friend_count=\'%s\', followers_count=\'%s\', geo_lat=\'%s\', geo_long=\'%s\', geo_text=\'%s\' where  name=\'%s\'" ,
                "Insert into tw_userfollower (user_tw_id, follower) values (%s,%s)",
                "Insert into tw_frienduser (friend, user_tw_id) values (%s,%s)"
