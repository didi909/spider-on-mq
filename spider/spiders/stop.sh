ps -ef|grep python37 |grep Process|grep -v grep|awk '{print "kill -9 "$2}'|sh
