---
description: "Write production-ready code with double-ended rules, pre-read trace, post-read verification, and plan alignment"
skills: { required: [coding-rules], contextual: [auto, domyh-design, tailwind] }
success_criteria: "Pre-read verified, surgical change applied, post-read confirmed, build/tests passed, plan aligned"
---

# /code — Production Coding Workflow

## 🛡️ [GATE 0: PRE-FLIGHT HARD RULES — BẮT BUỘC ĐỌC TRƯỚC KHI CODE]

1. **NO BLIND WRITING**: Tuyệt đối KHÔNG viết/sửa code khi chưa đọc file mục tiêu (`view_file` / `hsa_search`). Không dựa vào phán đoán.
2. **SURGICAL CHANGES**: Chỉ chạm vào các dòng thuộc phạm vi yêu cầu. Khớp 100% style/cú pháp/thụt lề hiện có. Không refactor ngoài phạm vi ("clean only your own mess").
3. **SIZE SAFETY**: Nếu thay đổi >50 dòng hoặc tạo >2 files mới ➔ BẮT BUỘC dừng lại xác nhận Implementation Plan với User.
4. **COMMENT POLICY**: Mặc định KHÔNG viết comment mô tả WHAT (code đã tự giải thích). Chỉ viết comment ngắn gọn cho WHY (ràng buộc kỹ thuật, workaround).
5. **READ-BACK MANDATE**: Sau KHI SỬA bất kỳ file nào, BẮT BUỘC phải đọc lại file (`view_file`) để đối soát diff trước khi chuyển bước.

---

## 🔄 6-PHASE SYSTEMATIC CODE FLOW

### PHASE 1: DISCOVER & ASSUMPTIONS (Khám phá & Xác định Giả định)
*   **Parse Intent**: Phân loại rõ ràng mục tiêu (`feature` | `bugfix` | `refactor` | `test` | `add`).
*   **Stack & Skill Detection**: Gọi `hsa_detect(stack)` và `hsa_search(query, action="skills")` để nạp các quy tắc và domain patterns phù hợp.
*   **UI Intent**: Nếu liên quan đến UI:
    *   Mới (T1): Nạp skill thiết kế UI.
    *   Chỉnh sửa (T2): Chạy phân tích design.
    *   Phức tạp (T3): Chuyển hướng sang workflow `/visualize`.
*   **Surface Assumptions**: Liệt kê rõ ràng phạm vi (Scope), định dạng (Format), công nghệ và các ràng buộc. STOP nếu chưa rõ yêu cầu.

### PHASE 2: PRE-READ & TRACE FLOW (Đọc trước & Lần vết Phụ thuộc)
*   **Locate Target**: Định vị chính xác file và khối mã nguồn cần chỉnh sửa.
*   **Pre-Reading**: Gọi `view_file` đọc toàn bộ ngữ cảnh xung quanh (bao gồm imports, interfaces, types, exports).
*   **Trace Flow (DRY Enforcement)**:
    *   Nếu sửa hàm/class: Chạy `hsa_trace_flow(entry, direction:"both")` hoặc grep callers để nắm toàn bộ các vị trí đang gọi hàm đó.
    *   Nếu tạo mới: Tìm kiếm hàm tương tự trong `utils/` / `shared/` / `lib/` để tái sử dụng trước khi tạo mới.
*   **Edge Cases Gate**: Xác định trước ít nhất 3 test cases và 2 edge cases cần bao phủ.

### PHASE 3: SURGICAL IMPLEMENTATION (Thực thi Phẫu thuật & TDD)
*   **TDD / Test-First**: Nếu là logic mới hoặc fix bug, viết test tái hiện lỗi (RED) trước khi viết code xử lý (GREEN).
*   **Precision Editing**:
    *   Sử dụng `replace_file_content` cho các khối thay đổi cục bộ trong file hiện có.
    *   Sử dụng `write_to_file` khi tạo mới file độc lập.
*   **YAGNI & Simplicity**: Viết lượng code tối thiểu giải quyết triệt để vấn đề. Không suy đoán tính năng cho tương lai ("no speculative features").

