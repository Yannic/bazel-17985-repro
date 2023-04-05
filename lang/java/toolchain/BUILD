load("@bazel_tools//tools/jdk:default_java_toolchain.bzl", "default_java_toolchain")

default_java_toolchain(
    name = "java11_impl",
    oneversion = "//lang/java/oneversion:oneversion",
    oneversion_whitelist = "oneversion_allowlist.json",
    source_version = "17",
    target_version = "17",
)
