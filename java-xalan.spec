
# Conditional builds
# - with jdk14 - build with jdk 1.4.x and up

Summary:	XSLT processor for Java
Summary(pl):	Procesor XSLT napisany w Javie
Name:		xalan-j
Version:	2.5.D1
%define	ver	%(echo %{version} | tr . _)
Release:	2
License:	Apache/W3C
Group:		Applications/Publishing/XML/Java
Source0:	http://xml.apache.org/xalan-j/dist/%{name}_%{ver}-src.tar.gz
# Source0-md5:	9fb00330484d6d7936eaede035c9156e
Patch0:		%{name}-build.patch
URL:		http://xml.apache.org/xalan-j/
BuildRequires:	jakarta-ant >= 1.4.1
BuildRequires:	jdk >= 1.2
Requires:	jre >= 1.2

%if %{!?_with_jdk14:1}%{?_with_jdk14:0}
BuildRequires:	xerces-j >= 1.4.4-2
Requires:	xerces-j >= 1.4.4-2
%endif

BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_javaclassdir	%{_datadir}/java/

%description
XSLT processor for Java.

%description -l pl
Procesor XSLT napisany w Javie.

%prep
%setup -q -n xalan-j_%{ver}
#%patch -p1

mv build.sh build.sh.dos
sed 's/
$//' < build.sh.dos > build.sh

%build
JAVA_HOME=%{_libdir}/java
ANT_OPTS=-O

%if %{!?_with_jdk14:1}%{?_with_jdk14:0}
PARSER_JAR=/usr/share/java/xerces.jar
export JAVA_HOME ANT_OPTS PARSER_JAR
%else
export JAVA_HOME ANT_OPTS
%endif

sh build.sh docs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javaclassdir}

%if %{!?_with_jdk14:1}%{?_with_jdk14:0}
install bin/xml-apis.jar $RPM_BUILD_ROOT%{_javaclassdir}
%endif
install build/xalan.jar $RPM_BUILD_ROOT%{_javaclassdir}/xalan-%{version}.jar
ln -sf xalan-%{version}.jar $RPM_BUILD_ROOT%{_javaclassdir}/xalan.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc License build/docs/*
%{_javaclassdir}/*.jar
