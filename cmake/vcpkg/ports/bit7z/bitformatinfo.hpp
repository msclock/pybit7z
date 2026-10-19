/*
 * bit7z - A C++ static library to interface with the 7-zip shared libraries.
 * Copyright (c) 2014-2023 Riccardo Ostani - All Rights Reserved.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

#ifndef BITFORMATINFO_HPP
#define BITFORMATINFO_HPP

#include "bittypes.hpp"

#include <cstdint>
#include <string>

namespace bit7z {

struct BitFormatInfo {
    std::string name;
    std::string extension;
    std::string addExtension;
    bool update = false;
    std::string signature;
    std::uint32_t signatureOffset = 0;
    std::uint32_t flags = 0;
};

struct BitCodecInfo {
    std::uint64_t id = 0;
    std::string name;
    bool decoder = false;
    bool encoder = false;
    std::uint32_t packStreams = 0;
    std::uint32_t unpackStreams = 0;
    std::string description;
    bool isFilter = false;
    bool isExternal = false;
};

} // namespace bit7z

#endif // BITFORMATINFO_HPP
