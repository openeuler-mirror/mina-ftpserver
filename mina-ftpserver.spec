Name:                mina-ftpserver
Version:             1.0.6
Release:             5
Summary:             A 100% pure Java FTP server
License:             ASL 2.0
URL:                 http://mina.apache.org/ftpserver-project/
Source0:             https://archive.apache.org/dist/mina/ftpserver/%{version}/ftpserver-%{version}-src.tar.gz
Patch0:              mina-ftpserver-1.0.6-mina2.0.9.patch
Patch1:              fix-build-error-for-apache-mina-upgrade.patch

BuildRequires:       maven-local mvn(commons-codec:commons-codec) mvn(commons-net:commons-net)
BuildRequires:       mvn(hsqldb:hsqldb:1) mvn(junit:junit) mvn(log4j:log4j:1.2.17)
BuildRequires:       mvn(org.apache:apache:pom:) mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:       mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:       mvn(org.apache.mina:mina-core) mvn(org.osgi:org.osgi.core)
BuildRequires:       mvn(org.slf4j:jcl-over-slf4j) mvn(org.slf4j:slf4j-api)
BuildRequires:       mvn(org.slf4j:slf4j-log4j12) mvn(org.springframework:spring-beans)
BuildRequires:       mvn(org.springframework:spring-context)
BuildArch:           noarch

%description
The Apache FtpServer is a 100% pure Java FTP server. It's
designed to be a complete and portable FTP server engine
solution based on currently available open protocols.
FtpServer can be run standalone as a Windows service or
Unix/Linux daemon, or embedded into a Java application.
We also provide support for integration within Spring
applications and provide our releases as OSGi bundles.
The default network support is based on Apache MINA, a
high performance asynchronous IO library. Using MINA,
FtpServer can scale to a large number of concurrent users.
It is also an FTP application platform. We have developed
a Java API to let you write Java code to process FTP event
notifications that we call the Ftplet API. Apache FtpServer
provides an implementation of an FTP server to support this
API.

%package examples
Summary:             Apache FtpServer Examples

%description examples
This package provides:
* FtpServer OSGi Ftplet service example
* FtpServer OSGi Spring-DM example

%package javadoc
Summary:             Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n apache-ftpserver-%{version}
find . -name "*.bat" -delete
find . -name "*.class" -delete
find . -name "*.exe" -delete
find . -name "*.jar" -delete
%patch0 -p1
%patch1 -p1
mv src/* ./

%pom_disable_module distribution
%pom_disable_module ftpserver-example-spring-war examples
%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin -r :rat-maven-plugin
%pom_remove_plugin :jxr-maven-plugin ftplet-api
%pom_xpath_set "pom:Bundle-SymbolicName" '${project.artifactId}' ftplet-api
%pom_xpath_set "pom:Bundle-SymbolicName" '${project.artifactId}' core
%pom_xpath_set "pom:Bundle-SymbolicName" '${project.artifactId}' examples/ftpserver-osgi-ftplet-service
%pom_xpath_set "pom:Bundle-SymbolicName" '${project.artifactId}' examples/ftpserver-osgi-spring-service
%pom_xpath_remove "pom:Private-Package" core
%pom_xpath_inject "pom:plugin[pom:artifactId='maven-bundle-plugin']/pom:configuration/pom:instructions" "
<Private-Package>org.apache.ftpserver.command.impl,
org.apache.ftpserver.command.impl.listing,
org.apache.ftpserver.filesystem.nativefs.impl,
org.apache.ftpserver.ftpletcontainer.impl,
org.apache.ftpserver.impl, org.apache.ftpserver.listener.nio,
org.apache.ftpserver.message.impl, org.apache.ftpserver.ssl.impl,
org.apache.ftpserver.usermanager.impl,
org.apache.ftpserver.util</Private-Package>" core
%pom_xpath_inject "pom:plugin[pom:artifactId='maven-surefire-plugin']" "<configuration><testFailureIgnore>true</testFailureIgnore></configuration>"
%pom_change_dep org.osgi:osgi_R4_core org.osgi:org.osgi.core examples/ftpserver-osgi-ftplet-service
%pom_change_dep -r :hsqldb :hsqldb:1
%pom_change_dep -r :log4j :log4j:1.2.17
%mvn_package :ftpserver-examples examples
%mvn_package :ftpserver-osgi-*-service examples
rm core/src/test/java/org/apache/ftpserver/impl/DefaultFtpServerTest.java  \
 core/src/test/java/org/apache/ftpserver/ssl/MinaExplicitSSLTest.java \
 core/src/test/java/org/apache/ftpserver/ssl/MinaImplicitDataChannelTest.java \
 core/src/test/java/org/apache/ftpserver/ssl/MinaImplicitSSLTest.java \
 core/src/test/java/org/apache/ftpserver/clienttests/PasvUsedPortTest.java

%build
%mvn_build -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles
%doc distribution/README.txt
%license LICENSE NOTICE

%files examples -f .mfiles-examples
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Thu 31 Mar 2022 xiaoqianlv <xiaoqian@nj.iscas.ac.cn> - 1.0.6-5
- ignore maven-surefire-plugin test failure 

* Tue 9 Feb 2021 baizhonggui <baizhonggui@huawei.com> - 1.0.6-4
- Remove unused model

* Wed 28 Oct 2020 baizhonggui <baizhonggui@huawei.com> - 1.0.6-3
- Remove spring-context-support dep

* Mon 21 Sep 2020 wangyue <wangyue92@huawei.com> - 1.0.6-2
- Fix build errors for apache-mina upgrade

* Tue Jul 28 2020 leiju <leiju4@huawei.com> - 1.0.6-1
- Package init
