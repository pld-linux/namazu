Summary:	Namazu is a full-text search engine
Summary(pl):	Namazu - silnik pe³notekstowego przeszukiwania
Name:		namazu
Version:	2.0.10
Release:	1
License:	GPL
Group:		Applications/Text
Source0:	http://www.namazu.org/stable/%{name}-%{version}.tar.gz
# Source0-md5:	85892f930e5ef694f39469f136f484b4
Patch0:		%{name}-2.0.5-linguas.patch
Patch1:		%{name}-2.0.6-newgettext3.patch
URL:		http://www.namazu.org/
BuildRequires:	autoconf
BuildRequires:	perl >= 5.6.0
BuildRequires:	perl-NKF >= 1.70
BuildRequires:	perl-Text-Kakasi >= 1.00
Requires:	kakasi >= 2.3.0
Requires:	perl >= 5.6.0
Requires:	perl-File-MMagic >= 1.12
Requires:	perl-NKF >= 1.70
Requires:	perl-Text-Kakasi >= 1.00
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# XXX is this right - it was /var/lib before FHS macros
%define _localstatedir	/var/lib
%define _libexecdir	/home/services/httpd/cgi-bin

%description
Namazu is a full-text search engine software intended for easy use.
Not only it works as CGI program for small or medium scale WWW search
engine, but also works as personal use such as search system for local
HDD.

%description -l pl
Namazu to silnik pe³notekstowego przeszukiwania zrobiony z my¶l± o
³atwym u¿ytkowaniu. Dzia³a nie tylko jako program CGI dla ma³ych i
¶rednich wyszukiwarek WWW, ale tak¿e jako prywatny system
przeszukiwania dla lokalnego dysku.

%package devel
Summary:	Libraries and include files of Namazu
Summary(pl):	Biblioteki i pliki nag³ówkowe Namazu
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Libraries and include files of Namazu.

%description devel -l pl
Biblioteki i pliki nag³ówkowe Namazu.

%package cgi
Summary:	A CGI interface for Namazu
Summary(pl):	Interfejs CGI do Namazu
Group:		Applications/Text
Requires:	%{name} = %{version}
Requires:	webserver

%description cgi
A CGI interface for Namazu.

%description cgi -l pl
Interfejs CGI do Namazu.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
autoconf
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

mv -f $RPM_BUILD_ROOT%{_sysconfdir}/namazu/namazurc-sample \
	$RPM_BUILD_ROOT%{_sysconfdir}/namazu/namazurc
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/namazu/mknmzrc-sample \
	$RPM_BUILD_ROOT%{_sysconfdir}/namazu/mknmzrc
chmod a+rw -R $RPM_BUILD_ROOT%{_localstatedir}/namazu
chmod a+rw -R $RPM_BUILD_ROOT%{_localstatedir}/namazu/index

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

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
