Summary: Utilities for managing processes on your system
Name: psmisc
Version: 22.6
Release: 15%{?dist}
License: GPLv2+
Group: Applications/System
Source: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
URL: http://sourceforge.net/projects/psmisc
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#fix configure.ac to include all the required headers for peekfd
Patch0: psmisc-22.6-types.patch
#fix #441871
Patch1: psmisc-22.6-pstree-overflow.patch
#fix #497303
Patch2: psmisc-22.6-fuser-remove-mountlist.patch
Patch3: psmisc-22.6-overflow2.patch
#fix #596055
Patch4: psmisc-22.6-udp.patch

BuildRequires: libselinux-devel
BuildRequires: gettext
BuildRequires: ncurses-devel
BuildRequires: autoconf automake

%description
The psmisc package contains utilities for managing processes on your
system: pstree, killall and fuser.  The pstree command displays a tree
structure of all of the running processes on your system.  The killall
command sends a specified signal (SIGTERM if nothing is specified) to
processes identified by name.  The fuser command identifies the PIDs
of processes that are using specified files or filesystems.

%prep
%setup -q
%patch0 -p1 -b .types
%patch1 -p1 -b .overflow
%patch2 -p1 -b .mount
%patch3 -p1 -b .overflow2
%patch4 -p1 -b .udp

%build
export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE"
autoreconf
%configure --prefix=%{_prefix} --enable-selinux
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
# The rpm makeinstall macro breaks the build, so we do it the old way
make install DESTDIR="$RPM_BUILD_ROOT"

mkdir -p $RPM_BUILD_ROOT/sbin
mv $RPM_BUILD_ROOT%{_bindir}/fuser $RPM_BUILD_ROOT/sbin
rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/pidof.1*
rm -f $RPM_BUILD_ROOT/%{_bindir}/oldfuser
%ifnarch %ix86 x86_64 ppc ppc64
rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/peekfd.1*
%endif

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
/sbin/fuser
%{_bindir}/killall
%{_bindir}/pstree
%{_bindir}/pstree.x11
%{_mandir}/man1/fuser.1*
%{_mandir}/man1/killall.1*
%{_mandir}/man1/pstree.1*
%doc INSTALL AUTHORS COPYING README
%ifarch %ix86 x86_64 ppc ppc64
%{_bindir}/peekfd
%{_mandir}/man1/peekfd.1*
%endif

%changelog
* Wed May 26 2010 Jan Görig <jgorig@redhat.com> 22.6-15
- Fixed udp namespace problem in fuser
- Resolves: rhbz#596055

* Thu Feb 25 2010 Daniel Novotny <dnovotny@redhat.com> 22.6-14
- added docs (README etc.)

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 22.6-13.1
- Rebuilt for RHEL 6

