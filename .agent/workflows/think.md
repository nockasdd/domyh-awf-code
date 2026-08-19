---
description: "Think Pro: 6 reasoning methods, 5 tiers, multi-mode analysis with evidence and balanced trade-offs"
skills: { required: [], contextual: [] }
success_criteria: "Analysis complete, evidence cited with file:line, confidence scored, trade-offs stated, user direction confirmed"
---

# /think — Deep Reasoning & Architectural Analysis

## 🛡️ [GATE 0: PRE-FLIGHT REASONING RULES — BẮT BUỘC ĐỌC TRƯỚC KHI SUY NGHĨ]

1. **EVIDENCE MANDATE**: Mọi nhận định, so sánh và đề xuất BẮT BUỘC phải dẫn chứng bằng chứng thực tế (`file:line`, kết quả benchmark, tài liệu kỹ thuật). Tuyệt đối không phán đoán cảm tính.
2. **MANDATORY CONFIDENCE SCORE**: Mọi đề xuất và phương án BẮT BUỘC phải kèm điểm độ tin cậy từ `1 - 10` kèm lý do định lượng.
3. **BALANCED TRADE-OFFS**: Bắt buộc chỉ rõ cả hai mặt: Ưu điểm (Pros) VÀ Rủi ro/Hạn chế (Cons/Trade-offs). Tuyệt đối không phân tích phiến diện một chiều.
4. **SOCRATIC PROBING**: Tự phản biện các giả định ban đầu. Đặt câu hỏi: *"Điều gì sẽ xảy ra nếu giả định này sai? Có giải pháp nào đơn giản hơn 50% không?"*
5. **STOP AT STEP 5**: Dừng lại ở Bước 5 (Validate) để người dùng xác nhận định hướng trước khi chuyển sang giai đoạn `/plan` hoặc `/code`.

---

## 🔄 5-PHASE SYSTEMATIC THINK FLOW

### PHASE 1: CONTEXT & SCOPE TRACING (Bối cảnh & Dấu vết)
*   **Identify Intent**: Nhận diện vấn đề thuộc tầng kiến trúc, thuật toán, debug hay lựa chọn công nghệ.
*   **Codebase Scan**: Dùng `hsa_search(query)` hoặc `hsa_trace_flow` để nắm cấu trúc hiện tại, các phụ thuộc và ràng buộc của dự án.
*   **Select Reasoning Method**: Tự động chọn phương pháp phân tích phù hợp từ bảng bên dưới.

