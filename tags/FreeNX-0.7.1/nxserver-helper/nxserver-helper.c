/*
 * Copyright (c) 2006 by Fabian Franz.
 *
 * License: GPL, v2
 *
 * SVN: $Id: nxserver-helper.c 405 2007-10-14 22:25:14Z fabianx $
 *
 */

#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>

int main(int argc, char* argv[])
{
	int fds[2];

	socketpair(AF_UNIX, SOCK_STREAM, 0, fds);
	argv++;
	execv(argv[0], argv);
}
