---
description: "Plan Pro: Outcome-focused feature planning with impact analysis, risk matrix, bite-sized tasks, and TDD granularity"
skills: { required: [], contextual: [auto] }
success_criteria: "Understanding lock passed, plan approved by user, bite-sized tasks broken down, saved to .domyh/plans/"
---

# /plan — Outcome-Focused Feature Planning

## 🛡️ [GATE 0: PRE-FLIGHT PLANNING RULES — BẮT BUỘC ĐỌC TRƯỚC KHI LẬP KẾ HOẠCH]

1. **EVIDENCE-BASED DESIGN**: Mọi quyết định thiết kế và lựa chọn công nghệ BẮT BUỘC phải dựa trên khảo sát thực tế codebase (`hsa_search`, `hsa_explore`, `view_file`). Không đoán mò kiến trúc.
2. **UNDERSTANDING LOCK MANDATE**: BẮT BUỘC chốt "Khóa Hiểu Biết" (Understanding Lock) với User ở Phase 1 trước khi bước vào Phase 3 (Thiết kế chi tiết).
3. **SCOPE CREEP GUARD**: Nếu phát hiện yêu cầu mới hoặc ý tưởng mở rộng trong quá trình lập kế hoạch ➔ Đưa ngay vào danh mục **Scope OUT**, tuyệt đối không tự ý mở rộng phạm vi ("no scope creep").
4. **BITE-SIZED TASK GRANULARITY**: Mỗi bước trong kế hoạch phải là **một hành động nguyên tử (2 - 5 phút)**, chỉ rõ đường dẫn file chính xác (`file:line`), code mẫu hoàn chỉnh và lệnh chạy thực tế.
5. **TDD / TEST-FIRST PRIORITY**: Với các tính năng nghiệp vụ logic, bắt buộc thiết kế theo quy trình Test-First: `Viết Test (RED) ➔ Implement (GREEN) ➔ Refactor ➔ Commit`.
6. **STOP FOR APPROVAL**: Kế hoạch phải được User bấm duyệt chính thức trước khi chuyển sang giai đoạn thực thi mã nguồn `/code`.

---

## 🔄 7-PHASE SYSTEMATIC PLAN FLOW

### PHASE 0: DEEP INTERVIEW (Phỏng vấn Đào sâu Bối cảnh)
*   *Bỏ qua nếu yêu cầu của User đã đầy đủ và rõ ràng*.
*   Nếu còn mơ hồ: Hỏi **1 câu hỏi trọng tâm mỗi lượt** (không spam nhiều câu hỏi làm quá tải User).
*   Đưa ra 2 - 3 phương án lựa chọn kèm Trade-offs để User chọn hướng.

### PHASE 1: UNDERSTAND & UNDERSTANDING LOCK (Khóa Hiểu Biết — Hard Gate)
*   Khởi tạo phiên: `hsa_session(action="intent", focus="plan: {feature}")`.
*   Khảo sát bối cảnh: `hsa_detect(stack)`, `hsa_explore(repo_map)`.
*   **🔒 UNDERSTANDING LOCK**: Tóm tắt ngắn gọn 6 điểm mấu chốt:
    1.  **Mục tiêu (Goal)**: [1 câu duy nhất]
    2.  **Đối tượng & Quy mô**: [Ai sử dụng, tải dự kiến]
    3.  **Ràng buộc kỹ thuật (Constraints)**: [Ngôn ngữ, framework, chuẩn bảo mật]
    4.  **Phạm vi THỰC HIỆN (Scope IN)**: [Danh sách tính năng cụ thể]
    5.  **Phạm vi KHÔNG LÀM (Scope OUT)**: [Các tính năng hoãn lại để chống phình scope]
    6.  **Tiêu chí Nghiệm thu (Success Criteria)**: [Điều kiện để xem là hoàn thành]
*   ⛔ **HỎI USER**: *"Bản tóm tắt hiểu biết này đã hoàn toàn chính xác chưa? Có điểm nào cần bổ sung/thay đổi không?"* ➔ **Chỉ tiếp tục khi User xác nhận OK.**

### PHASE 2: IMPACT ANALYSIS & RISK MATRIX (Phân tích Tác động & Rủi ro)
*   Đánh giá độ phức tạp: `XS (<1h)` | `S (1-4h)` | `M (1-2d)` | `L (3-5d)` | `XL (>1w)`.
*   Liệt kê số lượng files ảnh hưởng, dependencies mới, breaking changes tiềm ẩn.
*   Xây dựng bảng Ma trận Rủi ro (Risk Likelihood $\times$ Impact).

