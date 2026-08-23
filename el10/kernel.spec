### spec file for Enterprise Linux 10 (EL10)
### Licensed as GPLv3

%global _default_patch_fuzz 2
%define _build_id_links none
%define _disable_source_fetch 1

%ifarch x86_64
%define karch x86
%define asmarch x86
%endif

Name: kernel-ogc
Summary: The Linux Kernel with Open Gaming Collective (OGC) patches

%define _basekver @@BASEKVER@@
%define _stablekver @@STABLEKVER@@
%define _rcver @@RCVER@@

%if "%{_rcver}" == "none"
%if %{_stablekver} == 0
%define _tarkver %{_basekver}
%else
%define _tarkver %{_basekver}.%{_stablekver}
%endif
%define _rcrel %{nil}
%else
%define _tarkver %{_basekver}-%{_rcver}
%define _rcrel .%{_rcver}
%endif

Version: %{_basekver}.%{_stablekver}

%define ogcver @@OGCVER@@
%define buildnum @@BUILDNUM@@
Release: ogc%{ogcver}%{_rcrel}.%{buildnum}%{?dist}

%define rpmver %{version}-%{release}
%define krelstr %{release}.%{_arch}
%define kverstr %{version}-%{krelstr}

License: GPLv2 and Redistributable, no modifications permitted
Group: System Environment/Kernel
Vendor: The Linux Community and OGC maintainer(s)
URL: https://opengamingcollective.org
Source0: linux-%{_tarkver}.tar.xz
Source1: config
Patch0: monolithic.patch

ExcludeArch:    %{ix86}

BuildRequires: bc
BuildRequires: binutils
BuildRequires: bison
BuildRequires: cpio
BuildRequires: dwarves
BuildRequires: flex
BuildRequires: gcc
BuildRequires: git
BuildRequires: kmod
BuildRequires: make
BuildRequires: perl
BuildRequires: python3
BuildRequires: redhat-rpm-config
BuildRequires: rpm-build
BuildRequires: rust
BuildRequires: rust-src
BuildRequires: tar
BuildRequires: xz
BuildRequires: openssl-devel
BuildRequires: elfutils-libelf-devel
BuildRequires: zlib-devel
BuildRequires: ncurses-devel

Requires: kernel-ogc-core = %{rpmver}
Requires: kernel-ogc-modules = %{rpmver}
Provides: kernel-ogc = %{rpmver}
Provides: kernel-ogc-uname-r = %{kverstr}

%description
The kernel-ogc meta package

%package core
Summary: Kernel core package
Group: System Environment/Kernel
Provides: installonlypkg(kernel)
Provides: kernel = %{rpmver}
Provides: kernel-core = %{rpmver}
Provides: kernel-core-uname-r = %{kverstr}
Provides: kernel-uname-r = %{kverstr}
Provides: kernel-%{_arch} = %{rpmver}
Provides: kernel-core%{_isa} = %{rpmver}
Provides: kernel-core-%{rpmver} = %{kverstr}
Provides: kernel-ogc-core-%{rpmver} = %{kverstr}
Requires: bash
Requires: coreutils
Requires: linux-firmware
Requires: /usr/bin/kernel-install
Requires: kernel-ogc-modules-%{rpmver} = %{kverstr}
Supplements: kernel-ogc = %{rpmver}
%description core
The kernel-ogc package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system: memory allocation, process allocation, device
input and output, etc.

%package modules
Summary: Kernel modules to match the core kernel
Group: System Environment/Kernel
Provides: installonlypkg(kernel-module)
Provides: kernel-modules = %{rpmver}
Provides: kernel-modules%{_isa} = %{rpmver}
Provides: kernel-modules-core = %{rpmver}
Provides: kernel-modules-extra = %{rpmver}
Provides: kernel-modules-uname-r = %{kverstr}
Provides: kernel-modules-%{_arch} = %{rpmver}
Provides: kernel-modules-core-uname-r = %{kverstr}
Provides: kernel-modules-extra-uname-r = %{kverstr}
Provides: kernel-modules-%{rpmver} = %{kverstr}
Provides: kernel-ogc-modules-%{rpmver} = %{kverstr}
Supplements: kernel-ogc = %{rpmver}
Requires: kmod
%description modules
This package provides kernel modules for the core kernel-ogc kernel package.

