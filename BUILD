java_import(
    name = "error_prone_annotations",
    jars = [
        "error_prone_annotations-2.11.0.jar",
    ],
)

java_test(
    name = "ReproTest",
    test_class = "ReproTest",
    srcs = [
        "ReproTest.java",
    ],
    deps = [
        ":error_prone_annotations",
    ],
)
