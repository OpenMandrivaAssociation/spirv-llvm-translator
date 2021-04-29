%ifarch %{x86_64}
# Mesa >= 21.0 uses LLVMSPIRVLib
%bcond_without compat32
%endif

%define major %(echo %{version} |cut -d. -f1)
%define libname %mklibname LLVMSPIRVLib %{major}
%define devname %mklibname -d LLVMSPIRVLib
%define lib32name libLLVMSPIRVLib%{major}
%define dev32name libLLVMSPIRVLib-devel

# bd3916... is the last commit before the switch to LLVM 13
%define git bd391609380a34685747206bc4acf890d6a04232

Name: spirv-llvm-translator
Version: 12.0.0
Release: 1
Source0: https://github.com/KhronosGroup/SPIRV-LLVM-Translator/archive/%{git}.tar.gz
Summary: Library for bi-directional translation between SPIR-V and LLVM IR
URL: https://github.com/KhronosGroup/SPIRV-LLVM-Translator
License: Apache 2.0
Group: Development/Tools
BuildRequires: cmake ninja
BuildRequires: cmake(llvm)
BuildRequires: spirv-tools
BuildRequires: %{_lib}gpuruntime
%if %{with compat32}
BuildRequires: libllvm-devel
BuildRequires: libgpuruntime
%endif

%description
Library for bi-directional translation between SPIR-V and LLVM IR

%package -n %{libname}
Summary: Library for bi-directional translation between SPIR-V and LLVM IR
Group: System/Libraries

%description -n %{libname}
Library for bi-directional translation between SPIR-V and LLVM IR

%files
%{_bindir}/llvm-spirv

%files -n %{libname}
%{_libdir}/libLLVMSPIRVLib.so.%{major}*

%package -n %{devname}
Summary: Library for bi-directional translation between SPIR-V and LLVM IR
Group: Development/Tools

%description -n %{devname}
Library for bi-directional translation between SPIR-V and LLVM IR

%files -n %{devname}
%{_includedir}/LLVMSPIRVLib
%{_libdir}/libLLVMSPIRVLib.so
%{_libdir}/pkgconfig/LLVMSPIRVLib.pc

%if %{with compat32}
%package -n %{lib32name}
Summary: Library for bi-directional translation between SPIR-V and LLVM IR (32-bit)
Group: System/Libraries

%description -n %{lib32name}
Library for bi-directional translation between SPIR-V and LLVM IR (32-bit)

%files -n %{lib32name}
%{_prefix}/lib/libLLVMSPIRVLib.so.%{major}*

%package -n %{dev32name}
Summary: Library for bi-directional translation between SPIR-V and LLVM IR (32-bit)
Group: Development/Tools

%description -n %{dev32name}
Library for bi-directional translation between SPIR-V and LLVM IR (32-bit)

%files -n %{dev32name}
%{_prefix}/lib/libLLVMSPIRVLib.so
%{_prefix}/lib/pkgconfig/LLVMSPIRVLib.pc
%endif

%prep
%autosetup -p1 -n SPIRV-LLVM-Translator-%{git}
%if %{with compat32}
%cmake32 -G Ninja \
	-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON
# FIXME for some reason we detect the wrong set of libraries...
sed -i -e 's,lib64,lib,g' build.ninja
cd ..
%endif

%cmake -G Ninja \
	-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON

%build
%if %{with compat32}
%ninja_build -C build32
%endif

%ninja_build -C build

# Build the tool (for whatever reasons, its cmake files are set
# up to work only when built inside the LLVM source tree, but
# that's not actually necessary)
clang++ %{optflags} -Iinclude -o llvm-spirv tools/llvm-spirv/llvm-spirv.cpp -Lbuild/lib/SPIRV -lLLVMSPIRVLib -lLLVMAnalysis -lLLVMBitReader -lLLVMBitWriter -lLLVMCore -lLLVMSupport -lLLVMTransformUtils

%install
%if %{with compat32}
%ninja_install -C build32
%endif

%ninja_install -C build

mkdir -p %{buildroot}%{_bindir}
install -m 755 llvm-spirv %{buildroot}%{_bindir}/
