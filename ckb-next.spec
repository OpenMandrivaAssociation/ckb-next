Name:           ckb-next
Version:        0.4.2
Release:        1
Summary:        Corsair RGB keyboard driver for Linux and OS X
Group:          System/Configuration
License:        GPLv2 and BSD

URL:            https://github.com/ckb-next/ckb-next
Source0:        https://github.com/ckb-next/ckb-next/archive/v%{version}/%{name}-%{version}.tar.gz

# Upstream provides none of the following files
#Source1:        ckb-next.appdata.xml
Source2:        ckb-next.1
Source3:        99-ckb-next.preset

Patch0:         ckb-next-0.4.2-fix-daemon.patch

BuildRequires:  cmake
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5Network)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  quazip-devel
BuildRequires:  qmake5
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(udev)
BuildRequires:  pkgconfig(appindicator-0.1)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  desktop-file-utils
BuildRequires:  appstream-util
BuildRequires:  imagemagick

Obsoletes:      ckb

Requires(post):   rpm-helper >= %{rpmhelper_required_version}
Requires(preun):  rpm-helper >= %{rpmhelper_required_version}
Requires(postun): rpm-helper >= %{rpmhelper_required_version}

%description
ckb-next is an open-source driver for Corsair keyboards and mice. It aims to
bring the features of their proprietary CUE software to the Linux and Mac
operating systems. This project is currently a work in progress, but it already
supports much of the same functionality, including full RGB animations.

%files
%license LICENSE
%doc CHANGELOG.md FIRMWARE README.md README.install.urpmi
%{_bindir}/*
%{_libexecdir}/%{name}-*
%{_unitdir}/ckb-next-daemon.service
%{_presetdir}/99-ckb-next.preset
%{_datadir}/applications/ckb-next.desktop
#{_datadir}/appdata/ckb-next.appdata.xml
%{_iconsdir}/hicolor/*/apps/ckb-next.png
%{_mandir}/man1/*
%{_udevrulesdir}/*.rules
%{_libdir}/cmake/ckb-next

%prep
%setup -q -n %{name}-%{version}
%autopatch -p0

%build
# We force systemd since autodetection fail inside the buildsystem
%cmake -DCMAKE_BUILD_TYPE=Release \
       -DFORCE_INIT_SYSTEM=systemd \
       -DSAFE_INSTALL=OFF \
       -DSAFE_UNINSTALL=OFF \
       -DCMAKE_INSTALL_PREFIX=%{_prefix} \
       -DCMAKE_INSTALL_LIBEXECDIR=%{_libexecdir} \
       -DDISABLE_UPDATER=1 \
       -DUDEV_RULE_DIRECTORY=%{_udevrulesdir}

%make_build

%install
%make_install -C build
#__install -Dpm 0644 %{SOURCE1} %{buildroot}%{_datadir}/appdata/ckb-next.appdata.xml
%__install -Dpm 0644 %{SOURCE2} %{buildroot}%{_mandir}/man1/ckb-next.1
%__install -Dpm 0644 %{SOURCE3} %{buildroot}/%{_presetdir}/99-ckb-next.preset
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/ckb-next.appdata.xml

%post
%_post_service %{name}-daemon

%preun
%_preun_service %{name}-daemon

%postun
%systemd_postun_with_restart %{name}-daemon
