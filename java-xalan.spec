%define		ver	2.5.1
%define		_ver	%(echo %{ver} | tr . _)

Summary:	XSLT processor for Java
Summary(pl):	Procesor XSLT napisany w Javie
Name:		xalan-j
Version:	%{ver}
Release:	1
License:	Apache/W3C
Group:		Applications/Publishing/XML/Java
Source0:	http://xml.apache.org/dist/xalan-j/%{name}_%{_ver}-src.tar.gz
# Source0-md5:	a07c12bfb562ecfd9985c3b00ec06328
URL:		http://xml.apache.org/xalan-j/
BuildRequires:	jakarta-ant >= 1.5
BuildRequires:	jdk >= 1.2
BuildRequires:	xml-commons
BuildRequires:	jaxp_parser_impl
BuildRequires:	jakarta-bcel
BuildRequires:	servlet
BuildRequires:	jlex
BuildRequires:	java_cup
Requires:	jre >= 1.2
Requires:	jaxp_parser_impl
Provides:	jaxp_transform_impl
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_javalibdir	%{_datadir}/java

%description
XSLT processor for Java.

%description -l pl
Procesor XSLT napisany w Javie.

%prep
%setup -q -n xalan-j_%{_ver}
find . -name "*.jar" ! -name "xalan2jdoc.jar" ! -name "stylebook-1.0-b3_xalan-2.jar" -exec rm -f {} \;

%build
JAVA_HOME=%{_libdir}/java
CLASSPATH=%{_javalibdir}/servlet.jar
CLASSPATH=$CLASSPATH:%{_javalibdir}/java_cup.jar
CLASSPATH=$CLASSPATH:%{_javalibdir}/java_cup-runtime.jar
CLASSPATH=$CLASSPATH:%{_javalibdir}/jlex.jar
CLASSPATH=$CLASSPATH:%{_javalibdir}/bcel.jar
export JAVA_HOME CLASSPATH

ln -sf %{_javalibdir}/bcel.jar bin/BCEL.jar
ln -sf %{_javalibdir}/regexp.jar bin/regexp.jar
ln -sf %{_javalibdir}/java_cup-runtime.jar bin/runtime.jar
ant xsltc.unbundledjar docs xsltc.docs javadocs samples servlet

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javalibdir}

install build/{xalan,xsltc}.jar $RPM_BUILD_ROOT%{_javalibdir}
ln -sf xalan.jar $RPM_BUILD_ROOT%{_javalibdir}/xalan-%{version}.jar
ln -sf xalan.jar $RPM_BUILD_ROOT%{_javalibdir}/jaxp_transform_impl.jar
ln -sf xsltc.jar $RPM_BUILD_ROOT%{_javalibdir}/xsltc-%{version}.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc License build/docs/*
%{_javalibdir}/*.jar
