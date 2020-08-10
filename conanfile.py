from conans import ConanFile, CMake, tools


class DarknetConan(ConanFile):
    name = "darknet"
    version = "master"
    license = "YOLO"
    #author = "<Put your name here> <And your email here>"
    url = "https://github.com/omaralvarez/conan-darknet"
    repo_url = "https://github.com/AlexeyAB/darknet"
    description = "Windows and Linux version of Darknet Yolo v3 & v2 Neural Networks for object detection (Tensor Cores are used)"
    topics = ("dnn", "deep-learning", "object-detection")
    settings = "os", "compiler", "build_type", "arch"
    options = { "shared": [True, False], 
                "opencv": [True, False],
                "cuda": [True, False],
                "cudnn": [True, False],
                "half": [True, False],
                "cpp": [True, False] }
    default_options = { "shared": True,
                        "opencv": False,
                        "cuda": True,
                        "cudnn": False,
                        "half": False,
                        "cpp": False }
    generators = "cmake"

    def source(self):
        self.run("git clone %s dn" % (self.repo_url))
    
    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions['ENABLE_OPENCV'] = self.options.opencv
        cmake.definitions['ENABLE_CUDA'] = self.options.cuda
        cmake.definitions['ENABLE_CUDNN'] = self.options.cudnn
        cmake.definitions['ENABLE_CUDNN_HALF'] = self.options.half
        cmake.definitions['BUILD_AS_CPP'] = self.options.cpp
        cmake.definitions['ENABLE_ZED_CAMERA'] = False
        cmake.configure(source_folder="dn")
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
    
    def package_info(self):
        self.cpp_info.libs = ["darknet"]
