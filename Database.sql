create table user if not exists (tw_id int, task_status int, task_host int, created_at text, statuses_count int, friends_count int, followers_count int, geo_lat text, geo_long text, geo_text text, geo_province text, geo_community text);
create table if not exists tw_userfollower (user_tw_id int, follower int);
create table if not exists tw_frienduser (friend int, user_tw_id int);