%package headers
Summary: Header files for the Linux kernel for use by glibc
Group: Development/System
Provides: kernel-headers = %{kverstr}
Provides: glibc-kernheaders = 3.0-46
Provides: kernel-headers%{_isa} = %{kverstr}
Obsoletes: kernel-headers < %{kverstr}
Obsoletes: glibc-kernheaders < 3.0-46
%description headers
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.

%package devel
Summary: Development package for building kernel modules to match the kernel-ogc kernel
Group: System Environment/Kernel
AutoReqProv: no
Requires: findutils
Requires: perl-interpreter
Requires: openssl-devel
Requires: flex
Requires: make
Requires: bison
Requires: elfutils-libelf-devel
Requires: gcc
Enhances: akmods
Enhances: dkms
Provides: installonlypkg(kernel)
Provides: kernel-devel = %{rpmver}
Provides: kernel-devel-uname-r = %{kverstr}
Provides: kernel-devel-%{_arch} = %{rpmver}
Provides: kernel-devel%{_isa} = %{rpmver}
Provides: kernel-devel-%{rpmver} = %{kverstr}
Provides: kernel-ogc-devel-%{rpmver} = %{kverstr}
%description devel
This package provides kernel headers and makefiles sufficient to build modules
against the kernel-ogc kernel package.

%package devel-matched
Summary: Meta package to install matching core and devel packages for a given kernel-ogc kernel
Requires: kernel-ogc-devel = %{rpmver},
Requires: kernel-ogc-core = %{rpmver}
Provides: kernel-devel-matched = %{rpmver}
Provides: kernel-devel-matched%{_isa} = %{rpmver}
%description devel-matched
This meta package is used to install matching core and devel packages for a given kernel-ogc kernel.

%prep
%setup -q -n linux-%{_tarkver}

patch -p1 -i %{PATCH0}

cp %{SOURCE1} .config

scripts/config -u DEFAULT_HOSTNAME

scripts/config --set-str BUILD_SALT "%{kverstr}"

make olddefconfig

cat .config > config-linux-ogc

%build
make %{?_smp_mflags} EXTRAVERSION=-%{krelstr}

%install

%ifarch aarch64
mkdir -p %{buildroot}/boot/dtb-%{kverstr}
make %{?_smp_mflags} ARCH=arm64 dtbs
make %{?_smp_mflags} ARCH=arm64 dtbs_install \
     INSTALL_DTBS_PATH=%{buildroot}/boot/dtb-%{kverstr}
mkdir -p %{buildroot}/lib/modules/%{kverstr}/dtb
cp -a %{buildroot}/boot/dtb-%{kverstr}/. %{buildroot}/lib/modules/%{kverstr}/dtb/
%endif

ImageName=$(make KERNELRELEASE=%{kverstr} image_name | tail -n 1)

mkdir -p %{buildroot}/boot

cp -v $ImageName %{buildroot}/boot/vmlinuz-%{kverstr}
chmod 755 %{buildroot}/boot/vmlinuz-%{kverstr}

ZSTD_CLEVEL=19 make %{?_smp_mflags} \
    KERNELRELEASE=%{kverstr} \
    INSTALL_MOD_PATH=%{buildroot} \
    INSTALL_MOD_STRIP=1 \
    modules_install mod-fw=

make %{?_smp_mflags} INSTALL_HDR_PATH=%{buildroot}/usr headers_install

cd %{_builddir}/linux-%{_tarkver}
rm -f %{buildroot}/lib/modules/%{kverstr}/build
rm -f %{buildroot}/lib/modules/%{kverstr}/source
mkdir -p %{buildroot}/lib/modules/%{kverstr}/build
(cd %{buildroot}/lib/modules/%{kverstr} ; ln -s build source)
mkdir -p %{buildroot}/lib/modules/%{kverstr}/updates
mkdir -p %{buildroot}/lib/modules/%{kverstr}/weak-updates
find . -name *.h.s -delete
cp --parents `find  -type f -name "Makefile*" -o -name "Kconfig*"` %{buildroot}/lib/modules/%{kverstr}/build
if [ ! -e Module.symvers ]; then
touch Module.symvers
fi
cp Module.symvers %{buildroot}/lib/modules/%{kverstr}/build
cp System.map %{buildroot}/lib/modules/%{kverstr}/build
if [ -s Module.markers ]; then
cp Module.markers %{buildroot}/lib/modules/%{kverstr}/build
fi

