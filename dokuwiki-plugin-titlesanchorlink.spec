%define		subver	2013-03-01
%define		ver		%(echo %{subver} | tr -d -)
%define		plugin		titlesanchorlink
%define		php_min_version 5.0.0
Summary:	DokuWiki TitlesAnchorLink Plugin
Name:		dokuwiki-plugin-%{plugin}
Version:	%{ver}
Release:	2
License:	GPL v2
Group:		Applications/WWW
Source0:	https://github.com/Dric/dokuwiki-titlesanchorlink/archive/3ca9927/%{plugin}-%{subver}.tar.gz
# Source0-md5:	2ac066f5186ca085fc3e9e3193211398
Patch0:		heading-link.patch
URL:		https://www.dokuwiki.org/plugin:titlesanchorlink
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	dokuwiki >= 20131208
Requires:	php(core) >= %{php_min_version}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}

%description
Displays Anchors links when hovering DokuWiki Sections titles, in a
similar way to Github.

%prep
%setup -qc
mv *-%{plugin}-*/* .
%patch0 -p1

%build
version=$(awk '/^date/{print $2}' plugin.info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
%{__rm} $RPM_BUILD_ROOT%{plugindir}/README.md

%clean
rm -rf $RPM_BUILD_ROOT

%post
# force js/css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files
%defattr(644,root,root,755)
%doc README.md
%dir %{plugindir}
%{plugindir}/*.css
%{plugindir}/*.js
%{plugindir}/*.php
%{plugindir}/*.txt
%{plugindir}/images
