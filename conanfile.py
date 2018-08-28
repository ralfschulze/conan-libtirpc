#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class LibnameConan(ConanFile):
    name = "libtirpc"
    version = "1.1.4"
    description = "Libtirpc is a port of Suns Transport-Independent RPC library to Linux. It's being developed by the Bull GNU/Linux NFSv4 project."
    url = "https://github.com/bincrafters/conan-libtirpc"
    homepage = "https://sourceforge.net/projects/libtirpc/"
    author = "Bincrafters <bincrafters@gmail.com>"
    # Indicates License type of the packaged library
    license = "BSD"

    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]
    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"

    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    # Use version ranges for dependencies unless there's a reason not to
    # Update 2/9/18 - Per conan team, ranges are slow to resolve.
    # So, with libs like zlib, updates are very rare, so we now use static version

    def source(self):
        source_url = " https://downloads.sourceforge.net/project/libtirpc/libtirpc"
        tools.get("{0}/{1}/libtirpc-{1}.tar.bz2".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version

        #Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_subfolder)

    def configure_autotools(self):
        args = ['--enable-shared=yes', '--enable-static=no'] if self.options.shared else ['--enable-shared=no', '--enable-static=yes']
        autotools = AutoToolsBuildEnvironment(self)
        autotools.configure(configure_dir=self.source_subfolder, args=args)
        return autotools

    def build(self):
        autotools = self.configure_autotools()
        autotools.make()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self.source_subfolder)
        autotools = self.configure_autotools()
        autotools.install()
        # If the CMakeLists.txt has a proper install method, the steps below may be redundant
        # If so, you can just remove the lines below
        include_folder = os.path.join(self.source_subfolder, "tirpc")
        self.copy(pattern="*", dst="include", src=include_folder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
