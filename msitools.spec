#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	vala		# Vala API
#
Summary:	MSI manipulation library and tools
Summary(pl.UTF-8):	Biblioteka i narzędzia do obróbki plików MSI
Name:		msitools
Version:	0.94
Release:	1
License:	LGPL v2.1+
Group:		Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/msitools/0.94/%{name}-%{version}.tar.xz
# Source0-md5:	76dec60217d3bfa44c744a6a55577a83
URL:		https://live.gnome.org/msitools
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake
BuildRequires:	gcab-devel >= 0.1.10
BuildRequires:	gettext-tools >= 0.18
BuildRequires:	glib2-devel >= 1:2.23.0
BuildRequires:	gobject-introspection-devel >= 0.9.4
BuildRequires:	intltool >= 0.35
BuildRequires:	libgsf-devel
BuildRequires:	libtool
BuildRequires:	libuuid-devel >= 1.41.3
BuildRequires:	libxml2-devel >= 1:2.7
BuildRequires:	tar >= 1:1.22
%{?with_vala:BuildRequires:	vala >= 2:0.16}
BuildRequires:	xz
Requires:	glib2 >= 1:2.23.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
msitools is a set of programs to inspect and build Windows Installer
(.MSI) files. It is based on libmsi, a portable library to read and
write .MSI files. libmsi in turn is a port of (and a subset of) Wine's
implementation of the Windows Installer.

%description -l pl.UTF-8
msitools to zbiór programów do badania i tworzenia plików Windows
Installera (.MSI). Jest oparty na libmsi - przenośnej bibliotece do
odczytu i zapisu plików .MSI. libmsi to z kolei port (podzbioru)
implementacji Windows Installera z WINE.

%package devel
Summary:	Header files for MSI library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki MSI
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.23.0

%description devel
Header files for MSI library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki MSI.

%package static
Summary:	Static MSI library
Summary(pl.UTF-8):	Statyczna biblioteka MSI
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static MSI library.

%description static -l pl.UTF-8
Statyczna biblioteka MSI.

%package -n vala-libmsi
Summary:	Vala API for MSI library
Summary(pl.UTF-8):	API języka Vala do biblioteki MSI
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.16

%description -n vala-libmsi
Vala API for MSI library.

%description -n vala-libmsi -l pl.UTF-8
API języka Vala do biblioteki MSI.

%package -n bash-completion-msitools
Summary:	Bash completion for MSI tools
Summary(pl.UTF-8):	Bashowe dopełnianie poleceń dla narzędzi MSI
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n bash-completion-msitools
Bash completion for MSI tools (msiinfo and msibuild).

%description -n bash-completion-msitools -l pl.UTF-8
Bashowe dopełnianie poleceń dla narzędzi MSI (msiinfo oraz msibuild).

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-fast-install \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmsi.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README TODO
%attr(755,root,root) %{_bindir}/msibuild
%attr(755,root,root) %{_bindir}/msidiff
%attr(755,root,root) %{_bindir}/msidump
%attr(755,root,root) %{_bindir}/msiextract
%attr(755,root,root) %{_bindir}/msiinfo
%attr(755,root,root) %{_bindir}/wixl
%attr(755,root,root) %{_bindir}/wixl-heat
%attr(755,root,root) %{_libdir}/libmsi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmsi.so.0
%{_libdir}/girepository-1.0/Libmsi-1.0.typelib
%{_datadir}/wixl-%{version}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmsi.so
%{_includedir}/libmsi-1.0
%{_datadir}/gir-1.0/Libmsi-1.0.gir
%{_pkgconfigdir}/libmsi-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmsi.a
%endif

%if %{with vala}
%files -n vala-libmsi
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libmsi-1.0.vapi
%endif

%files -n bash-completion-msitools
%defattr(644,root,root,755)
%{_datadir}/bash-completion/completions/msitools
