#include "pybit7z.hpp"

#include <iostream>

namespace _core {

std::string& default_library_path() {
#ifdef WIN32
#if defined(_MSC_VER)
    constexpr auto default_lib7zip = "7zip.dll";
#else
    constexpr auto default_lib7zip = "lib7zip.dll";
#endif
#elif __APPLE__
    constexpr auto default_lib7zip = "lib7zip.dylib";
#else
    constexpr auto default_lib7zip = "lib7zip.so";
#endif
    static std::string default_path(default_lib7zip);
    return default_path;
}

const bit7z::Bit7zLibrary& Bit7zipSingleton::getInstance() {
    auto lib7zip_dir = std::getenv("__PYBIT7Z_LIB7ZIP_PATH__");
    static const bit7z::Bit7zLibrary instance(
        lib7zip_dir == nullptr ? default_library_path() : std::string(lib7zip_dir) + "/" + default_library_path());
    return instance;
}

} // namespace _core
