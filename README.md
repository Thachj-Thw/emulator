# emulator

package này hỗ trợ điều khiển các phần mềm giả lập (Hiện tại chỉ hỗ trợ phần mềm LDPlayer)

## Installation

```bash
pip install emulator-thw
```

---

## Usage

### Example started

LDPlayer

```python
import emulator


ld = emulator.LDPlayer(ldplayer_dir="C:/LDPlayer/LDPlayer4.0")
print(ld.emulators)
```

Có hai cách để lấy ldplayer trong `LDPlayer` là dùng `index` `ld.emulators[0]` hoặc dùng `name` `ld.emulator["LDPlayer"]`. Tôi khuyên bạn nên sử dụng index, vì name có thể trùng lặp dẫn tới điều khiển sai ldplayer.

Tạo LDPlayer mới

```python
em = ld.new("New-LDPlayer")
em.start()
```

Xóa LDPlayer

```python
em_remove = ld.emulators[0]
ld.remove(em_remove)
```

Sao chép LDPlayer

```python
em_copy = ld.emulators[0]
ld.copy(em_copy)
```

Sắp xếp các cửa sổ LDPlayer

```python
for em in ld.emulators:
    em.start(wait=False)
ld.sort_window()
```

Đặt giá trị ADB debugging (mặc định sẽ tự bật ADB debugging cho tất cả LDPlayer, nhưng có một số phiên bản LDPlayer mặc dù ADB debugging hiển thị đã bật nhưng không thể kết nối và phải thực hiện bật lại một cách thủ công)

```python
em = ld.emulators[0]
ld.set_ADB_debugging(em, True) # turn on ADB debugging
ld.set_ADB_debugging(em, False) # turn off ADB debugging
em.start(wait=False)
```

Tạo các hành động

```python
em = ld.emulators[0]
em.start()
em.tap((100, 100)) # code từng dòng
em.wait(3).swipe((200, 100), (10, 100)).wait(3).quit() # code 1 chuỗi hành động
```

Bỏ qua `quit()` bằng cách sử dụng `with`

```python
with ld.emulators[0].start() as em:
    em.tap((100, 100))
```

---

## List methods

Danh sách các phương thức có thể sử dụng

