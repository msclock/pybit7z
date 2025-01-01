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

std::string& lib7zipPath() {
    static std::string lib7zip_path;
    return lib7zip_path;
}

const bit7z::Bit7zLibrary& Bit7zipSingleton::getInstance() {
    static const bit7z::Bit7zLibrary instance([]() {
        if (lib7zipPath().empty()) {
            return platform_lib7zip_name();
        }
        return lib7zipPath().c_str();
    }());
    return instance;
}

} // namespace _core