echo "**** GENERATING kernel ABI metadata ****"
gzip -c9 < Module.symvers > %{buildroot}/boot/symvers-%{kverstr}.gz
cp %{buildroot}/boot/symvers-%{kverstr}.gz %{buildroot}/lib/modules/%{kverstr}/symvers.gz

rm -rf %{buildroot}/lib/modules/%{kverstr}/build/scripts
rm -rf %{buildroot}/lib/modules/%{kverstr}/build/include
cp .config %{buildroot}/lib/modules/%{kverstr}/build
cp -a scripts %{buildroot}/lib/modules/%{kverstr}/build
rm -rf %{buildroot}/lib/modules/%{kverstr}/build/scripts/tracing
rm -f %{buildroot}/lib/modules/%{kverstr}/build/scripts/spdxcheck.py

%ifarch s390x
if [ -f arch/s390/lib/expoline/expoline.o ]; then
cp -a --parents arch/s390/lib/expoline/expoline.o %{buildroot}/lib/modules/%{kverstr}/build
fi
%endif

mkdir -p %{buildroot}/lib/modules/%{kverstr}/build/tools/include/tools
cp -a --parents tools/include/tools/be_byteshift.h %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/include/tools/le_byteshift.h %{buildroot}/lib/modules/%{kverstr}/build

cp -a --parents tools/include/linux/compiler* %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/include/linux/types.h %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/build/Build.include %{buildroot}/lib/modules/%{kverstr}/build
cp --parents tools/build/fixdep.c %{buildroot}/lib/modules/%{kverstr}/build
cp --parents tools/objtool/sync-check.sh %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/bpf/resolve_btfids %{buildroot}/lib/modules/%{kverstr}/build

cp -a --parents tools/include/asm-generic %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/include/linux %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/include/uapi/asm %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/include/uapi/asm-generic %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/include/uapi/linux %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/include/vdso %{buildroot}/lib/modules/%{kverstr}/build
cp --parents tools/scripts/utilities.mak %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/lib/subcmd %{buildroot}/lib/modules/%{kverstr}/build
cp --parents tools/lib/*.c %{buildroot}/lib/modules/%{kverstr}/build
cp --parents tools/objtool/*.[ch] %{buildroot}/lib/modules/%{kverstr}/build
cp --parents tools/objtool/Build %{buildroot}/lib/modules/%{kverstr}/build
cp --parents tools/objtool/include/objtool/*.h %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/lib/bpf %{buildroot}/lib/modules/%{kverstr}/build
cp --parents tools/lib/bpf/Build %{buildroot}/lib/modules/%{kverstr}/build

if [ -f tools/objtool/objtool ]; then
cp -a tools/objtool/objtool %{buildroot}/lib/modules/%{kverstr}/build/tools/objtool/ || :
fi
if [ -f tools/objtool/fixdep ]; then
cp -a tools/objtool/fixdep %{buildroot}/lib/modules/%{kverstr}/build/tools/objtool/ || :
fi
if [ -d arch/%{karch}/scripts ]; then
cp -a arch/%{karch}/scripts %{buildroot}/lib/modules/%{kverstr}/build/arch/%{_arch} || :
fi
if [ -f arch/%{karch}/*lds ]; then
cp -a arch/%{karch}/*lds %{buildroot}/lib/modules/%{kverstr}/build/arch/%{_arch}/ || :
fi
if [ -f arch/%{asmarch}/kernel/module.lds ]; then
cp -a --parents arch/%{asmarch}/kernel/module.lds %{buildroot}/lib/modules/%{kverstr}/build/
fi
find %{buildroot}/lib/modules/%{kverstr}/build/scripts \( -iname "*.o" -o -iname "*.cmd" \) -exec rm -f {} +
%ifarch ppc64le
cp -a --parents arch/powerpc/lib/crtsavres.[So] %{buildroot}/lib/modules/%{kverstr}/build/
%endif
if [ -d arch/%{asmarch}/include ]; then
cp -a --parents arch/%{asmarch}/include %{buildroot}/lib/modules/%{kverstr}/build/
fi
%ifarch aarch64
cp -a --parents arch/arm/include/asm/xen %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/arm/include/asm/opcodes.h %{buildroot}/lib/modules/%{kverstr}/build/
%endif
%ifarch %{arm}
if [ -d arch/%{asmarch}/mach-${Variant}/include ]; then
cp -a --parents arch/%{asmarch}/mach-${Variant}/include %{buildroot}/lib/modules/%{kverstr}/build/
fi
cp -a --parents arch/arm/tools/gen-mach-types %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/arm/tools/mach-types %{buildroot}/lib/modules/%{kverstr}/build/
%endif
cp -a include %{buildroot}/lib/modules/%{kverstr}/build/include

%ifarch i686 x86_64
cp -a --parents arch/x86/entry/syscalls/syscall_32.tbl %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/entry/syscalls/syscall_64.tbl %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/tools/relocs_32.c %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/tools/relocs_64.c %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/tools/relocs.c %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/tools/relocs_common.c %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/tools/relocs.h %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/purgatory/purgatory.c %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/purgatory/stack.S %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/purgatory/setup-x86_64.S %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/purgatory/entry64.S %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/boot/string.h %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/boot/string.c %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/boot/ctype.h %{buildroot}/lib/modules/%{kverstr}/build/

cp -a --parents scripts/syscalltbl.sh %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents scripts/syscallhdr.sh %{buildroot}/lib/modules/%{kverstr}/build/

cp -a --parents tools/arch/x86/include/asm %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/arch/x86/include/uapi/asm %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/objtool/arch/x86/lib %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/arch/x86/lib/ %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/arch/x86/tools/gen-insn-attr-x86.awk %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/objtool/arch/x86/ %{buildroot}/lib/modules/%{kverstr}/build
%endif

find %{buildroot}/lib/modules/%{kverstr} -name "*.ko" -type f >modnames
xargs --no-run-if-empty chmod u+x < modnames

grep -F /drivers/ modnames | xargs --no-run-if-empty nm -upA |
sed -n 's,^.*/\([^/]*\.ko\):  *U \(.*\)$,\1 \2,p' > drivers.undef

