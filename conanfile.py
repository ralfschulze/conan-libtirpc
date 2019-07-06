# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.errors import ConanInvalidConfiguration
import os


class LibtirpcConan(ConanFile):
    name = "libtirpc"
    version = "1.1.4"
    description = "Libtirpc is a port of Suns Transport-Independent RPC library to Linux"
    topics = ("conan", "tirpc", "RPC", "sun", "transport", "independent")
    url = "https://github.com/bincrafters/conan-libtirpc"
    homepage = "https://sourceforge.net/projects/libtirpc"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "BSD-3-Clause"
    exports = ["LICENSE.md"]
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }
    _source_subfolder = "source_subfolder"
    _autotools = None

    def configure(self):
        if self.settings.os != "Linux":
            raise ConanInvalidConfiguration("libtirpc is only supported for Linux")
        del self.settings.compiler.libcxx

    def source(self):
        url = "{homepage}/files/{name}/{version}/{name}-{version}.tar.bz2".format(
            homepage=self.homepage, name=self.name, version=self.version
        )
        sha256 = "2ca529f02292e10c158562295a1ffd95d2ce8af97820e3534fe1b0e3aec7561d"
        tools.get(url, sha256=sha256)
        os.rename("{}-{}".format(self.name, self.version), self._source_subfolder)

    def _configure_autotools(self):
        if not self._autotools:
            conf_args = [
                "--disable-gssapi",
                "--enable-ipv6",
                "--enable-shared" if self.options.shared else "--disable-shared",
                "--disable-static" if self.options.shared else "--enable-static",
                "--with-pic" if self.options.fPIC else "--without-pic",
            ]
            self._autotools = AutoToolsBuildEnvironment(self)
            self._autotools.configure(configure_dir=os.path.join(self.source_folder, self._source_subfolder), args=conf_args)
        return self._autotools

    def build(self):
        autotools = self._configure_autotools()
        autotools.make()

    def package(self):
        self.copy("COPYING", dst="licenses", src=self._source_subfolder)
        autotools = self._configure_autotools()
        autotools.install()
        tools.rmdir(os.path.join(self.package_folder, "share"))
        tools.rmdir(os.path.join(self.package_folder, "etc"))

    def package_info(self):
        self.cpp_info.includedirs = ["include", os.path.join("include", "tirpc")]
        self.cpp_info.libs = ["tirpc", "pthread"]
