#!/bin/bash

date=$(date '+%Y-%m-%d %H:%M:%S')

case "$(ps -ax | grep '/home/omrapp/Desktop/Jugaad_testV1/bin/python3 /home/omrapp/Desktop/Jugaad_testV1/app.py' | wc -l)" in

1) printf "Restarting the application server on %s view Error Logs! \n" "$date"
   nohup /home/omrapp/Desktop/Jugaad_testV1/bin/python3 /home/omrapp/Desktop/Jugaad_testV1/app.py 2>> /home/omrapp/Desktop/reporthash/SYSLOGS_ADMIN_ONLY/appserverlogs/flaskapp_logs.txt &
   ;;

2) printf "App server status checked on %s is GOOD! \n" "$date" >> /home/omrapp/Desktop/reporthash/SYSLOGS_ADMIN_ONLY/appserverlogs/flaskapp_logs.txt &
   ;;
esac

case "$(ps -ax | grep 'python3 /home/omrapp/Desktop/Jugaad_testV1/email_functionV1.py' | wc -l)" in

1) printf "Restarting the email server on %s view Error Logs! \n" "$date"
   nohup python3 /home/omrapp/Desktop/Jugaad_testV1/email_functionV1.py 2>> /home/omrapp/Desktop/reporthash/SYSLOGS_ADMIN_ONLY/appserverlogs/emailserver_logs.txt &

   ;;

2) printf "Email server status checked on %s is GOOD! \n" "$date" >> /home/omrapp/Desktop/reporthash/SYSLOGS_ADMIN_ONLY/appserverlogs/emailserver_logs.txt &
   ;;
esac