collect_modules_list()
{
  sed -r -n -e "s/^([^ ]+) \\.?($2)\$/\\1/p" drivers.undef |
  LC_ALL=C sort -u > %{buildroot}/lib/modules/%{kverstr}/modules.$1
  if [ ! -z "$3" ]; then
  sed -r -e "/^($3)\$/d" -i %{buildroot}/lib/modules/%{kverstr}/modules.$1
  fi
}

collect_modules_list networking \
  'register_netdev|ieee80211_register_hw|usbnet_probe|phy_driver_register|rt(l_|2x00)(pci|usb)_probe|register_netdevice'
collect_modules_list block \
  'ata_scsi_ioctl|scsi_add_host|scsi_add_host_with_dma|blk_alloc_queue|blk_init_queue|register_mtd_blktrans|scsi_esp_register|scsi_register_device_handler|blk_queue_physical_block_size' 'pktcdvd.ko|dm-mod.ko'
collect_modules_list drm \
  'drm_open|drm_init'
collect_modules_list modesetting \
  'drm_crtc_init'

( find %{buildroot}/lib/modules/%{kverstr} -name '*.ko' | xargs /sbin/modinfo -l | \
grep -E -v 'GPL( v2)?$|Dual BSD/GPL$|Dual MPL/GPL$|GPL and additional rights$' ) && exit 1

remove_depmod_files()
{
pushd %{buildroot}/lib/modules/%{kverstr}/
rm -f modules.{alias,alias.bin,builtin.alias.bin,builtin.bin} \
  modules.{dep,dep.bin,devname,softdep,symbols,symbols.bin}
popd
}

remove_depmod_files

mkdir -p %{buildroot}%{_prefix}/src/kernels
mv %{buildroot}/lib/modules/%{kverstr}/build %{buildroot}%{_prefix}/src/kernels/%{kverstr}

ln -sf %{_prefix}/src/kernels/%{kverstr} %{buildroot}/lib/modules/%{kverstr}/build

find %{buildroot}%{_prefix}/src/kernels -name ".*.cmd" -delete

