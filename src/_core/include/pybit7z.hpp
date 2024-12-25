#pragma once

#include <bit7z/bit7z.hpp>

namespace _core {

std::string& default_library_path();

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