### PHASE 3: TECHNICAL DESIGN & CONTRACTS (Thiết kế Kỹ thuật & Giao diện)
*   Thiết kế kiến trúc hệ thống, sơ đồ quan hệ dữ liệu (Data Models), API Contracts / Interfaces.
*   Đề xuất phương án tối giản nhất (YAGNI).

### PHASE 4: BITE-SIZED TASK BREAKDOWN (Bẻ nhỏ Tác vụ theo Hành động Nguyên tử)
*   Chia nhỏ kế hoạch thành từng Task độc lập. Mỗi task gồm các bước nhỏ có Checkbox (`- [ ]`).
*   Tuân thủ cấu trúc mẫu bên dưới.

### PHASE 5: VALIDATE & USER CONFIRMATION GATE (Nghiệm thu Kế hoạch — STOP)
*   Trình bày toàn bộ bản kế hoạch cho User.
*   ⛔ **STOP**: Tạm dừng chờ User duyệt kế hoạch trước khi chuyển sang `/code`.

### PHASE 6: PERSIST & SAVE (Lưu trữ Kế hoạch)
*   Lưu kế hoạch vào thư mục: `.domyh/plans/YYYY-MM-DD_{feature_slug}/plan.md`.
*   Nếu phạm vi $\ge$ Size L: Lưu thêm `impact.md` và `tasks.md`.
*   Cập nhật `active_plan` trong `.agent/memory/state.json`.

---

## 🧱 CẤU TRÚC MẪU TASK NGUYÊN TỬ (BITE-SIZED TASK FORMAT)

```markdown
### Task 1: [Tên Module / Thành phần]
- **Files liên quan**: Tạo mới: `src/auth/token.ts` | Sửa đổi: `src/server.ts:45-60` | Tests: `tests/auth.test.ts`
- **Mục tiêu**: Xử lý logic xác thực JWT token và mã hóa khóa bí mật.

- [ ] **Step 1 (Test RED)**: Viết test case kiểm tra token hết hạn trong `tests/auth.test.ts`.
- [ ] **Step 2 (Lệnh chạy Test)**: Chạy `pnpm test tests/auth.test.ts` (Xác nhận test FAIL).
- [ ] **Step 3 (Implement GREEN)**: Thêm hàm `verifyToken()` vào `src/auth/token.ts`.
- [ ] **Step 4 (Read-Back Diff)**: Gọi `view_file` đọc lại `src/auth/token.ts` kiểm tra cú pháp.
- [ ] **Step 5 (Verify PASS)**: Chạy lại `pnpm test tests/auth.test.ts` (Xác nhận test PASS 100%).
- [ ] **Step 6 (Commit)**: `git commit -m "feat(auth): add jwt token verification"`.
```

---

## ⚡ SUB-COMMANDS

| Lệnh | Mô tả |
|:-----|:------|
| `/plan [feature]` | Quy trình lập kế hoạch đầy đủ (7 Phases) |
| `/plan quick [feature]` | Lập kế hoạch nhanh cho task nhỏ (bỏ qua Phase 0) |
| `/plan estimate [feature]` | Đánh giá nỗ lực và kích thước task (RICE / T-shirt sizing) |
| `/plan list` | Xem danh sách các plan đã lưu trong `.domyh/plans/` |
| `/plan open [slug]` | Mở và tiếp tục thực thi một plan đã lưu |

---

## 🎯 [GATE 9: POST-FLIGHT PLANNING CHECKLIST — BẮT BUỘC ĐỐI SOÁT TRƯỚC KHI BÀN GIAO KẾ HOẠCH]

Trước khi bàn giao bản kế hoạch cho User, Agent BẮT BUỘC tự kiểm tra 5 câu hỏi vàng:
1.  ✅ **Khóa Hiểu Biết (Understanding Lock) đã được User xác nhận chưa?**
2.  ✅ **Mọi tác vụ đã được bẻ nhỏ thành từng bước nguyên tử (2-5 phút, kèm file:line và lệnh chạy cụ thể) chưa?**
3.  ✅ **Đã có danh mục Scope OUT để ngăn chặn triệt để hiện tượng phình phạm vi chưa?**
4.  ✅ **Các module logic đã được thiết kế theo quy trình Test-First / TDD chưa?**
5.  ✅ **Kế hoạch đã được lưu đầy đủ vào `.domyh/plans/` và STOP chờ User bấm duyệt chưa?**
