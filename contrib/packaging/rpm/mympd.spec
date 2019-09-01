#
# spec file for package myMPD
#
# (c) 2018-2019 Juergen Mang <mail@jcgames.de>

Name:           mympd
Version:        5.6.0
Release:        0 
License:        GPLv2
Group:          Productivity/Multimedia/Sound/Players
Summary:        Standalone web mpdclient
Url:            https://github.com/jcorporation/myMPD
Source:         mympd_%{version}.orig.tar.gz
BuildRequires:  gcc
BuildRequires:	gcc-c++
BuildRequires:  cmake
BuildRequires:  unzip
BuildRequires:	libmpdclient-devel
BuildRequires:	pkgconfig
BuildRequires:	openssl-devel
BuildRequires:  libmediainfo-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%global debug_package %{nil}

%description 
myMPD is a standalone and mobile friendly web mpdclient.

%prep 
%setup -q -n %{name}-%{version}

%build
mkdir release
cd release || exit 1
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_BUILD_TYPE=RELEASE ..
make

%install
cd release || exit 1
make install DESTDIR=%{buildroot}

%post
echo "Checking status of mympd system user and group"
getent group mympd > /dev/null
[ "$?" = "2" ] && groupadd -r mympd
getent passwd mympd > /dev/null
[ "$?" = "2" ] && useradd -r mympd -g mympd -d /var/lib/mympd -s /usr/sbin/nologin

%postun
if [ "$1" = "0" ]
then
  echo "Please purge /var/lib/mympd manually"
fi

%files 
%defattr(-,root,root,-)
%doc README.md LICENSE
/usr/bin/mympd
/usr/share/mympd
/usr/lib/mympd
/usr/lib/systemd/system/mympd.service
%config(noreplace) /etc/mympd.conf

%changelog
* Sun Sep 01 2019 Juergen Mang <mail@jcgames.de> 5.6.0-0
- Version from master
