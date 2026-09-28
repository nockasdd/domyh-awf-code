---
description: Bắt đầu game từ con số 0 — phát hiện state, định tuyến, scaffold
---

# 🎮 /game-start — Zero-State Game Entry

> Cho người chưa có project, hoặc có ý tưởng mơ hồ.
> Trả lời "tôi đang ở đâu?" trước khi hỏi "tôi muốn làm gì?".

---

## STEP 1: PHÂN LOẠI

Chạy trước, không suy đoán:

```
hsa_detect(action:"stack")
Glob: *.unity | *.uproject | project.godot | ProjectSettings/ProjectVersion.txt
hsa_bridge({target:'unity', action:'status'})
hsa_bridge({target:'ue',    action:'status'})
```

| Tình trạng | Nhánh |
|:-----------|:------|
| Không có project, không có engine | **A** |
| Không có project, đã nói rõ engine | **B** |
| Có Unity/Unreal project, Editor đang mở | **C** |
| Có project, Editor đóng | **D** |

---

## NHÁNH A — Chưa có gì

**Đừng hỏi "bạn muốn làm game gì?" ngay.** Hỏi theo thứ tự, mỗi câu một lần:

1. **Thể loại** — "Bạn muốn loại game nào?" Gợi ý từ `data/genres.yaml` (7 template có sẵn, không cần brainstorm từ đầu).
2. **Nền tảng** — PC / mobile / web.
3. **Phong cách** — 2D pixel / 2D vector / 3D low-poly / 3D realistic.
4. **Phạm vi** — "Bản chơi được đầu tiên cần bao lâu để chạy?" (scope nhỏ: 1–2 tuần).

Sau đó sinh GDD từ template → **dừng, chờ duyệt** → sang **B**.

> Không hỏi "bạn có ý tưởng gì không" nếu người dùng đã nói rồi. Câu đó chỉ dành cho khi họ thật sự trống.

## NHÁNH B — Đã chọn engine, chưa có project

Agent **không tự tạo project**. Unity và Unreal project do Editor sinh ra, một phần là file nhị phân — viết tay sẽ tạo ra thứ trông hoàn chỉnh nhưng hỏng.

Nói rõ với user, rồi chờ:

> **Unity**: mở Unity Hub → Create project (chọn URP, Empty 3D hoặc 2D) →
> vào `Edit > Package Manager > +` → `Add package from git...` →
> dán URL bridge plugin → quay lại `/game-start`.

> **Unreal**: Epic Launcher → Launch engine → New Project (Blank, C++ hoặc Blueprints) →
> `Tools > Plugins > Programming Languages > Editor Scripting (Python)` → bật →
> copy `init_unreal.py` vào `<Project>/Content/Python/` → quay lại `/game-start`.

> **Godot**: `godot --headless --path <dir>` tạo `project.godot`. Không cần Editor,
> không cần bridge — hỗ trợ file-level.

Đọc `references/engine-scaffold.md` để lấy nội dung chính xác từng dòng.

Khi user quay lại: chạy lại STEP 1 → sang **C** hoặc **D**.

## NHÁNH C — Project + Editor sẵn sàng

Đây là trạng thái làm việc bình thường. Sang `/game`.

Trước khi sang, load skill và báo cáo ngắn:

```
hsa_search(action:"skills", query:"game development")
hsa_bridge({target:'<engine>', action:'discover'})   → instance_id, engine version
hsa_bridge({target:'<engine>', action:'status'})
```

## NHÁNH D — Có project, Editor đóng

Nói rõ, không tự mở GUI:

> "Tìm thấy project `<engine>` tại `<path>`, nhưng Editor chưa chạy.
> Mở Editor để em đọc/ghi scene được, rồi chạy lại `/game`."

Nếu user muốn chỉ làm việc file-level (code, config, docs) → làm trực tiếp, không cần Editor.

---

## OUTPUT

Sau khi phân loại, **luôn** kết thúc bằng một trong:

| Kết quả | Hành động tiếp |
|:--------|:---------------|
| Nhánh A hoàn tất | Sinh GDD → chờ duyệt → nhảy `/game` |
| Nhánh B | Dừng, hướng dẫn tạo project, chờ user |
| Nhánh C | Nhảy `/game` |
| Nhánh D | Dừng, yêu cầu mở Editor (trừ khi chỉ sửa file) |

---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_001):

1. **VERIFY** — Đã phân loại đúng state? Đã chỉ đúng bước cần thiết, không hơn?
2. **PERSIST** (if HSA available):
   - `hsa_session({action:'persist', task_summary:'/game-start [branch] [state]', files_touched:[...]})`
3. **PERSIST** (if HSA unavailable):
   - Append task summary to `memory/session.md`
