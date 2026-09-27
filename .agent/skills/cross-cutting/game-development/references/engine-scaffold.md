# Engine Scaffold — Setup chính xác từng engine

> Agent KHÔNG tự tạo Unity/Unreal project. File này là hướng dẫn để đưa user từ
> con số 0 đến state mà bridge kết nối được.

---

## Unity

**Tạo project** (Unity Hub → Install → New project):

| Template | Dùng khi |
|:---------|:---------|
| **3D (URP)** | game 3D, mặc định |
| **2D (URP)** | platformer, shooter top-down, puzzle |
| **3D (Built-in)** | project cũ đã dùng BIRP |

> Chọn URP trừ khi project đã tồn tại và dùng pipeline khác. GCS_005.

**Cài bridge plugin:**

```
Edit > Package Manager > + > Add package from git URL...
https://github.com/<owner>/plugin-awf.git?path=/bridge/unity
```

**Cài Input System** (nếu chọn template không kèm):

```
Edit > Package Manager > Unity Registry > com.unity.inputsystem > Install
Project Settings > Player > Active Input Handling = Input System Package (New)
```

**Sau đó verify:**

```
hsa_bridge({target:'unity', action:'health_check'})
→ { status:'ok', version:'2.0.0', unity:'2022.3.x', endpoints:[...] }
```

Nếu fail: kiểm tra `Window > General > HSA Bridge` có bật không.

**Godot KHÔNG cần** — file-based, dùng `godot --headless --path .`.

---

## Unreal Engine

**Tạo project** (Epic Launcher → Launch engine → New project):

| Template | Dùng khi |
|:---------|:---------|
| **Blank (C++)** | gameplay logic cần performance/tính mở rộng |
| **Blank (Blueprints)** | prototype, nội dung-heavy, người không viết code |
| **Third Person** | có sẵn character + camera |

**Bật Python Editor Script Plugin** — bắt buộc, không có thì `ue_execute_python` fail:

```
Tools > Plugins > Programming Languages > Editor Scripting (Python) > Enable
Restart editor
```

**Copy executor vào project:**

```
cp mcp-bridge-plugins/ue-bridge/resources/init_unreal.py  <Project>/Content/Python/
```

Lần gọi `ue_execute_python` đầu tiên sẽ trả `ready:false` với hướng dẫn — đó là
bình thường, lần sau mới chạy được. Không phải bug.

**Bật Remote Control API** (cho 13 tool còn lại):

```
Project Settings > Plugins > Remote Control > Enable
```

**Sau đó verify:**

```
hsa_bridge({target:'ue', action:'health_check'})
```

---

## Godot

Không cần Editor, không cần bridge. File-level hoàn toàn.

**Tạo project:**

```
godot --headless --path ./my-game --quit
```

Sinh `project.godot`:

```ini
config_version=5

[application]
config/name="My Game"
run/main_scene=""
config/features=PackedStringArray("4.3", "Forward Plus")

[rendering]
renderer/rendering_method="forward_plus"
```

| Renderer | Value | Dùng khi |
|:---------|:-------|:---------|
| Forward+ | `forward_plus` | 3D desktop, mặc định |
| Mobile | `mobile` | mobile, low-end |
| Compatibility | `gl_compatibility` | web, hardware cũ |

> Cố ý để `run/main_scene` trống. Godot sẽ báo lỗi nếu main scene không tồn tại —
> điều đó đúng. Tạo scene trước, rồi điền path.

**Verify:**

```
godot --headless --path . --quit
```

Exit 0 = OK.

**Cạm bẫy `.gitignore`** — nguyên nhân script hỏng sau fresh clone:

```
**/.godot/*
!**/.godot/global_script_class_cache.cfg
```

`class_name` resolve từ `global_script_class_cache.cfg`. Nếu gitignore cả thư mục
`.godot/`, mọi script tham chiếu `class_name` sẽ fail parse sau khi clone —
**nhưng** `godot --headless --quit` vẫn exit 0, nên CI không bắt được.
Luôn giữ file cache đó trong git.

---

## Sau khi setup xong

Chạy lại `/game-start`. Nó sẽ phát hiện project và route sang `/game`.
