#
# Conditional build:
%bcond_without	doc	# do not build documentation
#
%define	srcname	xalan
%define	_ver	%(echo %{version} | tr . _)
Summary:	XSLT processor for Java
Summary(pl.UTF-8):	Procesor XSLT napisany w Javie
Name:		java-xalan
Version:	2.7.0
Release:	4
License:	Apache v2.0
Group:		Applications/Publishing/XML/Java
Source0:	http://www.apache.org/dist/xml/xalan-j/source/xalan-j_%{_ver}-src.tar.gz
# Source0-md5:	7859a78a5564cae42c933adcbbecdd01
Patch0:		xalan-j-javadoc-mem.patch
URL:		http://xml.apache.org/xalan-j/
BuildRequires:	ant >= 1.5
BuildRequires:	jakarta-bcel
BuildRequires:	java-gcj-compat-devel
BuildRequires:	java-xerces
BuildRequires:	java-xml-commons-external
BuildRequires:	java_cup
BuildRequires:	jlex
BuildRequires:	jpackage-utils
BuildRequires:	rpmbuild(macros) >= 1.300
# servlet provided by jakarta-servletapi.spec
# also resin.spec, resin-cmp.spec seem to provide it by simple grep.
# but we do want servlet implementation working with gnu java
BuildRequires:	java-servletapi5
Requires:	jaxp_parser_impl
Provides:	jaxp_transform_impl
Provides:	xalan-j
Obsoletes:	xalan-j
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
XSLT processor for Java.

%description -l pl.UTF-8
Procesor XSLT napisany w Javie.

%package javadoc
Summary:	API documentation for xalan-j, an XSLT processor for Java
Summary(pl.UTF-8):	Dokumentacja API dla xalan-j, procesora XSLT napisanego w Javie
Group:		Documentation
Requires:	jpackage-utils
Obsoletes:	xalan-j-doc
Obsoletes:	xalan-j-javadoc

%description javadoc
API documentation for xalan-j, an XSLT processor for Java.

%description javadoc -l pl.UTF-8
Dokumentacja API dla xalan-j, procesora XSLT napisanego w Javie.

%package examples
Summary:	Xalan-j, an XSLT processor for Java examples
Summary(pl.UTF-8):	Przykłady dla xalan-j, procesora XSLT napisanego w Javie
Group:		Documentation
Obsoletes:	xalan-j-examples

%description examples
Xalan-j, an XSLT processor for Java examples.

%description examples -l pl.UTF-8
Przykłady dla xalan-j, procesora XSLT napisanego w Javie.

%prep
%setup -q -n xalan-j_%{_ver}
%patch0 -p1

find . -name "*.jar" ! -name "xalan2jdoc.jar" ! -name "stylebook-1.0-b3_xalan-2.jar" -exec rm -f {} \;

# copied to xalan.jar (TODO: don't do it and use system ones?)
ln -sf %{_javadir}/bcel.jar lib/BCEL.jar
ln -sf %{_javadir}/regexp.jar lib/regexp.jar
ln -sf %{_javadir}/java_cup-runtime.jar lib/runtime.jar

%build
export JAVA_HOME=%{java_home}
export JAVAC=%{javac}
export JAVA=%{java}
required_jars='servlet java_cup java_cup-runtime jlex bcel jaxp_parser_impl xml-apis'
CLASSPATH=$(build-classpath $required_jars)
export CLASSPATH
export SHELL=/bin/sh

%ant -Dbuild.compiler=gcj \
	xsltc.unbundledjar servlet \
	%{?with_doc:docs xsltc.docs javadocs samples}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_examplesdir},%{_javadocdir}/%{srcname}-%{version}}

install build/serializer.jar $RPM_BUILD_ROOT%{_javadir}/serializer-%{version}.jar
install build/xalan.jar $RPM_BUILD_ROOT%{_javadir}/xalan-%{version}.jar
install build/xsltc.jar $RPM_BUILD_ROOT%{_javadir}/xsltc-%{version}.jar
ln -sf serializer-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/serializer.jar
ln -sf xalan-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/xalan.jar
ln -sf xalan-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/jaxp_transform_impl.jar
ln -sf xsltc-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/xsltc.jar

%if %{with doc}
cp -r samples $RPM_BUILD_ROOT%{_examplesdir}/%{srcname}-%{version}
cp -r build/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc %{?with_doc:build/docs/design build/docs/xsltc}
%{_javadir}/*.jar

%if %{with doc}
%files javadoc
%defattr(644,root,root,755)
%doc %{_javadocdir}/%{srcname}-%{version}

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{srcname}-%{version}
%endif
