Name:       libslp-lbsplugin-replay
Summary:    LBS Server plugin library for replay mode
Version:    0.2.2
Release:    1
Group:      Location/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    libslp-lbsplugin-replay.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(lbs-server-plugin)
BuildRequires:  pkgconfig(deviced)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
LBS Server plugin library for replay mode

%define DATADIR /etc/lbs-server

%prep
%setup -q
cp %{SOURCE1} .

%build
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DFULLVER=%{version} -DMAJORVER=${MAJORVER} \
        -DLIB_DIR=%{_libdir} \

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

mkdir -p %{buildroot}%{DATADIR}/replay
cp -a nmea-log/*.log %{buildroot}%{DATADIR}/replay

%post
rm -rf %{_libdir}/libSLP-lbs-plugin.so
ln -sf %{_libdir}/libSLP-lbs-plugin-replay.so %{_libdir}/libSLP-lbs-plugin.so
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest libslp-lbsplugin-replay.manifest
%defattr(-,root,root,-)
%{_libdir}/libSLP-lbs-plugin-replay.so*
%{DATADIR}/replay/*
