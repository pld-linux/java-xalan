#
# Conditional build:
%bcond_without	docs	# do not build documentation
#
# TODO:
#	- FIXME: xalan-interpretive needs org.w3c.dom.xpath, which is in included xml-commons-external only
#	- build with external xml-commons? (is there new version available?)
#
%define	_ver	%(echo %{version} | tr . _)
Summary:	XSLT processor for Java
Summary(pl):	Procesor XSLT napisany w Javie
Name:		xalan-j
Version:	2.7.0
Release:	1
License:	Apache v2.0
Group:		Applications/Publishing/XML/Java
Source0:	http://www.apache.org/dist/xml/xalan-j/source/%{name}_%{_ver}-src.tar.gz
# Source0-md5:	7859a78a5564cae42c933adcbbecdd01
URL:		http://xml.apache.org/xalan-j/
BuildRequires:	ant >= 1.5
BuildRequires:	jakarta-bcel
BuildRequires:	java_cup
BuildRequires:	jaxp_parser_impl
BuildRequires:	jdk >= 1.2
BuildRequires:	jlex
BuildRequires:	jpackage-utils
BuildRequires:	rpmbuild(macros) >= 1.300
# servlet provided by jakarta-servletapi.spec
# also resin.spec, resin-cmp.spec seem to provide it by simple grep.
BuildRequires:	servlet
Requires:	jaxp_parser_impl
Requires:	jre >= 1.2
Provides:	jaxp_transform_impl
BuildArch:	noarch
ExclusiveArch:	i586 i686 pentium3 pentium4 athlon %{x8664} noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
XSLT processor for Java.

%description -l pl
Procesor XSLT napisany w Javie.

%package javadoc
Summary:	API documentation for xalan-j, an XSLT processor for Java
Summary(pl):	Dokumentacja API dla xalan-j, procesora XSLT napisanego w Javie
Group:		Documentation
Requires:	jpackage-utils
Obsoletes:	xalan-j-doc

%description javadoc
API documentation for xalan-j, an XSLT processor for Java.

%description javadoc -l pl
Dokumentacja API dla xalan-j, procesora XSLT napisanego w Javie.

%package examples
Summary:	Xalan-j, an XSLT processor for Java examples
Summary(pl):	Przyk³ady dla xalan-j, procesora XSLT napisanego w Javie
Group:		Documentation

%description examples
Xalan-j, an XSLT processor for Java examples.

%description examples -l pl
Przyk³ady dla xalan-j, procesora XSLT napisanego w Javie.

%prep
%setup -q -n %{name}_%{_ver}

find . -name "*.jar" ! -name "xalan2jdoc.jar" ! -name "stylebook-1.0-b3_xalan-2.jar" -exec rm -f {} \;

%build
export JAVA_HOME=%{java_home}
export JAVAC=%{javac}
export JAVA=%{java}
required_jars='servlet java_cup java_cup-runtime jlex bcel jaxp_parser_impl'
export CLASSPATH="`/usr/bin/build-classpath $required_jars`"

# XXX: is it needed? other jars are not symlinked
ln -sf %{_javadir}/bcel.jar lib/BCEL.jar
ln -sf %{_javadir}/regexp.jar lib/regexp.jar
ln -sf %{_javadir}/java_cup-runtime.jar lib/runtime.jar

%ant xsltc.unbundledjar servlet %{?with_docs:docs xsltc.docs javadocs samples}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_examplesdir},%{_javadocdir}/%{name}-%{version}}

install build/xalan.jar $RPM_BUILD_ROOT%{_javadir}/xalan-%{version}.jar
install build/xsltc.jar $RPM_BUILD_ROOT%{_javadir}/xsltc-%{version}.jar
ln -sf xalan-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/xalan.jar
ln -sf xalan-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/jaxp_transform_impl.jar
ln -sf xsltc-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/xsltc.jar

%if %{with docs}
cp -r samples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r build/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar
%doc NOTICE %{?with_docs:build/docs/design build/docs/xsltc}

%if %{with docs}
%files javadoc
%defattr(644,root,root,755)
%doc %{_javadocdir}/%{name}-%{version}

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
%endif