* Wed Aug 05 2009 Lubomir Rintel <lkundrak@v3.sk> - 22.6-13
- Fix a buffer overflow

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 22.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 11 2009 Daniel Novotny <dnovotny@redhat.com> 22.6-11
- merge review (#226322): a few .spec changes

* Thu Apr 23 2009 Daniel Novotny <dnovotny@redhat.com> - 22.6-10
- fix #497303 -  fuser -m <dev> doesn't work after lazy unmount

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 22.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> 22.6-8
- fix package so it builds again

* Fri Aug 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> 22.6-7
- fix license tag

* Mon Apr 14 2008 Tomas Smetana <tsmetana@redhat.com> 22.6-6
- fix #441871 - pstree fails to show most processes;
  patch by Emil Jerabek

* Mon Apr 07 2008 Tomas Smetana <tsmetana@redhat.com> 22.6-5
- fix configure.ac to include all the required headers for peekfd
- remove kernel-headers again -- not needed in rawhide

* Mon Apr 07 2008 Tomas Smetana <tsmetana@redhat.com> 22.6-4
- fix #440762 - add kernel-headers to build reuqirements

* Tue Feb 12 2008 Tomas Smetana <tsmetana@redhat.com> 22.6-3
- rebuild (gcc-4.3)

* Mon Dec 10 2007 Tomas Smetana <tsmetana@redhat.com> 22.6-2
- fix #417801 - exclude peekfd on secondary architectures

* Mon Dec 03 2007 Tomas Smetana <tsmetana@redhat.com> 22.6-1
- update to new upstream version

* Wed Aug 29 2007 Tomas Smetana <tsmetana@redhat.com> 22.5-2
- rebuild (because of BuildID)

* Thu Jun 07 2007 Tomas Smetana <tsmetana@redhat.com> 22.5-1.2
- exclude peekfd manpage on non-x86 archs

* Thu Jun 07 2007 Tomas Smetana <tsmetana@redhat.com> 22.5-1.1
- rebuild

* Wed Jun 06 2007 Tomas Smetana <tsmetana@redhat.com> 22.5-1
- update to new upstream version

* Thu Mar  1 2007 Karel Zak <kzak@redhat.com> 22.3-2
- fix #214214 - killall <path> misbehavior (prelink, etc)

* Thu Mar  1 2007 Karel Zak <kzak@redhat.com> 22.3-1
- update to upstream 22.3
- backport ipv6 bugfix from upstream CVS
- clean up spec file

* Wed Jul 19 2006 Karel Zak <kzak@redhat.com>  - 22.2-5
- spec file cleanup & rebuild

* Mon Jul 17 2006 Jesse Keating <jkeating@redhat.com> - 22.2-4
- rebuild

* Wed May 17 2006 Karel Zak <kzak@redhat.com> 22.2-2
- add BuildRequires: gettext-devel
- sync with upstream

* Wed Mar 22 2006 Karel Zak <kzak@redhat.com> 22.1.03072006cvs-1.1
- rebuild

* Tue Mar  7 2006 Karel Zak <kzak@redhat.com> 22.1.03072006cvs-1
- update to new upstream CVS version 
- enable new fuser version
- fix fuser return code 
- fix #183897 - "pstree -a" call results in segmentation fault

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 21.8-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 21.8-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 30 2005 Karel Zak <kzak@redhat.com> 21.8-1
- fix #174585 - killall crashes on long variable name
- spec file cleanup

* Wed Oct  5 2005 Karel Zak <kzak@redhat.com> 21.7-1.cvs20051005
- sync with upstream CVS
- use old version of fuser

* Thu Sep  8 2005 Karel Zak <kzak@redhat.com> 21.6-1
- sync with upstream release 21.6
- cleanup selinux patch
- fix #165167 - buffer overflow detected in fuser

* Sat Mar  5 2005 Karel Zak <kzak@redhat.com> 21.5-4
- fixed problem with perl expression in the build .spec section

* Sat Mar  5 2005 Karel Zak <kzak@redhat.com> 21.5-3
- rebuilt

* Tue Dec 14 2004 Karel Zak <kzak@redhat.com> 21.5-2
- use other way for psmisc-21.5-term.patch

* Mon Dec 13 2004 Karel Zak <kzak@redhat.com> 21.5-1
- Updated to new upstream version 21.5
- Ported SELinux patch forward as psmisc-21.5-selinux.patch
- Added psmisc-21.5-term.patch that fix termcap.h and term.h conflicts

* Fri Sep 24 2004 Mike A. Harris <mharris@redhat.com> 21.4-4
- Added "BuildRequires: libselinux-devel" for WITH_SELINUX builds (#123754)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com> 21.4-3
- rebuilt

* Sun Mar 15 2004 Mike A. Harris <mharris@redhat.com> 21.4-2
- Re-enabled SELINUX support
- Removed gcc33 patch, no longer needed it seems.

* Sun Mar 15 2004 Mike A. Harris <mharris@redhat.com> 21.4-1
- Updated to new upstream version 21.4
- Ported SELinux patch forward as psmisc-21.4-redhat-selinux-psmisc.patch,
  but disabled SELINUX support temporarily until other build problems are
  resolved
- Remove MKINSTALLDIRS-./mkinstalldirs from "make install" as that causes the
  build to fail when "./" changes.  If this option is ever added back, make
  it relative to $RPM_BUILD_DIR instead of ./ so that things do not break
- Added pstree.x11 to file list after rpm reported it present in buildroot but
  not packaged

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 21.3-8
- rebuilt

* Mon Jan 26 2004 Dan Walsh <dwalsh@redhat.com> 21.3-7
- fix is_selinux_enabled call

* Fri Sep 5 2003 Dan Walsh <dwalsh@redhat.com> 21.3-6.sel
- turn on selinux
- Hack to fix build problem on Fedora core

* Fri Sep 5 2003 Dan Walsh <dwalsh@redhat.com> 21.3-6
- turn off selinux

* Thu Aug 28 2003 Dan Walsh <dwalsh@redhat.com> 21.3-5.sel
- change flags to -Z and build for selinux

* Tue Jul 28 2003 Dan Walsh <dwalsh@redhat.com> 21.3-4
- Remove -lsecure check from configure.

* Tue Jul 28 2003 Dan Walsh <dwalsh@redhat.com> 21.3-2
- Added SELinux patches

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 29 2003 Mike A. Harris <mharris@redhat.com> 21.3-1.RHEL.0
- Bump to 21.3-1.RHEL.0 and rebuild for Red Hat Enterprise Linux

* Thu May 29 2003 Mike A. Harris <mharris@redhat.com> 21.3-1
- Updated to new upstream version 21.3
- Removed dead script gensig.sh
- Disabled psmisc-21.2-gcc33.patch as it is included in 21.3

* Thu May 22 2003 Jeremy Katz <katzj@redhat.com> 21.2-5
- fix build with gcc 3.3

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Nov 13 2002 Mike A. Harris <mharris@redhat.com> 21.2-3
- Remove pidof manpage from buildroot by adding with_pidof conditional
- _bindir cleanup

* Wed Nov 13 2002 Mike A. Harris <mharris@redhat.com> 21.2-2
- Updated to new upstream version 21.2
- Updated Source: URL to sourceforge's current ftp area
- Fixes fuser largefile bug (#66340)
- Disable prep time sh %%{SOURCE1} >src/signames.h as the 21.2 release
  fixes this already now.

* Tue Oct  8 2002 Mike A. Harris <mharris@redhat.com> 20.2-7
- All-arch rebuild
- Updated spec file with _bindir et al. fixes.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 20.2-6
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com> 20.2-5
- automated rebuild

* Thu May 16 2002 Bernhard Rosenkraenzer <bero@redhat.com> 20.2-4
- Autogenerate the signal list from _includedir/bits/signum.h
  to make sure it works on all arches and doesn't break again.

* Wed May  8 2002 Trond Eivind Glomsrod <teg@redhat.com> 20.2-3
- Fix the signal list
- Don't strip when linking
- Use a %%{_tmppath}

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Nov 20 2001 Bernhard Rosenkraenzer <bero@redhat.com> 20.2-1
- 20.2
- Add patch from bug report #56186; the problem is not reproducable,
  but the patch can't hurt.

* Sat Jul 21 2001 Bernhard Rosenkraenzer <bero@redhat.com> 20.1-2
- Add BuildRequires (#49562)
- s/Copyright/License/
- Fix license (it's actually dual-licensed BSD/GPL, not just "distributable")

* Wed Apr 25 2001 Bernhard Rosenkraenzer <bero@redhat.com> 20.1-1
- 20.1

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Matt Wilson <msw@redhat.com>
- FHS man paths
- patch makefile to enable non-root builds

* Sat Feb  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Deal with compressed man pages

* Sun Nov 21 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- update to v19
- handle RPM_OPT_FLAGS

* Mon Sep 27 1999 Bill Nottingham <notting@redhat.com>
- move fuser to /sbin

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Sat Mar 13 1999 Michael Maher <mike@redhat.com>
- updated package

* Fri May 01 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- renamed the patch file .patch instead of .spec

* Thu Apr 09 1998 Erik Troan <ewt@redhat.com>
- updated to psmisc version 17
- buildrooted

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- updated from version 11 to version 16
- spec file cleanups

* Tue Jun 17 1997 Erik Troan <ewt@redhat.com>
- built against glibc
