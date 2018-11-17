# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class LibtirpcConan(ConanFile):
    name = "libtirpc"
    version = "1.1.4"
    description = "Libtirpc is a port of Suns Transport-Independent RPC library to Linux. It's being developed by the Bull GNU/Linux NFSv4 project."
    topics = ("conan", "tirpc", "RPC", "sun", "transport", "independent")
    url = "https://github.com/bincrafters/conan-libtirpc"
    homepage = "https://sourceforge.net/projects/libtirpc/"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "BSD"
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
    _source_subfolder = "sources"

    def configure(self):
        if self.settings.compiler in ("gcc", "clang"):
            del self.settings.compiler.libcxx

    def source(self):
        url = "https://sourceforge.net/projects/{name}/files/{name}/{version}/{name}-{version}.tar.bz2".format(
            name=self.name, version=self.version
        )
        sha256 = "2ca529f02292e10c158562295a1ffd95d2ce8af97820e3534fe1b0e3aec7561d"
        tools.get(url, sha256=sha256)
        os.rename("{}-{}".format(self.name, self.version), self._source_subfolder)

    def build(self):
        conf_args = [
            "--disable-gssapi",
            "--enable-ipv6",
            "--enable-shared" if self.options.shared else "--disable-shared",
            "--disable-static" if self.options.shared else "--enable-static",
            "--with-pic" if self.options.fPIC else "--without-pic",
        ]
        autotools = AutoToolsBuildEnvironment(self)
        autotools.configure(configure_dir=os.path.join(self.source_folder, self._source_subfolder), args=conf_args)
        autotools.make()

    def package(self):
        with tools.chdir(self.build_folder):
            autotools = AutoToolsBuildEnvironment(self)
            autotools.install()

    def package_info(self):
        self.cpp_info.includedirs = ["include", "include/tirpc"]
        self.cpp_info.libs = ["tirpc", "pthread"]
