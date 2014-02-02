Summary:	LDAP libraries
Name:		openldap
Version:	2.4.39
Release:	1
License:	OpenLDAP Public License
Group:		Networking/Daemons
Source0:	ftp://ftp.openldap.org/pub/OpenLDAP/openldap-release/%{name}-%{version}.tgz
# Source0-md5:	b0d5ee4b252c841dec6b332d679cf943
URL:		http://www.openldap.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	db-devel
BuildRequires:	libltdl-devel
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	readline-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LDAP shared libraries.

%package devel
Summary:	LDAP development files
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files and libraries for developing applications that use LDAP.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
CPPFLAGS="-I/usr/include/ncurses -D_GNU_SOURCE"
%configure \
	--enable-backends=no	\
	--enable-dynamic	\
	--enable-ipv6		\
	--enable-local		\
	--enable-slapd=no	\
	--enable-static=no	\
	--with-readline		\
	--with-threads		\
	--with-tls		\
	--with-yielding-select

%{__make} -j1 depend
%{__make}

%{__rm} doc/rfc/rfc*

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/openldap/{*.default,ldap.conf}
%{__rm} -r $RPM_BUILD_ROOT%{_bindir}
%{__rm} -r $RPM_BUILD_ROOT%{_mandir}/man{1,5,8}

chmod +x $RPM_BUILD_ROOT%{_libdir}/*

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ANNOUNCEMENT CHANGES COPYRIGHT README LICENSE
%attr(755,root,root) %ghost %{_libdir}/liblber-2.4.so.?
%attr(755,root,root) %ghost %{_libdir}/libldap-2.4.so.?
%attr(755,root,root) %ghost %{_libdir}/libldap_r-2.4.so.?
%attr(755,root,root) %{_libdir}/liblber-2.4.so.*.*.*
%attr(755,root,root) %{_libdir}/libldap-2.4.so.*.*.*
%attr(755,root,root) %{_libdir}/libldap_r-2.4.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblber.so
%attr(755,root,root) %{_libdir}/libldap.so
%attr(755,root,root) %{_libdir}/libldap_r.so
%{_libdir}/liblber.la
%{_libdir}/libldap.la
%{_libdir}/libldap_r.la
%{_includedir}/*.h
%{_mandir}/man3/*

