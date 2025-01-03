#include "pybit7z.hpp"

namespace _core {

const char* platform_lib7zip_name() {
#ifdef WIN32
#if defined(_MSC_VER)
    constexpr auto lib7zip_name = "7zip.dll";
#else
    constexpr auto lib7zip_name = "lib7zip.dll";
#endif
#elif __APPLE__
    constexpr auto lib7zip_name = "lib7zip.dylib";
#else
    constexpr auto lib7zip_name = "lib7zip.so";
#endif
    return lib7zip_name;
}

} // namespace _core
