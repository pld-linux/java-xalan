
%define	major	2
%define	minor	2
%define	micro	0
%define	ver		%{major}_%{minor}

Summary:	XSLT processor for Java
Summary(pl):	Procesor XSLT napisany w Javie
Name:		xalan-j
Version:	%{major}.%{minor}
Release:	3
License:	Apache Software License
Group:		Applications/Publishing/XML/Java
Group(de):	Applikationen/Publizieren/XML/Java
Group(es):	Aplicaciones/Editoración/XML/Java
Group(pl):	Aplikacje/Publikowanie/XML/Java
Group(pt_BR):	Aplicações/Editoração/XML/Java
URL:		http://xml.apache.org/xalan-j
Source0:	http://xml.apache.org/xalan-j/dist/%{name}_%{ver}-src.tar.gz
Patch0:		xalan-build.patch
BuildRequires:	jdk
BuildRequires:	xerces-j >= 1.4.4-2
Requires:	jre
Requires:	xerces-j >= 1.4.4-2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_javaclassdir	%{_libdir}/java/
%define		jredir			%{_libdir}/java-sdk/jre/lib

%description
XSLT processor for Java.

%description -l pl
Procesor XSLT napisany w Javie.

%prep
%setup -q -n xalan-j_%{major}_%{minor}_%{micro}
%patch0 -p1

mv build.sh build.sh.dos
sed 's/
$//' < build.sh.dos > build.sh

%build
JAVA_HOME=%{_libdir}/java-sdk
export JAVA_HOME

ANT_OPTS=-O
export ANT_OPTS

sh build.sh docs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javaclassdir}

install bin/xml-apis.jar $RPM_BUILD_ROOT%{_javaclassdir}
install build/xalan.jar $RPM_BUILD_ROOT%{_javaclassdir}

gzip -9nf readme.html License

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {readme.html,License}.gz build/docs/*
%{_javaclassdir}/*.jar
