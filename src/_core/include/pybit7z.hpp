#pragma once

#include <bit7z/bit7z.hpp>

namespace _core {
#ifdef WIN32
#if defined(_MSC_VER)
constexpr auto default_lib7zip = "7zip.dll";
#else
constexpr auto default_lib7zip = "lib7zip.dll";
#endif
#else
constexpr auto default_lib7zip = "lib7zip.so";
#endif
} // namespace _core
