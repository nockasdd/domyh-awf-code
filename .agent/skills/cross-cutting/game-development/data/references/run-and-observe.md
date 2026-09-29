# Run and Observe

> Compile thành công ≠ game chơi được.
> Mỗi thay đổi player-observable phải được chạy và nhìn trước khi đóng.

---

## Vì sao

- **Compile** chứng minh code load được. Không chứng minh UI không tràn, không chứng
  minh nhân vật spawn đúng chỗ.
- **Test** chứng minh logic đúng. Không chứng minh nhìn ra sao.
- **Chạy và nhìn** là bước duy nhất bắt được cả hai.

Quy tắc: *"Nếu không ai nhìn nó, nó chưa xong."*

---

## Unity — qua bridge

```
1. unity_play_mode({action:'play'})     → vào play mode
2. chờ 1–2 giây cho scene load
3. unity_get_logs({limit:50})           → không có error?
4. chụp viewport                        → xem cái gì hiện ra
5. unity_play_mode({action:'stop'})     → thoát play mode
```

Bước 4 là bắt buộc, nhưng bridge **chưa có** tool chụp ảnh — 22 Unity tools
(`t17_bridge.ts:255-278`) không có `unity_capture_screenshot`. Cho đến khi thêm,
làm một trong hai:

- `unity_create_script` tạo một script tạm gọi `ScreenCapture.CaptureScreenshot`,
  rồi xem file trong `Library/Screenshots/`.
- Chụp cửa sổ Editor thủ công và dán vào đây.

Đừng báo "đã verify" nếu chỉ chạy bước 1–3.

## Unreal — qua bridge

```
1. ue_execute_python: unreal.EditorLevelLibrary.editor_play_simulate()   (hoặc
   ue_execute_python: unreal.EditorLevelLibrary.editor_request_begin_play())
2. chờ tick
3. đọc Output Log
4. chụp viewport qua Remote Control
5. ue_execute_python: editor_request_end_play()
```

UE có 14 tools (`t17_bridge.ts:280-294`) — `ue_execute_python` là đường vào,
không có tool chụp ảnh riêng.

## Godot — không cần bridge

```bash
# 60 frame rồi tự thoát, ghi ra PNG
godot --path . --write-movie out.png --quit-after 60

# chạy headless để bắt lỗi script
godot --headless --path . --quit
```

> Lưu ý: `--headless --quit` exit 0 **không** có nghĩa là game chạy đúng.
> Xem mục `.godot/global_script_class_cache.cfg` trong `engine-scaffold.md`.

---

## Khi nào KHÔNG cần

- Đổi hằng số nội bộ, rename biến, refactor không đổi hành vi.
- Chỉ sửa comment hoặc doc.

Cần khi: thêm/đổi scene, đổi UI, đổi input, đổi physics, đổi spawn, đổi flow
màn chơi. Tức là bất cứ thứ gì người chơi nhìn hoặc chạm vào.

---

## Ghi lại bằng chứng

Lưu screenshot vào `production/qa/evidence/` (hoặc `.domyh/game-evidence/`
nếu project chưa có cấu trúc QA). Tên file có ngày + mô tả:

```
production/qa/evidence/2026-09-27-player-spawn-fixed.png
```

Khi user hỏi "chạy thử giúp tôi", đây là thứ chứng minh bạn đã thực sự chạy.
