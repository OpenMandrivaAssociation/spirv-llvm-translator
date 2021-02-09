%define major %(echo %{version} |cut -d. -f1)
%define libname %mklibname LLVMSPIRVLib %{major}
%define devname %mklibname -d LLVMSPIRVLib

Name: spirv-llvm-translator
Version: 11.0.0
Release: 1
Source0: https://github.com/KhronosGroup/SPIRV-LLVM-Translator/archive/v%{version}/%{name}-%{version}.tar.gz
Summary: Library for bi-directional translation between SPIR-V and LLVM IR
URL: https://github.com/KhronosGroup/SPIRV-LLVM-Translator
License: Apache 2.0
Group: Development/Tools
BuildRequires: cmake ninja
BuildRequires: cmake(llvm)
BuildRequires: spirv-tools

%description
Library for bi-directional translation between SPIR-V and LLVM IR

%package -n %{libname}
Summary: Library for bi-directional translation between SPIR-V and LLVM IR
Group: System/Libraries

%description -n %{libname}
Library for bi-directional translation between SPIR-V and LLVM IR

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

%prep
%autosetup -p1 -n SPIRV-LLVM-Translator-%{version}
%cmake -G Ninja \
	-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON

%build
%ninja_build -C build

%install
%ninja_install -C build
