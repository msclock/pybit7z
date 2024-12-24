#include <pybind11/pybind11.h>

#include "_core.hpp"

namespace py = pybind11;

PYBIND11_MODULE(_core, m) {
    m.doc() = R"pbdoc(
      Pybind11 _core plugin
      -----------------------
      .. currentmodule:: _core
  )pbdoc";

    m.def("version", []() { return _core::ProjectVersion(); }, R"pbdoc(
      The _core plugin version.
  )pbdoc");

    m.attr("default_lib7zip") = _core::default_lib7zip;
}