### PHASE 2: BRAINSTORM & SOCRATIC HYPOTHESIS (Động não & Giả thuyết)
*   Áp dụng phương pháp đã chọn (Tree of Thought, Six Thinking Hats, SCAMPER, Starbursting).
*   Tạo ra ít nhất **2 - 3 phương án khả thi** (bao gồm phương án giữ nguyên/tối giản nhất).
*   Liệt kê các câu hỏi phản biện cốt lõi và các góc nhìn đối lập (Devil's Advocate).

### PHASE 3: EVALUATION & TRADE-OFF MATRIX (Đánh giá & Ma trận Đánh đổi)
*   Chấm điểm từng phương án dựa trên các tiêu chí: Tính đúng đắn, Độ phức tạp (Complexity), Khả năng bảo trì, Hiệu năng và Rủi ro.
*   Trình bày bảng ma trận so sánh trực quan (Weighted Matrix hoặc Pro/Con Table).

### PHASE 4: DECISION & ACTIONABLE MITIGATION (Ra quyết định & Kế hoạch Giảm thiểu)
*   Đưa ra **Khuyến nghị Tối ưu (Recommendation)** với điểm số Confidence Score rõ ràng.
*   Xây dựng bảng kế hoạch giảm thiểu rủi ro: `[Rủi ro tiềm ẩn] ➔ [Giải pháp khắc phục cụ thể]`.

### PHASE 5: VALIDATE & USER CONFIRMATION (Xác nhận Định hướng — STOP)
*   Trình bày tóm tắt quyết định và lý do cho User.
*   ⛔ **STOP**: Tạm dừng để người dùng duyệt định hướng trước khi bắt tay vào lập kế hoạch `/plan` hoặc viết mã `/code`.

---

## 🧭 PHƯƠNG PHÁP TỰ ĐỘNG CHỌN (AUTO-SELECT REASONING METHOD)

| Từ khóa / Tình huống | Phương pháp Đề xuất | Cấp độ | Mục tiêu |
|:---------------------|:-------------------|:------:|:---------|
| `architecture`, `design`, `migrate`, `scale` | **Tree of Thought (3 paths)** | Tier 3 | Khảo sát 3 nhánh kiến trúc độc lập và đánh giá độ sâu |
| `compare`, `choose`, `tradeoff`, `vs` | **Six Thinking Hats / Weighted Matrix** | Tier 2 | Đánh giá 6 lăng kính (Dữ liệu, Rủi ro, Lợi ích, Sáng tạo...) |
| `fix`, `solve`, `debug`, `stuck` | **Reverse Analysis + SCAMPER** | Tier 4 | Đảo ngược vấn đề, thay thế/kết hợp/loại bỏ để gỡ tắc nghẽn |
| `plan`, `feature`, `roadmap` | **Starbursting (5W1H)** | Tier 5 | Mở rộng góc nhìn qua Who, What, Where, When, Why, How |
| `brainstorm`, `ideas`, `options` | **Mind Mapping** | Tier 1 | Mở rộng tối đa các ý tưởng sáng tạo không phán xét |
| *Mặc định (Không khớp)* | **Structured Analysis** | Tier 2 | Phân tích cấu trúc tiêu chuẩn: Hiện trạng ➔ Vấn đề ➔ Giải pháp |

---

## ⚡ SUB-COMMANDS

| Lệnh | Phương pháp | Ngân sách Token |
|:-----|:------------|:---------------:|
| `/think [topic]` | Auto-select theo ngữ cảnh | 2-4K |
| `/think brainstorm [topic]` | Mind Mapping | 1-2K |
| `/think analyze [decision]` | Six Thinking Hats | 4-6K |
| `/think deep [architecture]` | Tree of Thought (3 paths) | 8-15K |
| `/think solve [problem]` | Reverse + SCAMPER | 3-5K |
| `/think plan [feature]` | Starbursting (5W1H) | 3-5K |
| `/think tradeoff [options]` | Weighted Matrix Table | 2-4K |

*Flags khả dụng*: `--explore` (chỉ mở rộng ý tưởng) | `--debate` (tranh biện 2 mặt) | `--plan` (kèm lộ trình hành động)

---

## 📋 MẪU ĐỊNH DẠNG KẾT QUẢ ĐỀ XUẤT (OUTPUT FORMAT)

```markdown
### 🎯 Khuyến nghị: [Phương án Lựa chọn] (Confidence: X/10)
- **Lý do lựa chọn (Rationale)**: [Dẫn chứng kỹ thuật từ codebase, benchmark, best practice]
- **Ma trận Đánh đổi (Trade-offs)**: [Những gì được và những gì phải chấp nhận hy sinh]
- **Rủi ro & Kế hoạch Giảm thiểu**:
  * ⚠️ *Rủi ro 1*: [Mô tả] ➔ 🛡️ *Giải pháp*: [Cách khắc phục]
  * ⚠️ *Rủi ro 2*: [Mô tả] ➔ 🛡️ *Giải pháp*: [Cách khắc phục]
```

---

## 🎯 [GATE 9: POST-FLIGHT THINKING CHECKLIST — BẮT BUỘC ĐỐI SOÁT TRƯỚC KHI TRẢ LỜI]

Trước khi hoàn tất response gửi cho User, Agent BẮT BUỘC tự kiểm tra 5 tiêu chuẩn vàng:
1.  ✅ **Tôi đã dẫn chứng bằng chứng thực tế từ codebase/tài liệu chưa?** *(Không phán đoán mò)*
2.  ✅ **Mọi phương án đề xuất có điểm Confidence Score (1-10) chưa?**
3.  ✅ **Tôi đã trình bày Trade-offs hai mặt khách quan chưa?** *(Không tô hồng giải pháp)*
4.  ✅ **Tôi đã có bảng Rủi ro & Cách giảm thiểu cụ thể chưa?**
5.  ✅ **Tôi đã DỪNG LẠI ở Bước 5 để chờ User xác nhận định hướng chưa?**