- [start](#start)

- [wait_to_started](#wait_to_started)

- [is_running](#is_running)

- [restart](#restart)

- [rename](#rename)

- [list_packages](#list_packages)

- [install_app](#install_app)

- [uninstall_app](#uninstall_app)

- [run_app](#run_app)

- [kill_app](#kill_app)

- [clear_app](#clear_app)

- [set_locate](#set_locate)

- [update_properties](#update_properties)

- [get_properties](#get_properties)

- [setting](#setting)

- [down_cpu](#down_cpu)

- [backup](#backup)

- [restore](#restore)

- [action](#action)

- [scan](#scan)

- [pull](#pull)

- [push](#push)

- [capture](#capture)

- [adb_connected](#adb_connected)

- [tap](#tap)

- [tap_to_img](#tap_to_img)

- [tap_to_imgs](#tap_to_imgs)

- [wait_img_existed](#wait_img_existed)

- [swipe](#swipe)

- [hold](#hold)

- [drag_drop](#drag_drop)

- [send_text](#send_text)

- [send_event](#send_event)

- [home](#home)

- [back](#back)

- [app_switcher](#app_switcher)

- [dump_xml](#dump_xml)

- [find_node](#find_node)

- [find_nodes](#find_nodes)

- [wait](#wait)

- [hide](#hide)

- [show](#show)

- [quit](#quit)

---

### start

Khởi chạy emulator. Nếu tham số `wait=True` sẽ gọi phương thức `wait_to_stared()`.

```python
em.start(wait=True)
```

### wait_to_started

Chờ cho quá trình khởi chạy hoàn tất (thực chất là chờ kết nối ADB).

```python
em.wait_to_started()
```

### is_running

Trả về `True` nếu emulator đang chạy ngược lại `False`

```python
em.is_running()
```

### restart

Khởi chạy lại emulator, tham số `wait` tương tự `start()`

```python
em.restart(wait=True)
```

### rename

Đổi tên emulator thành `new_name`

```python
em.rename(new_name="New-Name-LDPlayer")
```

### list_packages

trả về danh sách các package đã cài đặt trên thiết bị

```python
packages = em.list_packages()
print(packages)
```

### install_app

Cài đặt ứng dụng, `source` có thể là đường dẫn tới file `.apk` hoặc `package name`

```python
em.install_app(source="example_app.apk")
```

### uninstall_app

Gỡ cài đặt ứng dụng có package name tương ứng. Xem thêm về [list_packages](#listpackages)

```python
em.uninstall_app(package_name="com.example.app")
```

### run_app

Mở dứng dụng có package name tương ứng. Xem thêm về [list_packages](#listpackages)

```python
em.run_app(package_name="com.android.chrome")
```

### kill_app

Dừng dứng dụng có package name tương ứng. Xem thêm về [list_packages](#listpackages)

```python
em.kill_app(package_name="com.android.chrome")
```

### clear_app

Xóa data của ứng dụng có package name tương ứng. Xem thêm về [list_packages](#listpackages)

```python
em.clear_app(package_name="com.android.chrome")
```

### set_locate

Cài đặt locate

```python
em.set_locate(locate="locate")
```

### update_properties

Cập nhật thông tin thiết bị, tham số prop là 1 `dict` với key là tên property và value là giá trị tương ứng

```python
em.update_properties(prop)
```

### get_properties

Trả về 1 `dict` với key là tên property và value là giá trị property

```python
prop = em.get_properties()
print(prop)
```

### setting

cài đặt thông số emlator, tham số là 1 EmulatorOptions

```python
import emulator
from emulator.option import EmulatorOptions


ld = emulator.LDPlayer("path/to/ldplayer/")
options = EmulatorOptions()
options.set_resolution(width=128, height=240, dpi=120)
em = ld.emulators[0]
em.setting(options)
em.start()
```

### down_cpu

```python
em.down_cpu(rate=50)
```

### backup

Tạo file backup emulator

```python
em.backup(file_path="C:/backup.ldbk")
```

### restore

```python
em.restore(file_path="C:/backup.ldbk")
```

### action

```python
actions = {"action": "value"}
em.action(actions=actions)
```

### scan

```python
em.scan(file_path="C:/scan.png")
```

### pull

Đưa file `remote` từ emulator về PC thành `local`

```python
em.pull(remote="sdcard/remote.txt", local="C:/local.txt")
```

### push

Đưa file `local` từ PC lên emulator thành `remote`

```python
em.push(local="C:/local.txt", remote="sdcard/remote.txt")
```

### capture

Chụp ảnh màn hình và lưu thành `as_file`

```python
em.capture(as_file="path/to/save_as.png")
```

### adb_connected

Trả về `True` nếu ADB đã kết nối với emulator ngược lại `False`. Bạn sẽ cần bật **ADB debugging** để kết nối ADB

```python
em.adb_connected()
```

### tap

Nhấn vào vị trí pos, là 1 list hoặc tuple có dạng `(x, y)`. Có thể truyền vào nhiều pos để tap nhiều lần vào nhiều vị trí khác nhau.

```python
em.tap((200, 200))
em.tap((150, 200), (250, 250))
```

### tap_to_img

Nhấp vào hình ảnh khớp với hình ảnh được cho. `timeout` là thời gian chờ hình xuất hiện nếu nhỏ hơn 0 sẽ chờ vô hạn mặc định `timeout=0`, `threshold` là độ chính xác khi tìm kiếm, nằm trong khoảng từ 0 tới 1 mặc định `threshold=0.8`.

```python
em.tap_to_img(img_path="path/to/img", timeout=0, threshold=0.8)
```

### tap_to_imgs

Nhấn vào tất cả hình ảnh khớp với hình ảnh được cho. `timeout` là thời gian chờ hình xuất hiện nếu nhỏ hơn 0 sẽ chờ vô hạn mặc định `timeout=0`, `threshold` là độ chính xác khi tìm kiếm, nằm trong khoảng từ 0 tới 1 mặc định `threshold=0.8`.

```python
em.tap_to_imgs(img_path="path/to/img", timeout=0, threshold=0.8)
```

### wait_img_existed

Chờ cho tới khi hình ảnh xuất hiện trên màn hình, chờ tối đa `timeout` giây, nếu `timeout=0` sẽ chờ vô hạn cho tới khi có hình ảnh. `threshold` là độ chính xác khi tìm kiếm nằm trong khoảng 0 tới 1 mặc định `threshold=0.8`.

```python
em.wait_img_existed(img_path="path/to/img", timeout=0, threshold=0.8)
```

### swipe

Vuốt từ vị trí `_from` tới vị trí `to` trong khoảng thời gian `duration` millisecond.

```python
em.swipe(_from=(100, 200), to=(500, 200), duration=100)
```

### hold

Nhấn giữ tại vị trí `pos` trong thời gian `duration` millisecond

```python
em.hold(pos=(250, 150), duration=500)
```

### drag_drop

Kéo thả từ vị trí `_from` tới vị trí `to`

```python
em.drag_drop(_from=(250, 150), to=(1000, 150))
```

### send_text

Gửi đoạn văn bản `text`.

```python
em.send_text(text)
```

### send_event

Gửi event tới emulator. Nhấn giữ nếu `long_press = True`

```python
import emulator.keys

em.send_event(emulator.keys.KEYCODE_CALL, long_press=False)
```

### home

Nhấn vào nút home

```python
em.home()
```

### back

Nhấn vào nút back

```python
em.back()
```

### app_switcher

Nhấn vào nút app switcher

```python
em.app_switcher()
```

### dump_xml

Lưu window_dump thành file

```python
em.dump_xml(as_file="path/local.xml")
```

### find_node

Trả về `Node` đầu tiên trong window_dump có giá trị khớp với giá trị đã cho, nếu không tìm được trả về `None`

```python
from emulator.node import By

node = em.find_node(By.TEXT, "LD Store")
```

### find_nodes

Trả về một `list` là tất cả các node trong window_dump có giá trị khới với gía trị đã cho

```python
from emulator.node import By

nodes = em.find_nodes(By.TEXT, "LD Store")
```

### wait

Dừng chương trình trong second giây

```python
em.wait(second)
```

### hide

Ẩn emulator

```python
em.hide()
```

### show

Hiển thị emulator

```python
em.show()
```

### quit

Tắt emulator

```python
em.quit()
```
