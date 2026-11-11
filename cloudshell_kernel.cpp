#include <iostream>
#include <cstdint>
#include <cstring>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
#include <iomanip>

#pragma pack(push, 1)
struct ApertureKernelState {
    uint32_t tower[25][7];
    uint8_t  switches[25];
    uint64_t generationCount;
    uint64_t stateRootHash;
};
#pragma pack(pop)

uint64_t fnv1a_hash(const ApertureKernelState* st) {
    uint64_t h = 14695981039346656037ULL;
    const uint8_t* raw = reinterpret_cast<const uint8_t*>(st);
    for (size_t i = 0; i < 725; ++i) {
        h ^= raw[i];
        h *= 1099511628211ULL;
    }
    return h;
}

void run_compute_cycle(ApertureKernelState* st) {
    std::memset(st, 0, sizeof(ApertureKernelState));
    uint32_t seed[7] = {15000, 8000, 50000, 35000, 6000, 4000, 20000};
    std::memcpy(st->tower[0], seed, sizeof(seed));
    st->switches[0] = 0x3F;

    for (int g = 0; g < 8; ++g) {
        for (int z = 1; z < 12; ++z) {
            uint32_t avg = (st->tower[z-1][1] + st->tower[z-1][2] + st->tower[z-1][3] +
                            st->tower[z-1][4] + st->tower[z-1][5] + st->tower[z-1][6]) / 6;
            st->tower[z][0] = (st->tower[z-1][0] + avg) / 2;
            for (int i = 1; i < 7; ++i)
                st->tower[z][i] = (st->tower[z-1][i] + st->tower[z][0]) / 2;
            st->switches[z] = 0x3F;
        }
        for (int z = 17; z <= 24; ++z) {
            uint32_t sum = 0;
            for (int i = 1; i < 7; ++i) {
                uint32_t d = (st->tower[11][i] > st->tower[11][0])
                           ? (st->tower[11][i] - st->tower[11][0]) * 2 : 0;
                st->tower[z][i] += d;
                sum += st->tower[z][i];
            }
            st->tower[z][0] = sum / 6;
            st->switches[z] = 0x3F;
        }
        for (int i = 0; i < 7; ++i)
            st->tower[0][i] += st->tower[24][i] / 4;
        st->generationCount++;
    }

    for (int z = 0; z < 25; ++z) {
        if (z == 12) continue;
        for (int i = 0; i < 7; ++i)
            st->tower[12][i] += st->tower[z][i];
    }
    st->switches[12] = 0x3F;
    st->stateRootHash = fnv1a_hash(st);
}

int main() {
    int fd = open("state_kernel.bin", O_RDWR | O_CREAT, 0644);
    if (fd < 0 || ftruncate(fd, sizeof(ApertureKernelState)) != 0) return 1;
    auto* state = static_cast<ApertureKernelState*>(
        mmap(nullptr, sizeof(ApertureKernelState), PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0)
    );
    run_compute_cycle(state);
    msync(state, sizeof(ApertureKernelState), MS_SYNC);

    std::cout << "[KERNEL RESTORED] Root: 0x" << std::hex << state->stateRootHash << std::dec << "\n[Z0]: [";
    for (int i = 0; i < 7; ++i)
        std::cout << state->tower[12][i] << (i < 6 ? ", " : "]\n");

    munmap(state, sizeof(ApertureKernelState));
    close(fd);
    return 0;
}
