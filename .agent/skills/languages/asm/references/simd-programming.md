## ⚡ SIMD Programming

### Intrinsics vs Inline ASM Decision

```yaml
recommendation:
  use_intrinsics:
    - Portable across compilers
    - Compiler can optimize around them
    - Easier to maintain
    - Better for SSE/AVX/AVX-512

  use_inline_asm:
    - CPU-specific features not in intrinsics
    - Precise instruction control needed
    - Very small, critical code paths
```

### SSE/AVX Intrinsics Example

```c
#include <immintrin.h>

// Add 8 floats using AVX
void vector_add_avx(float* result, const float* a, const float* b) {
    __m256 va = _mm256_load_ps(a);    // Load 8 floats from a
    __m256 vb = _mm256_load_ps(b);    // Load 8 floats from b
    __m256 vr = _mm256_add_ps(va, vb); // Add
    _mm256_store_ps(result, vr);       // Store result
}

// Dot product using SSE
float dot_product_sse(const float* a, const float* b, int n) {
    __m128 sum = _mm_setzero_ps();
    for (int i = 0; i < n; i += 4) {
        __m128 va = _mm_load_ps(&a[i]);
        __m128 vb = _mm_load_ps(&b[i]);
        sum = _mm_add_ps(sum, _mm_mul_ps(va, vb));
    }
    // Horizontal add
    sum = _mm_hadd_ps(sum, sum);
    sum = _mm_hadd_ps(sum, sum);
    return _mm_cvtss_f32(sum);
}
```

### Runtime CPU Feature Detection

```c
#include <cpuid.h>  // GCC/Clang

bool has_avx2(void) {
    unsigned int eax, ebx, ecx, edx;
    __cpuid(7, eax, ebx, ecx, edx);
    return (ebx & (1 << 5)) != 0;  // AVX2 bit
}

// Dispatch based on CPU features
void process_data(float* data, int n) {
    if (has_avx2()) {
        process_avx2(data, n);
    } else if (has_sse4()) {
        process_sse4(data, n);
    } else {
        process_scalar(data, n);
    }
}
```

### ARM64 NEON Intrinsics

```c
#include <arm_neon.h>

// Add 4 floats using NEON
void vector_add_neon(float* result, const float* a, const float* b) {
    float32x4_t va = vld1q_f32(a);     // Load 4 floats
    float32x4_t vb = vld1q_f32(b);     // Load 4 floats
    float32x4_t vr = vaddq_f32(va, vb); // Add
    vst1q_f32(result, vr);              // Store
}

// Horizontal sum
float horizontal_sum_neon(float32x4_t v) {
    float32x2_t sum = vadd_f32(vget_low_f32(v), vget_high_f32(v));
    sum = vpadd_f32(sum, sum);
    return vget_lane_f32(sum, 0);
}
```

---
