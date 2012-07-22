# Copyright 1999-2011 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: /var/cvsroot/gentoo-x86/net-misc/nxserver-freenx/nxserver-freenx-0.7.3_p104-r6.ebuild,v 1.4 2011/11/24 21:00:12 voyageur Exp $

EAPI=4

inherit git-2 multilib eutils toolchain-funcs versionator

MAJOR_PV="$(get_version_component_range 1-3)"
PATCH_VER="$(get_version_component_range 4)"
MY_PN="freenx-server"

DESCRIPTION="Free Software Implementation of the NX Server"
HOMEPAGE="http://freenx.berlios.de/ https://launchpad.net/~freenx-team"
EGIT_REPO_URI="git://git.etersoft.ru/people/dimbor/packages/freenx-server.git"
#EGIT_BOOTSTRAP="autogen.bash"
SRC_URI=""
LICENSE="GPL-2"
SLOT="0"
KEYWORDS="amd64 x86"
IUSE="nxclient rdesktop vnc"

DEPEND="x11-misc/gccmakedep
	x11-misc/imake"
RDEPEND="dev-tcltk/expect
	media-fonts/font-cursor-misc
	sys-devel/bc
	media-fonts/font-misc-misc
	net-analyzer/gnu-netcat
	>=net-misc/nx-2.1.0
	sys-apps/gawk
	virtual/ssh
	x11-apps/xauth
	x11-apps/xrdb
	x11-apps/sessreg
	x11-terms/xterm
	nxclient? ( net-misc/nxclient )
	!nxclient? ( !net-misc/nxclient
				 || ( x11-misc/xdialog
					  x11-apps/xmessage
					    gnome-extra/zenity ) )
	rdesktop? ( net-misc/rdesktop )
	vnc? ( x11-misc/x11vnc
		   net-misc/tightvnc )"

S=${WORKDIR}

export NX_HOME_DIR=/var/lib/nxserver/home

pkg_setup () {
	enewuser nx -1 -1 ${NX_HOME_DIR}
}

src_prepare() {
	cd ${S}
	epatch "${FILESDIR}"/nxserver-freenx-0.7.4-pam_ssh.patch
	epatch "${FILESDIR}"/nxserver-freenx-0.7.4-nxloadconfig.patch

	# Path to net-misc/nx files, support for nx >= 3.4.0
	sed	-e "/PATH_LIB=/s/lib/$(get_libdir)/g" \
		-e "s#REAL_PATH_LIB#/usr/$(get_libdir)/NX/bin#" \
		-i ${MY_PN}/nxloadconfig || die "nxloadconfig sed failed"
}

src_compile() {
	cd ${MY_PN}
	emake CC=$(tc-getCC) CDEBUGFLAGS="${CFLAGS}" || die "compilation failed"
}

src_install() {
	export NX_ETC_DIR=/etc/nxserver
	export NX_SESS_DIR=/var/lib/nxserver/db

	cd ${MY_PN}
	emake DESTDIR="${D}" install || die "install failed"

#	LIBREDIR_DIR="${D}""usr/lib/freenx-server"
#	dodir "/usr/lib/freenx-server"
#	OLDREDIR_DIR="${D}""usr/$(get_libdir)/NX/$(get_libdir)/freenx-server"
#	mv ${OLDREDIR_DIR}/libnxredir.so.0 ${LIBREDIR_DIR}
#	[[ $(get_libdir) == "lib64" ]] && rm -r "${D}""usr/$(get_libdir)" || \
#	    rm -r "${D}""usr/$(get_libdir)/NX"


	# This should be renamed to remove the blocker on net-misc/nxclient
	use nxclient && rm "${D}"/usr/bin/nxprint

	dodir ${NX_ETC_DIR}
	for x in passwords passwords.orig ; do
		touch "${D}"${NX_ETC_DIR}/$x
		chmod 600 "${D}"${NX_ETC_DIR}/$x
	done


	insinto ${NX_ETC_DIR}
	for x in Xkbmap Xsession fixkeyboard ; do
	    doins "${S}/${MY_PN}/data/$x"
	    [[ $x == "Xkbmap" ]] && continue
	    chmod 755 "${D}"${NX_ETC_DIR}/$x
	done

	CONF_DIR="${NX_ETC_DIR}"/node.conf.d
	dodir ${CONF_DIR}
	insinto ${CONF_DIR}

	doins "${S}/${MY_PN}/conf/conf.d"/*
	cp "${FILESDIR}"/70-gentoo.conf "${D}"${CONF_DIR}

	ACL_DIR="${NX_ETC_DIR}/acls"
	dodir "${ACL_DIR}"
	insinto "${ACL_DIR}"
	doins "${S}/${MY_PN}/conf/acls"/*

	dodir "${NX_ETC_DIR}/ppd"

	SUDO_DIR=/etc/sudoers.d
	dodir ${SUDO_DIR}
	insinto "${SUDO_DIR}"
	newins "${S}/sudoers.conf" nxserver
	chmod 440 "${D}"${SUDO_DIR}/nxserver

	LOGR_DIR=/etc/logrotate.d
	dodir ${LOGR_DIR}
	insinto "${LOGR_DIR}"
	newins "${S}/${MY_PN}/data/logrotate" nxserver

	dodir ${NX_HOME_DIR}

	for x in closed running failed ; do
		keepdir ${NX_SESS_DIR}/$x
		fperms 0700 ${NX_SESS_DIR}/$x
	done

	newinitd "${FILESDIR}"/nxserver.init nxserver
}

pkg_postinst () {
	# Other NX servers ebuilds may have already created the nx account
	# However they use different login shell/home directory paths
	if [[ ${ROOT} == "/" ]]; then
		usermod -s /usr/bin/nxserver nx || die "Unable to set login shell of nx user!!"
		usermod -d ${NX_HOME_DIR} nx || die "Unable to set home directory of nx user!!"
		usermod -a -G utmp nx || die "Unable to add nx user to utmp group!!"
	else
		elog "If you had another NX server installed before, please make sure"
		elog "the nx user account is correctly set to:"
		elog " * login shell: /usr/bin/nxserver"
		elog " * home directory: ${NX_HOME_DIR}"
		elog " * supplementary groups: utmp"
	fi

	elog "To complete the installation, run:"
	elog " nxsetup --install --setup-nomachine-key"
	elog "This will use the default Nomachine SSH key"
	elog "If you had older NX servers installed, you may need to add \"--clean --purge\" to the nxsetup command"

	if has_version net-misc/openssh[-pam]; then
		elog ""
		elog "net-misc/openssh was not built with PAM support"
		elog "You will need to unlock the nx account by setting a password for it"
	fi
}
