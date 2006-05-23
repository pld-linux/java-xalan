#
# TODO: without_docs bcond; generating takes ages
#
%include	/usr/lib/rpm/macros.java
Summary:	XSLT processor for Java
Summary(pl):	Procesor XSLT napisany w Javie
Name:		xalan-j
Version:	2.6.0
%define	_ver	%(echo %{version} | tr . _)
Release:	2
License:	Apache License v2.0
Group:		Applications/Publishing/XML/Java
Source0:	http://www.apache.org/dist/xml/xalan-j/source/%{name}_%{_ver}-src.tar.gz
# Source0-md5:	a210f7108e680ab60a11977ec99ab1f9
Patch0:		%{name}-dom3.patch
URL:		http://xml.apache.org/xalan-j/
BuildRequires:	ant >= 1.5
BuildRequires:	jdk >= 1.2
BuildRequires:	xml-commons
BuildRequires:	jaxp_parser_impl
BuildRequires:	jakarta-bcel
# servlet provided by jakarta-servletapi.spec
# also resin.spec, resin-cmp.spec seem to provide it by simple grep.
BuildRequires:	servlet
BuildRequires:	jlex
BuildRequires:	java_cup
Requires:	jre >= 1.2
Requires:	jaxp_parser_impl
Provides:	jaxp_transform_impl
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
XSLT processor for Java.

%description -l pl
Procesor XSLT napisany w Javie.

%package doc
Summary:	Documentation for xalan-j, an XSLT processor for Java
Group:		Documentation

%description doc
Documentation for xalan-j, an XSLT processor for Java.

%description doc -l pl
Dokumentacja dla xalan-j, procesora XSLT napisanego w Javie.

%prep
%setup -q -n xalan-j_%{_ver}
%patch0 -p1

find . -name "*.jar" ! -name "xalan2jdoc.jar" ! -name "stylebook-1.0-b3_xalan-2.jar" -exec rm -f {} \;

%build
required_jars='servlet java_cup java_cup-runtime jlex bcel jaxp_parser_impl'
export CLASSPATH="`/usr/bin/build-classpath $required_jars`"
export JAVA_HOME=%{java_home}
export JAVAC=%{javac}
export JAVA=%{java}

ln -sf %{_javadir}/bcel.jar bin/BCEL.jar
ln -sf %{_javadir}/regexp.jar bin/regexp.jar
ln -sf %{_javadir}/java_cup-runtime.jar bin/runtime.jar
%{ant} xsltc.unbundledjar docs xsltc.docs javadocs samples servlet

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_examplesdir}}

install build/{xalan,xsltc}.jar $RPM_BUILD_ROOT%{_javadir}
ln -sf xalan.jar $RPM_BUILD_ROOT%{_javadir}/xalan-%{version}.jar
ln -sf xalan.jar $RPM_BUILD_ROOT%{_javadir}/jaxp_transform_impl.jar
ln -sf xsltc.jar $RPM_BUILD_ROOT%{_javadir}/xsltc-%{version}.jar

cp -r samples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar
%doc NOTICE

%files doc
%defattr(644,root,root,755)
%doc build/docs/*
%{_examplesdir}/%{name}-%{version}
