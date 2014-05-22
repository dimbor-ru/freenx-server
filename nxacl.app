#!/bin/bash
# v1.0. Copyleft by dimbor at unixforum.org <akadown@pisem.net>
# Script parse ACLS-files in NX_ACL_DIR and search user/group permissions for given cmdstr.
# ACLS filenames are usernames, groupnames and "all". Permissions search order:
# user - group - all. ACL contain one or more strings of regexp-patterns. Format:
#
# # some comment-string
# [!]CmdTpl [%%% [[!][@@]OnceAppTpl] %%% Prog|"Msg"]
#
# ! - not equal == invert rule
# %%% - fields delimiter
# CmdTpl - startsession command template
# OnceAppTpl - if it not found/found (""/"!") in process-list of user do'nt start session
# @@ - search in process-list of all users (ps ax)
# Prog - string for nxdialog or other x-binary to execute instead session-app
# if "OnceAppTpl" condition is FALSE
#
# Attention!!! Spec-symbols (like ".","$","^") must be escaped twice vs once
# ('\\.' vs '\.'), sorry.
#
# TODO: remote shares an printers control.

# Read the config file
. $(PATH=$(cd $(dirname $0) && pwd):$PATH which nxloadconfig) --userconf

# test-line for unix-kde
#CMDPAR="&link=modem&backingstore=1&encryption=1&cache=32M&images=64M&shmem=1&shpix=1&strict=0&composite=1&samba=1&media=0&session=csrvKDE&type=unix-kde&geometry=1280x1024&client=winnt&keyboard=pc102/en_US&screeninfo=1280x1024x32+render&clientproto=3.2.0&login_method=SU&user=dim&userip=1.2.3.4&uniqueid=21C9152FF3D59AC7062F970AD174F256&display=2001&host=127.0.0.1"
# test-line for rootless
#CMDPAR="&rootless=1&virtualdesktop=0&application=/home/dim/1c.sh&link=modem&backingstore=1&encryption=1&cache=32M&images=64M&shmem=1&shpix=1&strict=0&composite=1&samba=1&media=0&session=csrv1c&type=unix-application&client=winnt&kbload=pc102/en_US&keymap=en_US&keyboard=pc102/en_US&aux=1&screeninfo=1280x1024x32+render&clientproto=3.2.0&login_method=SU&user=dim&userip=1.2.3.4&uniqueid=FC6EABFE60F3DFF4E38D7C4F52C27678&display=2000&host=127.0.0.1"

GAPP="$1" ; shift
CMDPAR="$@"
SELF="$(basename "$0")"
USR="$USER" # set session's username

stringinstring() { case "$2" in *$1*) return 0 ;; esac; return 1; }

getparam() {
    stringinstring "&$1=" "$CMDPAR" || return 1
    echo "$CMDPAR" |  tr "&" "\n" | egrep "^"$1"=" | awk -F= '{ VAL=$2 } END { print VAL }'
    return 0
}

nxlog() {
# There is almost copy+paste code from nxnode... Ups! - Not almost.
    [ $NX_LOG_LEVEL -ne 7 ] && return 0
    UFH="$USER_FAKE_HOME/.nx"; mkdir -p "$UFH" # TODO FIX. How?
    sessionid=$(getparam uniqueid)
    [ -n "$sessionid" ] || sessionid=$(getparam session_id) # need in the future for shares control?
    LOG_FN="$UFH/$SELF-$sessionid.log"
    password=$(getparam password) # need in the future for shares control?
    echo -n "$(date "+%d.%m %X"): " >> "$LOG_FN"
    [ -z "$password" ] && echo "$@" >> "$LOG_FN" || \
	echo "$@" | sed 's/'$password'/****/g' >> "$LOG_FN"
    return 0
}