### PHASE 4: POST-EDIT READ-BACK & DIFF VERIFICATION (Đọc lại sau khi sửa)
*   **Mandatory Read-Back**: Ngay sau khi tool chỉnh sửa hoàn tất, BẮT BUỘC gọi `view_file` đọc lại đúng phạm vi dòng vừa sửa trong file thực tế.
*   **Diff Quality Checklist**:
    *   [ ] Cú pháp (syntax), dấu ngoặc và thụt lề (indentation) có chuẩn xác 100% không?
    *   [ ] Có vô tình làm mất/thay đổi dòng nào ngoài phạm vi yêu cầu không?
    *   [ ] Imports, types, biến số mới có được khai báo và export đầy đủ không?
    *   [ ] Có tuân thủ Comment Policy (không để lại comment thừa/version tag) không?

### PHASE 5: RUN EVIDENCE & TEST LOOP (Chạy Bằng chứng Thực tế)
*   **Execution Evidence**: Chạy các lệnh kiểm thử và biên dịch thực tế của dự án (`pnpm test`, `tsc --noEmit`, `pnpm build`, v.v.).
*   **Auto Test Loop**: Sửa ➔ Đọc lại ➔ Chạy lại (Tối đa 3 vòng lặp).
*   **Escalation Gate**: Nếu sau 3 lần vẫn thất bại ➔ STOP ngay lập tức, áp dụng SCAMPER phân tích nguyên nhân gốc rễ và báo cáo cho User, không đoán mò tiếp.

### PHASE 6: PLAN & RULES PRE-REPORT AUDIT (Đối soát Kế hoạch & Rules)
*   **Plan Alignment**: So sánh đối chiếu mã nguồn đã viết với từng mục trong yêu cầu ban đầu của User / Implementation Plan.
*   **Index Refresh**: Chạy `hsa_check_changes` để cập nhật Merkle tree và BM25F index cho codebase.
*   **Session Persistence**: Cập nhật tóm tắt vào phiên làm việc qua `hsa_session(action="persist")`.

---

## ⚡ SUB-COMMANDS

| Lệnh | Chế độ | Mô tả |
|:-----|:-------|:------|
| `/code [task]` | Create / General | Viết tính năng mới hoặc phát triển mã nguồn hoàn chỉnh |
| `/code fix [issue]` | Bugfix | Sửa lỗi với quy trình: Reproduce ➔ Trace ➔ Surgical Fix ➔ Verify |
| `/code improve [area]` | Refactor | Tái cấu trúc mã nguồn (yêu cầu giữ nguyên 100% test pass) |
| `/code add [feature]` | Feature Extension | Bổ sung module/endpoint/component mới |
| `/code test [feature]` | Test Suite | Viết unit tests, integration tests, E2E tests |

---

## 🤝 CASCADE & SUBAGENT DELEGATION

*   **Tự động Cascade** (Complexity Score $\ge$ 6.5 hoặc scope > 200 dòng): Phân rã nhiệm vụ cho subagents chuyên biệt.
*   **Đề xuất Cascade** (Score 4.0 – 6.5 hoặc scope 100 – 200 dòng): Đề xuất kế hoạch với User trước khi chia nhỏ.

---

## 🎯 [GATE 9: POST-FLIGHT CLOSING CHECKLIST — BẮT BUỘC ĐỐI SOÁT TRƯỚC KHI TRẢ LỜI]

Trước khi xuất bản câu trả lời cuối cùng cho User, Agent BẮT BUỘC tự kiểm tra 5 câu hỏi vàng:
1.  ✅ **Tôi đã đọc file TRƯỚC khi sửa chưa?** *(Có dẫn chứng file:line thực tế)*
2.  ✅ **Tôi đã đọc lại file SAU khi sửa chưa?** *(Đã xác nhận diff sạch và cú pháp chuẩn)*
3.  ✅ **Tôi đã chạy lệnh test/build thực tế để lấy bằng chứng chưa?** *(Không dùng từ "chắc là hoạt động")*
4.  ✅ **Mọi thay đổi có bám sát 100% yêu cầu trong Plan không?** *(Không phát sinh code thừa ngoài scope)*
5.  ✅ **Đã tuân thủ nguyên tắc Surgical Change và Comment Policy chưa?**
