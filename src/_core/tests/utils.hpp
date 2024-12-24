#pragma once

#include <filesystem>
#include <fstream>
#include <iomanip>
#include <random>
#include <sstream>
#include <string>

#include <gtest/gtest.h>

#ifndef TESTS_DIR
#error "TESTS_DIR is not defined"
#endif

#define TEST_DATA_DIR_NAME "test_data"
#define TEST_TEMP_DIR_NAME "tmp"

namespace test {
namespace utils {
class rc_dir_test : public ::testing::Test {
protected:
    std::filesystem::path tests_dir{TESTS_DIR};
    std::filesystem::path test_data_dir_;
    std::filesystem::path system_test_tmp_dir_;

    void SetUp() override {
        this->test_data_dir_ = this->tests_dir / TEST_DATA_DIR_NAME;
        std::mt19937_64 gen(std::random_device{}());
        std::uniform_int_distribution<> dis(1000, 9999);
        auto suffix_dir_name = std::to_string(dis(gen)) + std::to_string(dis(gen));
        this->system_test_tmp_dir_ = this->test_data_dir_ / TEST_TEMP_DIR_NAME / suffix_dir_name;
        std::filesystem::create_directories(system_test_tmp_dir_);
    }

    void TearDown() override { std::filesystem::remove_all(system_test_tmp_dir_); }
};
} // namespace utils
} // namespace test
