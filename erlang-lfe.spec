%global realname lfe
%global upstream rvirding
%global debug_package %{nil}
%global git_tag 15b36cb
%global patchnumber 0


%if 0%{?el6}%{?fedora}
%bcond_without emacs
%else
%bcond_with emacs
%endif


%if %{with emacs}
# If the emacs-el package has installed a pkgconfig file, use that to determine
# install locations and Emacs version at build time, otherwise set defaults.
%if %($(pkg-config emacs) ; echo $?)
%define emacs_version 22.1
%define emacs_lispdir %{_datadir}/emacs/site-lisp
%define emacs_startdir %{_datadir}/emacs/site-lisp/site-start.d
%else
%define emacs_version %(pkg-config emacs --modversion)
%define emacs_lispdir %(pkg-config emacs --variable sitepkglispdir)
%define emacs_startdir %(pkg-config emacs --variable sitestartdir)
%endif
%endif


Name:		erlang-%{realname}
Version:	0.6.2
Release:	3%{?dist}
Summary:	Lisp Flavoured Erlang
Group:		Development/Languages
License:	BSD
URL:		http://github.com/rvirding/lfe
# wget --content-disposition http://github.com/rvirding/lfe/tarball/v0.6.2
Source0:	%{upstream}-%{realname}-%{version}-%{patchnumber}-g%{git_tag}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	erlang-rebar
%if %{with emacs}
BuildRequires:	emacs(bin), emacs-el >= 22.1-2
BuildRequires:	pkgconfig
BuildRequires:	emacs
BuildRequires:	xemacs
BuildRequires:	emacs-el
BuildRequires:	xemacs-packages-extra-el
%endif

Requires:	erlang-compiler%{?_isa}
Requires:	erlang-erts%{?_isa}
Requires:	erlang-kernel%{?_isa}
# Error:erlang(unicode:characters_to_list/1) in R12B and earlier
Requires:	erlang-stdlib%{?_isa} >= R13B


%description
Lisp Flavoured Erlang, is a lisp syntax front-end to the Erlang
compiler. Code produced with it is compatible with "normal" Erlang
code. An LFE evaluator and shell is also included.

%if %{with emacs}
%package -n emacs-erlang-lfe
Summary:	Emacs major mode for Lisp Flavoured Erlang
Group:		Applications/Editors
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description -n emacs-erlang-lfe
This package provides an Emacs major mode to edit Lisp Flavoured Erlang
files.

%package -n emacs-erlang-lfe-el
Summary:	Elisp source files for Lisp Flavoured Erlang under GNU Emacs
Group:		Applications/Editors
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description -n emacs-erlang-lfe-el
This package contains the elisp source files for Lisp Flavoured Erlang
under GNU Emacs. You do not need to install this package to run
Lisp Flavoured Erlang. Install the emacs-erlang-lfe package to use
Lisp Flavoured Erlang with GNU Emacs.
%endif


%prep
%setup -q -n %{upstream}-%{realname}-%{git_tag}
iconv -f iso-8859-1 -t UTF-8 README  > README.utf8
mv -f README.utf8  README
iconv -f iso-8859-1 -t UTF-8  examples/core-macros.lfe > examples/core-macros.lfe.utf8
mv  -f examples/core-macros.lfe.utf8 examples/core-macros.lfe
iconv -f iso-8859-1 -t UTF-8 doc/release_notes.txt > doc/release_notes.txt.utf8
mv -f doc/release_notes.txt.utf8 doc/release_notes.txt
# Remove precompiled elisp binary
rm emacs/lfe-mode.elc


%build
rebar compile -v
%if %{with emacs}
emacs -batch -f batch-byte-compile emacs/lfe-mode.el
%endif


%install
rm -rf %{buildroot}
install -p -m 0644 -D ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -p -m 0644 ebin/%{realname}_*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%if %{with emacs}
mkdir -p %{buildroot}%{emacs_lispdir}
mkdir -p %{buildroot}%{emacs_startdir}
install -p -m 0644 emacs/lfe-mode.el %{buildroot}%{emacs_lispdir}
install -p -m 0644 emacs/lfe-mode.elc %{buildroot}%{emacs_lispdir}
install -p -m 0644 emacs/lfe-start.el %{buildroot}%{emacs_startdir}
%endif


%clean
rm -rf %{buildroot}


%check
rebar eunit -v


%files
%doc COPYRIGHT README doc/ examples/
%if %{without emacs}
%doc emacs/
%endif
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_*.beam


%if %{with emacs}
%files -n emacs-erlang-lfe
%{emacs_startdir}/lfe-start.el
%{emacs_lispdir}/lfe-mode.elc


%files -n emacs-erlang-lfe-el
%{emacs_lispdir}/lfe-mode.el
%endif


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 11 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.6.2-1
- Ver. 0.6.2 (Backwards API/ABI compatible)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 17 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.6.1-5
- Make building of emacs sub-packages conditional (and disable on EL-5)

* Sun Nov 14 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.6.1-4
- Remove duplicated emacs files from docs

* Sun Oct 31 2010 Tim Niemueller <tim@niemueller.de> - 0.6.1-3
- Added Emacs sub-package
- Fix inconsitent macro usage

* Fri Oct 15 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.6.1-2
- Provide (x)emacs subpackages

* Fri Oct  1 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.6.1-1
- Initial build