parse_file() {
# args: filename, app-string
    nxlog "$FUNCNAME ($$): Start parsing ACL-file \"$1\"; given app-string \"$2\""
    while read LIN; do
	LIN="$(echo "$LIN" | sed 's/^\s\+//;s/\s\+$//')" # delete starting an tailing spaces
	[ -n "$LIN" ] || continue
	nxlog "$FUNCNAME ($$): Parse line: \"$LIN\""
	APTPL="$(echo "$LIN" | awk 'BEGIN {FS="%%%"} {print $1}' | sed 's/^\s\+//;s/\s\+$//')"
	[ "${LIN:0:1}" = "#" ] && { nxlog "$FUNCNAME ($$): Comment-string found - passed"; continue; }
	PSTPL="$(echo "$LIN" | awk 'BEGIN {FS="%%%"} {print $2}' | sed 's/^\s\+//;s/\s\+$//')"
	WSTR="$(echo "$LIN" | awk 'BEGIN {FS="%%%"} {print $3}' | sed 's/^\s\+//;s/\s\+$//')"
        [ -z "$PSTPL" -a  -n "$WSTR" ] && {
	    nxlog "$FUNCNAME ($$): Replace string-present. Substitute in empty process-pattern fake-condition \"!.*\"";
	    PSTPL="!.*"
        }
	APINV="0"; [ "${APTPL:0:1}" = "!" ] && { APTPL="${APTPL:1}"; APINV="1"; }
	LSTR="App-pattern = \"$APTPL\", Inversion = $APINV"
	R1="0"; [ -n "$(echo "$2" | grep --regexp="$APTPL")" ] && R1="1"
	[ $((APINV+R1)) -ne 1 ] && {
	    LSTR="$LSTR ==> app-pattern not match"
	    nxlog "$FUNCNAME ($$): $LSTR, passed."; continue;
	}
	LSTR="$LSTR ==> app-pattern match"
	[ -z "$PSTPL" ] && {
	    nxlog "$FUNCNAME ($$): $LSTR, RC=0, stop parsing."; echo "$2"; return 0;
	}
	PSINV="0"; [ "${PSTPL:0:1}" = "!" ] && { PSTPL="${PSTPL:1}"; PSINV="1"; }
	PSA="0"; [ "${PSTPL:0:2}" = "@@" ] && { PSTPL="${PSTPL:2}"; PSA="1"; }
	[ $PSA -eq 0 ] && {
	    [ -z "$PSL" ] && PSL="$(ps -o cmd= -U $USR)"; PSW="$PSL"
	} || {
	    [ -z "$PSLA" ] && PSLA="$(ps ax -o cmd=)"; PSW="$PSLA"
	}
	PSW="$(echo "$PSW" | sed '/'"$SELF"'/d')"
	LSTR="$LSTR; Process-pattern = \"$PSTPL\", Inversion = $PSINV, search-area in processes of"
	[ $PSA -eq 1 ] && LSTR="$LSTR ALL users" || LSTR="$LSTR $USR only"
	nxlog "Proc-list: \"$PSW\""
	R2="0"; [ -n "$(echo "$PSW" | grep --regexp="$PSTPL")" ] && R2="1"
	[ $((PSINV+R2)) -eq 1 ] && {
	    nxlog "$FUNCNAME ($$): $LSTR ==> proc-pattern match, RC=0, stop parsing.";
	    echo "$2"; return 0;
	}
	LSTR="$LSTR ==> proc-pattern not match"
	[ -n "$WSTR" ] && {
	    nxlog "$FUNCNAME ($$): $LSTR; Found replace-string \"$WSTR\", RC=1, stop parsing.";
	    echo "$WSTR"; return 1;
	}
	nxlog "$FUNCNAME ($$): $LSTR, RC=1, stop parsing."
	return 1;
    done < $1
    nxlog "$FUNCNAME ($$): EOF, any matches not found, RC=2, stop parsing."; return 2
}

nxlog "$SELF ($$): run with APP=\"$GAPP\"; PARAMS=\"$CMDPAR\""
WARN_APP='/usr/bin/nxdialog --dialog ok --caption "Acces denied!" --message '
WARN_MSG='"Acces denied! Session be terminated."'
[ -d $NX_ACL_DIR ] || {
    nxlog "$SELF ($$): NX_ACL_DIR=\"$NX_ACL_DIR\" not found. ACLS control disabled, warn.";
    echo "$APP"; exit 0;
}
LSACLD="$(ls "$NX_ACL_DIR" 2>/dev/null)"
[ -z "$LSACLD" ] && {
    nxlog "$SELF ($$): NX_ACL_DIR=\"$NX_ACL_DIR\" is empty. ACLS control disabled, warn.";
    echo "$APP";  exit 0;
}
UACLS="$(echo $(groups $USR | sed 's/'$USR' ://')) $USR all" # user's groups + spec-files
nxlog "$SELF ($$): attempt to control session for USER=\"$USR\", his ACLS can be \"$UACLS\"."

# parse NX_ACL_DIR files, sorting order "user-groups-all"
PSL=""; PSLA=""; # processes lists
DC="$(ls "$NX_ACL_DIR" | sed '/'$USR'/d;/all/d')"
[ -r "$NX_ACL_DIR/$USR" ] &&  DC=$USR$'\n'"$DC"
[ -r "$NX_ACL_DIR/all" ] &&  DC="$DC"$'\n'"all"
PARSED="0"
for PFILE in $DC; do
    [ -z "$(echo "$UACLS" | grep -w "$PFILE")" ] && continue
    APP="$(parse_file "$NX_ACL_DIR/$PFILE" "$GAPP")"; RC=$?
    [ $RC -eq 0 ] && { # All right!
	"$SELF ($$): User $USR have permission to start. Return source APP \"$APP\""
	echo "$APP"; exit 0;
    }
    [ $RC -eq 1 ] && {
	# OnlyOnceApp condition - replace app mode
	[ -n "$APP" ] && {
	    [ "${APP:0:1}" = '"' ] && APP="$WARN_APP$APP" || {
		[ -x $(echo "$APP" | cut -d' ' -f1) ] || APP="$WARN_APP$WARN_MSG"
	    } || APP="$WARN_APP$WARN_MSG"
	} || APP="$WARN_APP$WARN_MSG"
        PARSED="1"; break;
    }
done
[ "$PARSED" = "1" ] && nxlog "$SELF ($$): Setup session APP to \"$APP\"" || {
    APP="$WARN_APP$WARN_MSG"
    nxlog "$SELF ($$): No rules found for. Setup session APP to default \"$APP\""
}
SFNAME="$USER_FAKE_HOME/.nx/suicidal-$$"
cat <<EOF > $SFNAME
#!/bin/bash
$APP
rm $SFNAME
EOF
chmod 700 $SFNAME
nxlog "$SELF ($$): Create script \"$SFNAME\" and return reference to."
echo "$SFNAME"
exit 0
