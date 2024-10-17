%define api %(echo %{version} |cut -d. -f1)
%define major %api
%define beta %{nil}

%define qtwebglplugin %mklibname qt%{api}webglplugin %{major}
%define qtwebglplugind %mklibname qt%{api}webglplugin -d

%define _qt5_prefix %{_libdir}/qt%{api}

Name:		qt5-qtwebglplugin
Version:	5.15.15
%if "%{beta}" != ""
Release:	0.%{beta}.1
%define qttarballdir qtwebglplugin-everywhere-src-%{version}-%{beta}
Source0:	http://download.qt.io/development_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}-%{beta}/submodules/%{qttarballdir}.tar.xz
%else
Release:	1
%define qttarballdir qtwebglplugin-everywhere-opensource-src-%{version}
Source0:	http://download.qt.io/official_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}/submodules/%{qttarballdir}.tar.xz
%endif
# From KDE
# [currently no patches]
Summary:	WebGL platform plugin for Qt Quick applications
Group:		Development/KDE and Qt
License:	GPLv3
URL:		https://www.qt.io
BuildRequires:	qmake5
BuildRequires:	pkgconfig(Qt5Core) >= %{version}
BuildRequires:	pkgconfig(Qt5DBus) >= %{version}
BuildRequires:	pkgconfig(Qt5Quick) >= %{version}
BuildRequires:	pkgconfig(Qt5OpenGL) >= %{version}
BuildRequires:	pkgconfig(Qt5WebSockets) >= %{version}
BuildRequires:	pkgconfig(Qt5Gui) >= %{version}
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	%mklibname -d -s qt5fontdatabasesupport
BuildRequires:	%mklibname -d -s qt5eventdispatchersupport
BuildRequires:	%mklibname -d -s qt5themesupport
# For the Provides: generator
BuildRequires:	cmake >= 3.11.0-1

%description
The Qt Quick WebGL is a platform plugin that allows for single-user remote
access by streaming Qt Quick user interfaces over the network.

The UI is rendered in a WebGL™-enabled client browser.

%files
%_qt5_prefix/plugins/platforms/libqwebgl.so

#------------------------------------------------------------------------------

%package -n	%{qtwebglplugind}
Summary:	Devel files needed to build apps based on %name
Group:		Development/KDE and Qt
Requires:	%{name} = %{version}

%description -n %{qtwebglplugind}
Devel files needed to build apps based on %{name}.

%files -n %{qtwebglplugind}
%{_qt5_libdir}/cmake/Qt5Gui/*.cmake

#------------------------------------------------------------------------------

%prep
%autosetup -n %(echo %qttarballdir|sed -e 's,-opensource,,') -p1
%{_libdir}/qt5/bin/syncqt.pl -version %{version}

%build
%qmake_qt5
%make_build

#------------------------------------------------------------------------------
%install
%make_install INSTALL_ROOT=%{buildroot}
