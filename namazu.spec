Summary:	Namazu - a full-text search engine
Summary(pl.UTF-8):	Namazu - silnik pełnotekstowego przeszukiwania
Name:		namazu
Version:	2.0.13
Release:	6
License:	GPL
Group:		Applications/Text
Source0:	http://www.namazu.org/stable/%{name}-%{version}-1.tar.gz
# Source0-md5:	335ef8f4faecae4a30954f50af356ac0
Source1:	http://mm.tkikuchi.net/pipermail.pl
# Source1-md5:	d49f69f964d193a7aeb2cf11edf63a69
Patch0:		%{name}-linguas.patch
Patch1:		%{name}-newgettext3.patch
Patch2:		%{name}-emailaddress.patch
Patch3:		%{name}-fixinutf8.patch
Patch4:		%{name}-de.patch
URL:		http://www.namazu.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-tools
BuildRequires:	libtool
BuildRequires:	perl-File-MMagic >= 1.12
BuildRequires:	perl-NKF >= 1.71
BuildRequires:	perl-Text-ChaSen >= 1.03
BuildRequires:	perl-Text-Kakasi >= 1.00
BuildRequires:	perl-modules >= 5.6.0
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	kakasi >= 2.3.0
Requires:	perl-File-MMagic >= 1.12
Requires:	perl-NKF >= 1.71
Requires:	perl-Text-ChaSen >= 1.03
Requires:	perl-Text-Kakasi >= 1.00
Requires:	perl-modules >= 5.6.0
Conflicts:	mknmz-wwwoffle = 0.7.2-1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# XXX is this right - it was /var/lib before FHS macros
%define		_localstatedir	/var/lib
%define		_cgidir		%{_libexecdir}/%{name}

%description
Namazu is a full-text search engine software intended for easy use.
Not only it works as CGI program for small or medium scale WWW search
engine, but also works as personal use such as search system for local
HDD.

%description -l pl.UTF-8
Namazu to silnik pełnotekstowego przeszukiwania zrobiony z myślą o
łatwym użytkowaniu. Działa nie tylko jako program CGI dla małych i
średnich wyszukiwarek WWW, ale także jako prywatny system
przeszukiwania dla lokalnego dysku.

%package devel
Summary:	Header files for Namazu
Summary(pl.UTF-8):	Pliki nagłówkowe Namazu
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Namazu.

%description devel -l pl.UTF-8
Pliki nagłówkowe Namazu.

%package static
Summary:	Static Namazu library
Summary(pl.UTF-8):	Statyczna biblioteka Namazu
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Namazu library.

%description static -l pl.UTF-8
Statyczna biblioteka Namazu.

%package cgi
Summary:	A CGI interface for Namazu
Summary(pl.UTF-8):	Interfejs CGI do Namazu
Group:		Applications/Text
Requires:	%{name} = %{version}-%{release}

%description cgi
A CGI interface for Namazu.

%description cgi -l pl.UTF-8
Interfejs CGI do Namazu.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
rm -rf File-MMagic
%{__gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libexecdir}/%{name}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/%{name}/filter/pipermail.pl

mv -f $RPM_BUILD_ROOT%{_sysconfdir}/namazu/namazurc-sample \
	$RPM_BUILD_ROOT%{_sysconfdir}/namazu/namazurc
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/namazu/mknmzrc-sample \
	$RPM_BUILD_ROOT%{_sysconfdir}/namazu/mknmzrc

mv -f $RPM_BUILD_ROOT%{_libexecdir}/%{name}.cgi \
	$RPM_BUILD_ROOT%{_libexecdir}/%{name}/%{name}.cgi

install -d html
mv -f $RPM_BUILD_ROOT%{_datadir}/%{name}/doc/* html/
rm -fr $RPM_BUILD_ROOT%{_datadir}/%{name}/etc

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog* NEWS README THANKS TODO
%doc etc/namazu.png html
%lang(es) %doc README-es
%lang(ja) %doc README-ja
%attr(755,root,root) %{_bindir}/namazu
%attr(755,root,root) %{_bindir}/bnamazu
%attr(755,root,root) %{_bindir}/*nmz
%attr(755,root,root) %{_bindir}/mailutime
%attr(755,root,root) %{_bindir}/nmzgrep
%attr(755,root,root) %{_bindir}/nmzmerge
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnmz.so.7
%dir %{_sysconfdir}/namazu
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/namazu/namazurc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/namazu/mknmzrc
%{_mandir}/man1/*
%dir %{_datadir}/namazu
%{_datadir}/namazu/filter
%{_datadir}/namazu/pl
%{_datadir}/namazu/template
%dir %{_localstatedir}/namazu
%dir %{_localstatedir}/namazu/index

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nmz-config
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/namazu

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files cgi
%defattr(644,root,root,755)
%attr(755,root,root) %{_cgidir}
