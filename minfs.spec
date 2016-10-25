%define		tag	RELEASE.2016-10-04T19-44-43Z
%define		subver	%(echo %{tag} | sed -e 's/[^0-9]//g')
# git fetch https://github.com/minio/minfs.git refs/tags/RELEASE.2016-10-04T19-44-43Z
# git rev-list -n 1 FETCH_HEAD
%define     commitid c88fb0f2eda862b424347728c9bfc00dc17c33c1
Summary:	MinFS is a fuse driver
Name:		minfs
Version:	0.0.%{subver}
Release:	1
License:	Apache v2.0
Group:		Development/Building
Source0:	https://github.com/minio/minfs/archive/%{tag}.tar.gz
# Source0-md5:	9e5ef301294132f7675644ea5381197a
BuildRequires:	golang >= 1.6
ExclusiveArch:	%{ix86} %{x8664} %{arm}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

## Disable debug packages.
%define		_enable_debug_packages 0

## Go related tags.
%define		gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%define		gopath		%{_libdir}/golang
%define		import_path	github.com/minio/minfs

%description
MinFS is a fuse driver for Amazon S3 compatible object storage server.
Use it to store photos, videos, VMs, containers, log files, or any
blob of data as objects on your object storage server.

%prep
%setup -qc
mv %{name}-*/* .

install -d src/$(dirname %{import_path})
ln -s ../../.. src/%{import_path}

%build
export GOPATH=$(pwd)

# setup flags like 'go run buildscripts/gen-ldflags.go' would do
tag=%{tag}
version=${tag#RELEASE.}
commitid=%{commitid}
scommitid=$(echo $commitid | cut -c1-12)
prefix=%{import_path}/cmd

LDFLAGS="
-X $prefix.Version=$version
-X $prefix.ReleaseTag=$tag
-X $prefix.CommitID=$commitid
-X $prefix.ShortCommitID=$scommitid
"

%gobuild -o %{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/%{name}/db}
install -p %{name} $RPM_BUILD_ROOT%{_sbindir}
install -p mount.minfs $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.md
%attr(755,root,root) %{_sbindir}/minfs
%attr(755,root,root) %{_sbindir}/mount.minfs
