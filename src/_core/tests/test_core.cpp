#include "gtest/gtest.h"

#include "_core.hpp"
#include "pybit7z.hpp"
#include "utils.hpp"

TEST(_core, version) {
    auto version = _core::ProjectVersion();
    EXPECT_TRUE(!version.empty());
}

using _core_pybit7z_test = test::utils::rc_dir_test;

TEST_F(_core_pybit7z_test, compress) {
    using namespace bit7z;

    BitFileCompressor compressor{_core::Bit7zipSingleton::getInstance(), BitFormat::Zip};

    std::vector<std::string> files = {this->tests_dir.string() + "/test_core.cpp"};

    // Creating a simple zip archive
    compressor.compress(files, this->system_test_tmp_dir_.string() + "/output_archive.zip");

    // Creating a zip archive with a custom directory structure
    std::map<std::string, std::string> files_map = {
        {this->tests_dir.string() + "/test_core.cpp", "alias/path/test_core.cpp"}};
    compressor.compress(files_map, this->system_test_tmp_dir_.string() + "/custom_dir_archive.zip");

    // Compressing a directory
    compressor.compressDirectory(this->tests_dir.string() + "/.." + "/src",
                                 this->system_test_tmp_dir_.string() + "/dir_archive.zip");

    // Creating an encrypted zip archive of two files
    compressor.setPassword("password");
    compressor.compressFiles(files, this->system_test_tmp_dir_.string() + "/protected_archive.zip");

    // Updating an existing zip archive
    compressor.setUpdateMode(UpdateMode::Append);
    compressor.compressFiles(files, this->system_test_tmp_dir_.string() + "/existing_archive.zip");

    // Compressing a single file into a buffer
    std::vector<bit7z::byte_t> buffer;
    BitFileCompressor compressor2{_core::Bit7zipSingleton::getInstance(), BitFormat::BZip2};
    compressor2.compressFile(files[0], buffer);
}

TEST_F(_core_pybit7z_test, archive_writer) {
    using namespace bit7z;

    BitArchiveWriter archive{_core::Bit7zipSingleton::getInstance(), BitFormat::SevenZip};

    // Adding the items to be compressed (no compression is performed here)
    archive.addFile(this->tests_dir.string() + "/test_core.cpp");
    archive.addDirectory(this->tests_dir.string() + "/.." + "/include");
    archive.addDirectory(this->tests_dir.string() + "/.." + "/src");

    // Compressing the added items to the output archive
    archive.compressTo(this->system_test_tmp_dir_.string() + "/output.7z");
}

TEST_F(_core_pybit7z_test, bzip) {
    using namespace bit7z;

    BitFileCompressor compressor{_core::Bit7zipSingleton::getInstance(), BitFormat::BZip2};
    BitFileExtractor extractor{_core::Bit7zipSingleton::getInstance(), BitFormat::BZip2};

    auto file = this->tests_dir / "test_core.cpp";
    std::vector<std::string> files = {file.string()};

    auto archive_file_name = file.filename().string() + ".bz2";
    // Bzip requires output file to have the same name as  the file entry
    compressor.compress(files, this->system_test_tmp_dir_.string() + "/" + archive_file_name);

    extractor.extract(this->system_test_tmp_dir_.string() + "/" + archive_file_name,
                      this->system_test_tmp_dir_.string() + "/" + archive_file_name + ".extracted");
    EXPECT_TRUE(std::filesystem::exists(this->system_test_tmp_dir_.string() + "/" + archive_file_name + ".extracted"
                                        + "/" + file.filename().string()));
}
