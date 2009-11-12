#!/bin/bash


[ -e /etc/sysconfig/freenx-server ] && . /etc/sysconfig/freenx-server

SESSION_TTL=${SESSION_TTL:-3600}
nxdir="/var/lib/nxserver/db/running"
nxserver="/usr/bin/nxserver"
if [ -d "$nxdir" ] ; then
  for f in `ls $nxdir` ; do
    sessiontype=`cat $nxdir/$f | grep status | cut -d= -f2`
    user=`cat $nxdir/$f | grep userName | cut -d= -f2`
    sessiontime=`cat $nxdir/$f | grep creationTime | cut -d= -f2`
    sessionid=`cat $nxdir/$f | grep sessionId | cut -d= -f2`
    criticaltime=$(expr `date +%s` - $SESSION_TTL)
    if [ $sessiontime -lt $criticaltime ] ; then
        if [ $sessiontype = "Suspended" ] ; then
            $nxserver --terminate $sessionid
        fi
    fi
  done
fi