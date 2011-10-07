Summary:	Qt-based GUIs for unixODBC
Summary(pl.UTF-8):	Oparte na Qt graficzne interfejsy dla unixODBC
Name:		unixODBC-GUI-Qt
Version:	2.3.0
%define	snap	r92
Release:	0.%{snap}.1
License:	LGPL v2+ (libraries), GPL v2+ (applications)
Group:		X11/Applications
# svn co https://unixodbc-gui-qt.svn.sourceforge.net/svnroot/unixodbc-gui-qt
Source0:	%{name}-%{version}-%{snap}.tar.bz2
# Source0-md5:	102927d027e15dd7335eff9bed7213cd
Source1:	unixODBC.png
Source2:	ODBCDataManagerQ4.desktop
Source3:	ODBCManageDataSourcesQ4.desktop
Source4:	ODBCTestQ4.desktop
Patch0:		%{name}-qt4.patch
Patch1:		link.patch
URL:		http://sourceforge.net/projects/unixodbc-gui-qt/
BuildRequires:	QtGui-devel >= 4.0
BuildRequires:	QtNetwork-devel >= 4.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex
BuildRequires:	libltdl-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	qt4-build >= 4.0
BuildRequires:	readline-devel >= 4.2
BuildRequires:	unixODBC-devel >= 2.3.0
Requires:	unixODBC >= 2.3.0
Suggests:	qt4-assisant >= 4.0
Obsoletes:	unixODBC-qt
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Qt-based GUIs for unixODBC - libodbcinstQ plugin for libodbcinst
library and applications: DataManager, DataManagerII, ODBCConfig,
odbctest.

%description -l pl.UTF-8
Oparte na Qt graficzne interfejsy użytkownika do unixODBC - wtyczka
libodbcinstQ dla biblioteki libodbcinst oraz aplikacje: DataManager,
DataManagerII, ODBCConfig, odbctest.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-static \
	--enable-ltdllib \
	--with-qt-dir-bin=%{_libdir}/qt4/bin \
	--with-qt-dir-include=/usr/include/qt4 \
	--with-qt-dir-lib=%{_libdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# libodbcinstQ.so.1 is lt_dlopened
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib{gtrtstQ4,odbcinstQ4}.la

install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}
install %{SOURCE1} $RPM_BUILD_ROOT%{_pixmapsdir}
# acc. to README ODBCDataManagerQ4 is not done yet
#install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE3} %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/ODBCCreateDataSourceQ4
%attr(755,root,root) %{_bindir}/ODBCManageDataSourcesQ4
%attr(755,root,root) %{_bindir}/ODBCTestQ4
%attr(755,root,root) %{_libdir}/libgtrtstQ4.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgtrtstQ4.so.1
%attr(755,root,root) %{_libdir}/libodbcinstQ4.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libodbcinstQ4.so.1
# for dlopen
%attr(755,root,root) %{_libdir}/libgtrtstQ4.so
%attr(755,root,root) %{_libdir}/libodbcinstQ4.so
%{_pixmapsdir}/unixODBC.png
%{_desktopdir}/ODBCTestQ4.desktop
%{_desktopdir}/ODBCManageDataSourcesQ4.desktop
