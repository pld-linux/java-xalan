#
# Conditional build:
%bcond_without	doc	# do not build documentation
%bcond_without	servlet	# don't build servlet sample

%define		ver	%(echo %{version} | tr . _)
%define		srcname	xalan
%include	/usr/lib/rpm/macros.java
Summary:	XSLT processor for Java
Summary(pl.UTF-8):	Procesor XSLT napisany w Javie
Name:		java-xalan
Version:	2.7.1
Release:	5
License:	Apache v2.0
Group:		Applications/Publishing/XML/Java
Source0:	http://www.apache.org/dist/xml/xalan-j/source/xalan-j_%{ver}-src.tar.gz
# Source0-md5:	fc805051f0fe505c7a4b1b5c8db9b9e3
Patch0:		xalan-j-javadoc-mem.patch
URL:		http://xml.apache.org/xalan-j/
BuildRequires:	ant >= 1.5
BuildRequires:	java(jaxp_parser_impl)
%{?with_servlet:BuildRequires:	java(servlet)}
BuildRequires:	java-bcel
BuildRequires:	java-cup
BuildRequires:	java-xml-commons-external
BuildRequires:	jdk
BuildRequires:	jlex
BuildRequires:	jpackage-utils
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	java(jaxp_parser_impl)
Provides:	java(jaxp_transform_impl)
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
%setup -q -n xalan-j_%{ver}
%{__sed} -i -e 's,\r$,,' build.xml
%patch0 -p1

find -name '*.jar' ! -name 'xalan2jdoc.jar' ! -name 'stylebook-1.0-b3_xalan-2.jar' | xargs rm -f

# copied to xalan.jar (TODO: don't do it and use system ones?)
ln -sf %{_javadir}/bcel.jar lib/BCEL.jar
ln -sf %{_javadir}/regexp.jar lib/regexp.jar
ln -sf %{_javadir}/cup-runtime.jar lib/runtime.jar

%build
export JAVA_HOME=%{java_home}
export JAVAC=%{javac}
export JAVA=%{java}
required_jars='%{?with_servlet:servlet-api} cup cup-runtime jlex bcel jaxp_parser_impl xml-apis'
CLASSPATH=$(build-classpath $required_jars)
export CLASSPATH
export ANT_OPTS="-Xmx192m"

%ant xsltc.unbundledjar %{?with_servlet:servlet} \
	%{?with_doc:docs xsltc.docs javadocs samples}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_examplesdir},%{_javadocdir}/%{srcname}-%{version}}

cp -p build/serializer.jar $RPM_BUILD_ROOT%{_javadir}/xalan-serializer-%{version}.jar
cp -p build/xalan.jar $RPM_BUILD_ROOT%{_javadir}/xalan-%{version}.jar
cp -p build/xsltc.jar $RPM_BUILD_ROOT%{_javadir}/xsltc-%{version}.jar
ln -sf xalan-serializer-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/xalan-serializer.jar
ln -sf xalan-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/xalan.jar
ln -sf xalan-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/jaxp_transform_impl.jar
ln -sf xsltc-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/xsltc.jar

# some expected jar names from JPackage
ln -sf xalan-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/xalan-j2.jar
ln -sf xalan-serializer-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/xalan-j2-serializer.jar

%if %{with doc}
cp -a samples $RPM_BUILD_ROOT%{_examplesdir}/%{srcname}-%{version}
cp -a build/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc %{?with_doc:build/docs/design build/docs/xsltc}
%{_javadir}/jaxp_transform_impl.jar
%{_javadir}/xalan-%{version}.jar
%{_javadir}/xalan.jar
%{_javadir}/xalan-serializer-%{version}.jar
%{_javadir}/xalan-serializer.jar
%{_javadir}/xsltc-%{version}.jar
%{_javadir}/xsltc.jar
%{_javadir}/xalan-j2.jar
%{_javadir}/xalan-j2-serializer.jar

%if %{with doc}
%files javadoc
%defattr(644,root,root,755)
%doc %{_javadocdir}/%{srcname}-%{version}

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{srcname}-%{version}
%endif
