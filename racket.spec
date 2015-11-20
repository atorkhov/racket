# --disable-strip option in configure doesn't work
%global debug_package %{nil}

Name:           racket
Version:        6.2.1
Release:        1%{?dist}
Summary:        Racket

Group:          Development/Languages
License:        LGPLv3+
URL:            http://racket-lang.org
# Unable to do full build. see https://github.com/racket/racket/issues/1144
Source0:        http://mirror.racket-lang.org/installers/6.2.1/racket-6.2.1-src-builtpkgs.tgz

BuildRequires:  gcc libffi-devel desktop-file-utils

# Runtime requires for packages

# readline-lib/readline/rktrl.rkt
Requires:       readline

# gui-lib/mred/private/wx/gtk
Requires:       atk glib2 gdk-pixbuf2 gtk2 unique

# sgl/gl.rkt
Requires:       mesa-libGL

# math-lib/math/private/bigfloat
Requires:       gmp mpfr

# db-lib/db/private/odbc/ffi.rkt
Requires:       libiodbc

# racket-doc/scribblings/foreign/intro.scrbl:(define-ffi-definer define-curses (ffi-lib "libcurses"))
Requires:       ncurses-devel

# racket-doc/ffi/examples/tcl.rkt:(define libtcl (ffi-lib "libtcl"))
# racket-doc/ffi/examples/xosd.rkt:(define libxosd (ffi-lib "libxosd"))
# racket-doc/ffi/examples/xmmsctrl.rkt:(define libxmms (ffi-lib "libxmms"))
# racket-doc/ffi/examples/crypt.rkt:(define libcrypt (ffi-lib "libcrypt"))
# racket-doc/ffi/examples/magick.rkt:          (ffi-lib lib version))))))
# racket-doc/ffi/examples/esd.rkt:(define libesd (ffi-lib "libesd"))
# racket-doc/ffi/examples/sndfile.rkt:    ['unix (ffi-lib "libsndfile"   '("1.0.21" "1.0.20" ""))]
# racket-doc/scribblings/reference/filesystem.scrbl:(define libfit (ffi-lib libfit-path))
# racket-doc/scribblings/reference/filesystem.scrbl:(define libssl (ffi-lib libssl-so))

# draw-lib/racket/draw/unsafe/pango.rkt
Requires:       pango

# draw-lib/racket/draw/unsafe/glib.rkt
Requires:       glib2

# draw-lib/racket/draw/unsafe/cairo-lib.rkt
Requires:       fontconfig cairo

# draw-lib/racket/draw/unsafe/png.rkt
Requires:       libpng

# draw-lib/racket/draw/unsafe/jpeg.rkt
Requires:       libjpeg-turbo

%description
Racket is a full-spectrum programming language. It goes beyond Lisp and Scheme
with dialects that support objects, types, laziness, and more. Racket enables
programmers to link components written in different dialects, and it empowers
programmers to create new, project-specific dialects. Racket's libraries
support applications from web servers and databases to GUIs and charts.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
cd src
%configure
make %{?_smp_mflags}


%install
cd src
%make_install

# Fix paths. see https://github.com/racket/racket/issues/1143
sed -i -e 's,%{buildroot},,' %{buildroot}/%{_datadir}/applications/drracket.desktop
sed -i -e 's,%{buildroot},,' %{buildroot}/%{_datadir}/applications/slideshow.desktop


%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/drracket.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/slideshow.desktop


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%doc README src/COPYING*
%{_sysconfdir}/%{name}
%{_bindir}/*
%{_libdir}/%{name}
%{_datadir}/applications/*.desktop
%{_mandir}/man1/*
%{_datadir}/%{name}

%files devel
%{_includedir}/%{name}


%changelog
* Fri Nov 20 2015 Alexey Torkhov <atorkhov@gmail.com> 6.2.1-1
-  Initial package.

