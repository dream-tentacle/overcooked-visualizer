#include <cstdlib>
#include <cstring>
#include <fcntl.h>
#include <iostream>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#ifdef _WIN32
#include <direct.h>
#define mkdir(path, mode) _mkdir(path)
#endif

// modify this as your desired
static const char *tmp_root = "/tmp";

static int init_pipe() {
    std::string pipe_path = tmp_root + std::string("/visualize/pipe");
    int fd = open(pipe_path.c_str(), O_WRONLY, 0666);
    if (fd == -1) {
        perror("open pipe failed");
        exit(1);
    }
    return fd;
}

static int init_log() {
    // detect whether or not tmp_root/pipe exists
    struct stat st;
    std::string vis_root = tmp_root + std::string("/visualize");
    if (stat(vis_root.c_str(), &st) == -1) {
        if (mkdir(vis_root.c_str(), 0777) == -1) {
            perror("mkdir failed");
            exit(1);
        }
    }
    std::string log_name = tmp_root + std::string("/visualize/log.txt");
    int fd = open(log_name.c_str(), O_WRONLY | O_CREAT, 0666);
    if (fd == -1) {
        perror("open log failed");
        exit(1);
    }
    return fd;
}

static void write_visualize(const char *msg, int fd) {
    if (fd == -1) {
        std::cerr << "Error: open file failed" << std::endl;
        exit(1);
    }
    write(fd, msg, strlen(msg));
}

static int vis_fd;
void init_visualize(bool mode) {
    if (mode) {
        // pipe
        vis_fd = init_pipe();
    } else {
        // log
        vis_fd = init_log();
    }
}
// clang-format off
void perframe_visualize
    (double p1x, double p1y, double v1x, double v1y, int a1x, int a1y,
     double p2x, double p2y, double v2x, double v2y, int a2x, int a2y) {
    char *msg = new char[1024];
    sprintf(msg, "%lf %lf %lf %lf %d %d %lf %lf %lf %lf %d %d\n", 
            p1x, p1y, v1x, v1y, a1x, a1y, p2x, p2y, v2x, v2y, a2x, a2y);
    write_visualize(msg, vis_fd);
    delete[] msg;
}
// clang-format on
