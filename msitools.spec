#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	vala		# Vala API

Summary:	MSI manipulation library and tools
Summary(pl.UTF-8):	Biblioteka i narzędzia do obróbki plików MSI
Name:		msitools
Version:	0.102
Release:	1
License:	LGPL v2.1+
Group:		Applications/File
Source0:	https://download.gnome.org/sources/msitools/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	c773d25de403fefa896613ab26b59c84
URL:		https://wiki.gnome.org/msitools
BuildRequires:	bison
BuildRequires:	gcab-devel >= 0.1.10
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.23.0
BuildRequires:	gobject-introspection-devel >= 0.9.4
BuildRequires:	libgsf-devel
BuildRequires:	libxml2-devel >= 1:2.7
BuildRequires:	meson >= 0.52
BuildRequires:	ninja >= 1.5
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 2:0.16
BuildRequires:	vala-gcab >= 0.1.10
BuildRequires:	xz
Requires:	gcab >= 0.1.10
Requires:	glib2 >= 1:2.23.0
Requires:	libxml2 >= 1:2.7
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
BuildArch:	noarch

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
BuildArch:	noarch

%description -n bash-completion-msitools
Bash completion for MSI tools (msiinfo and msibuild).

%description -n bash-completion-msitools -l pl.UTF-8
Bashowe dopełnianie poleceń dla narzędzi MSI (msiinfo oraz msibuild).

%prep
%setup -q

%if %{with static_libs}
%{__sed} -i '/^libmsi =/ s/shared_library/library/' libmsi/meson.build
%endif

%{__sed} -i -e '1s,/usr/bin/env bash,/bin/bash,' tools/{msidiff,msidump}.in

%build
%meson build

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md TODO
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
%{_datadir}/vala/vapi/libmsi-1.0.deps
%{_datadir}/vala/vapi/libmsi-1.0.vapi
%endif

%files -n bash-completion-msitools
%defattr(644,root,root,755)
%{bash_compdir}/msitools
