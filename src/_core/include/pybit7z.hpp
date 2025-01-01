#pragma once

#include <bit7z/bit7z.hpp>

namespace _core {

const char* platform_lib7zip_name();

std::string& lib7zipPath();

class Bit7zipSingleton {
public:
    static const bit7z::Bit7zLibrary& getInstance();

private:
    Bit7zipSingleton() = default;
    ~Bit7zipSingleton() = default;

    Bit7zipSingleton(const Bit7zipSingleton&) = delete;
    Bit7zipSingleton& operator=(const Bit7zipSingleton&) = delete;
};

} // namespace _core
