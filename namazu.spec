# XXX is this right - it was /var/lib before FHS macros
%define _localstatedir	/var/lib
%define _libexecdir	/home/httpd/cgi-bin

Summary:	Namazu is a full-text search engine
Name:		namazu
Version:	2.0.10
Release:	1
License:	GPL
Group:		Applications/Text
BuildRequires:	perl >= 5.6.0, perl-NKF >= 1.70, perl-Text-Kakasi >= 1.00
Requires:	perl >= 5.6.0, perl-File-MMagic >= 1.12, perl-NKF >= 1.70
Requires:	kakasi >= 2.3.0, perl-Text-Kakasi >= 1.00
Source0:	http://www.namazu.org/stable/%{name}-%{version}.tar.gz
Patch0:		%{name}-2.0.5-linguas.patch
Patch1:		%{name}-2.0.6-newgettext3.patch
URL:		http://www.namazu.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Namazu is a full-text search engine software intended for easy use.
Not only it works as CGI program for small or medium scale WWW search
engine, but also works as personal use such as search system for local
HDD.

%package devel
Summary:	Libraries and include files of Namazu
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Libraries and include files of Namazu.

%package cgi
Summary:	a CGI interface for Namazu
Group:		Applications/Text
Requires:	%{name} = %{version}
Requires:	webserver

%description cgi
A CGI interface for Namazu.

%prep

%setup -q
%patch0 -p1 -b .linguas
%patch1 -p1 -b .newgettext

%build
autoconf
%configure

if [ "$SMP" != "" ]; then
  make -j$SMP "MAKE=make -j$SMP"
else
  make
fi

%install
rm -rf $RPM_BUILD_ROOT
rm -rf %{buildroot}
%makeinstall

mv %{buildroot}%{_sysconfdir}/namazu/namazurc-sample \
	%{buildroot}%{_sysconfdir}/namazu/namazurc
mv %{buildroot}%{_sysconfdir}/namazu/mknmzrc-sample \
	%{buildroot}%{_sysconfdir}/namazu/mknmzrc
chmod a+rw -R %{buildroot}%{_localstatedir}/namazu
chmod a+rw -R %{buildroot}%{_localstatedir}/namazu/index

%find_lang %{name}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog ChangeLog.1 CREDITS COPYING HACKING HACKING-ja
%doc INSTALL INSTALL-ja README README-es README-ja NEWS THANKS TODO
%doc etc/namazu.png
%config %{_sysconfdir}/namazu/*
%attr(755,root,root) %{_bindir}/namazu
%attr(755,root,root) %{_bindir}/bnamazu
%attr(755,root,root) %{_bindir}/*nmz
%attr(755,root,root) %{_bindir}/mailutime
%attr(755,root,root) %{_bindir}/nmzgrep
%attr(755,root,root) %{_bindir}/nmzmerge
%{_libdir}/*.so.*
%{_mandir}/man1/*
%{_datadir}/namazu/doc/*
%{_datadir}/namazu/filter/*
%{_datadir}/namazu/pl/*
%{_datadir}/namazu/template/*
%dir %{_localstatedir}/namazu
%dir %{_localstatedir}/namazu/index

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nmz-config
%{_includedir}/namazu/*.h
%{_libdir}/*.so
%{_libdir}/*a

%files cgi
%defattr(644,root,root,755)
%{_libexecdir}/namazu.cgi