cp -v System.map %{buildroot}/boot/System.map-%{kverstr}
cp -v System.map %{buildroot}/lib/modules/%{kverstr}/System.map
cp -v .config %{buildroot}/boot/config-%{kverstr}
cp -v .config %{buildroot}/lib/modules/%{kverstr}/config

(cd "%{buildroot}/boot/" && sha512hmac "vmlinuz-%{kverstr}" > ".vmlinuz-%{kverstr}.hmac")

cp -v  %{buildroot}/boot/vmlinuz-%{kverstr} %{buildroot}/lib/modules/%{kverstr}/vmlinuz
(cd "%{buildroot}/lib/modules/%{kverstr}" && sha512hmac vmlinuz > .vmlinuz.hmac)

dd if=/dev/zero of=%{buildroot}/boot/initramfs-%{kverstr}.img bs=1M count=48

%clean
rm -rf %{buildroot}

%post core
if [ `uname -i` == "x86_64" -o `uname -i` == "i386" ] &&
   [ -f /etc/sysconfig/kernel ]; then
  /bin/sed -r -i -e 's/^DEFAULTKERNEL=kernel-smp$/DEFAULTKERNEL=kernel/' /etc/sysconfig/kernel || exit $?
fi

%posttrans core
/bin/kernel-install add %{kverstr} /lib/modules/%{kverstr}/vmlinuz || exit $?
if [ ! -z $(rpm -qa | grep grubby) ]; then
  grubby --set-default="/boot/vmlinuz-%{kverstr}"
fi

%preun core
/bin/kernel-install remove %{kverstr} /lib/modules/%{kverstr}/vmlinuz || exit $?
if [ -x /usr/sbin/weak-modules ]
then
/usr/sbin/weak-modules --remove-kernel %{kverstr} || exit $?
fi

%post modules
/sbin/depmod -a %{kverstr}

%post devel
if [ -f /etc/sysconfig/kernel ]
then
. /etc/sysconfig/kernel || exit $?
fi
if [ "$HARDLINK" != "no" -a -x /usr/bin/hardlink -a ! -e /run/ostree-booted ]
then
(cd /usr/src/kernels/%{kverstr} &&
 /usr/bin/find . -type f | while read f; do
   hardlink -c /usr/src/kernels/*%{?dist}.*/$f $f 2>&1 >/dev/null
 done)
fi

%files core
%ghost %attr(0600, root, root) /boot/vmlinuz-%{kverstr}
%ghost %attr(0600, root, root) /boot/System.map-%{kverstr}
%ghost %attr(0600, root, root) /boot/initramfs-%{kverstr}.img
%ghost %attr(0600, root, root) /boot/symvers-%{kverstr}.gz
%ghost %attr(0644, root, root) /boot/config-%{kverstr}
/boot/.vmlinuz-%{kverstr}.hmac
%dir /lib/modules/%{kverstr}/
/lib/modules/%{kverstr}/.vmlinuz.hmac
/lib/modules/%{kverstr}/config
/lib/modules/%{kverstr}/vmlinuz
/lib/modules/%{kverstr}/System.map
/lib/modules/%{kverstr}/symvers.gz
%ifarch aarch64
%dir /boot/dtb-%{kverstr}
%dir /lib/modules/%{kverstr}/dtb
/boot/dtb-%{kverstr}/*
/boot/dtb-%{kverstr}/*/*
/lib/modules/%{kverstr}/dtb/*
/lib/modules/%{kverstr}/dtb/*/*
%endif

%files modules
/lib/modules/%{kverstr}/
%exclude /lib/modules/%{kverstr}/.vmlinuz.hmac
%exclude /lib/modules/%{kverstr}/config
%exclude /lib/modules/%{kverstr}/vmlinuz
%exclude /lib/modules/%{kverstr}/System.map
%exclude /lib/modules/%{kverstr}/symvers.gz
%exclude /lib/modules/%{kverstr}/build
%exclude /lib/modules/%{kverstr}/source

%files headers
%defattr (-, root, root)
/usr/include/*

%files devel
%defattr (-, root, root)
/usr/src/kernels/%{kverstr}
/lib/modules/%{kverstr}/build
/lib/modules/%{kverstr}/source

%files devel-matched

%changelog
* Sun Aug 23 2026 OGC Maintainer <maintainer@opengamingcollective.org>
- Initial EL10 package
