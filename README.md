# emulator
this package hỗ trợ điều khiển các phần mềm giả lập như LDPlayer một cách dễ dàng

## Installation
```bash
git clone https://github.com/Thachj-Thw/emulator.git
```

## Usage
Sao chép package emulator và ghi vào project của bạn. Sau đó chỉ cần `import emulator` và sử dụng

### Example started
LDPlayer
```python
import emulator

path_to_ldplayer_dir = "C:/LDPlayer/LDPlayer4.0"
ld = emulator.LDPlayer(path_to_ldplayer_dir)
```
có hai cách để lấy player trong LDPlayer là dùng `index` `ld.emulators[0].start()`
hoặc dùng `name` `ld.emulator["LDPlayer"].start()`.
'tôi khuyên bạn nên sử dụng index, vì name có thể trùng lặp dẫn tới điều khiển sai player'

tạo player mới
```python
em = ld.new("New-LDPlayer")
em.start()
```

xóa player
```python
em_remove = ld.emulators[0]
ld.remove(em_remove)
```

sao chép player
```python
em_copy = ld.emulators[0]
ld.copy(em_copy)
```

sắp xếp các player
```python
for em in ld.emulators:
    em.start(wait=False)
ld.sort_window()
```

tạo các hành động
```python
em = ld.emulator[0]
em.start()
em.tap((100, 100)) # code từng dòng
em.wait(3).swipe((200, 100), (10, 100)).wait(3).quit() # code 1 chuỗi hành động
```

Bỏ qua `quit()` bằng cách sử dụng `with`
```python
with ld.emulators[0].start() as em:
    em.tap((100, 100))
```

## List methods
Danh sách các phương thức có thể sử dụng
### start
Khởi chạy player. Nếu tham số wait=True sẽ gọi phương thức `wait_to_stared()`.
```python
em.start(wait=True)
```
### wait_to_started
Chờ cho quá trình khởi chạy hoàn tất. Thực chất là chờ kết nối ADB
### is_running
`return True` nếu player đang chạy ngược lại `return False`
### restart
Khởi chạy lại player, tham số `wait` tương tự `start()`
```python
em.restart(wait=True)
```
### rename
Đổi tên player
### install_app
Cài đặt ứng dụng, source có thể là đường dẫn tới file .apk hoặc package name
```python
em.install_app(source)
```
### uninstall_app
Gỡ cài đặt ứng dụng có package name tương ứng
```python
em.uninstall_app(package_name)
```
### run_app
Mở dứng dụng có package name tương ứng
```python
em.run_app(package_name)
```
### kill_app
Dừng dứng dụng có package name tương ứng
```python
em.kill_app(package_name)
```
### list_packages
trả về danh sách các package đã cài đặt trên thiết bị
### set_locate
Cài đặt locate
### update_properties
Cập nhật thông tin thiết bị, tham số prop là 1 `dict` với key là tên property và value là giá trị tương ứng
```python
em.update_properties(prop)
```
### get_properties
Trả về 1 `dict` với key là tên property và value là giá trị property
### property_setting
cài đặt thông số player, tham số là 1 EmulatorOptions
```python
import emulator
from emulator.option import EmulatorOptions


ld = emulator.LDPlayer("path/to/ldplayer dir/")
options = EmulatorOptions()
options.set_resolution(width=128, height=240, dpi=120)
em = ld.emulators[0]
em.property_setting(options)
em.start()
```
### down_cpu

### backup
Tạo file backup player
### restore

### action

### scan

### pull
Đưa file `remote` từ player về PC thành `local`
```python
em.pull(remote="sdcard/remote.txt", local="C:/local.txt")
```
### push
Đưa file `local` từ PC lên player thành `remote`
```python
em.push(local="C:/local.txt", remote="sdcard/remote.txt")
```
### capture
Chụp ảnh màn hình và lưu thành `as_file`
```python
em.capture(as_file="path/to/save_as.png")
```
### adb_connected
Trả về `True` nếu ADB đã kết nối với player ngược lại `False`
### tap
Nhấn vào vị trí `pos`
```python
em.tap(pos=(200, 200))
```
### swipe
Vuốt từ vị trí `_from` tới vị trí `to` trong khoảng thời gian `duration` millisecond.
```python
em.swipe(_from=(100, 200), to=(500, 200), duration=100)
```
### send_text
Gửi đoạn văn bản `text`.
```python
em.send_text(text)
```
### send_event
Gửi event tới player
```python
import emulator
from emulator import keys


ld = emulator.LDPlayer("path/to/ldplayer dir")
em = ld.emulators[0].start()
em.wait(5).send_event(keys.KEYCODE_CALL)
```
### home
Nhấn vào nút home
### back
Nhấn vào nút back
### app_switcher
Nhấn vào nút app switcher
### tap_to_img
Nhấp vào hình ảnh khới với hình ảnh được cho. `threshold` là độ chính xác khi tìm kiếm, nằm trong khoảng từ 0 tới 1
```python
em.tap_to_img("path/to/img", threshold=0.8)
```
### tap_to_imgs
Nhấn vào tất cả hình ảnh khớp với hình ảnh được cho. `threshold` là độ chính xác khi tìm kiếm, nằm trong khoảng từ 0 tới 1.
```python
em.tap_to_imgs("path/to/img", threshold=0.8)
```

### wait_img_existed
Chờ cho tới khi hình ảnh xuất hiện trên màn hình, chờ tối đa `timeout` giây, `threshold` là độ chính xác khi tìm kiếm nằm trong khoảng 0 tới 1.
```python
em.wait_img_existed("path/to/img", timeout=0, threshold=0.8)
```

### dump_xml
Lưu window_dump thành file
```python
em.dump_xml("path/local.xml")
```

### get_node
Trả về `Node` đầu tiên trong window_dump có giá trị khớp với giá trị đã cho, nếu tìm được trả về `None`
```python
import emulator
from emulator.node import By


ld = emulator.LDPlayer("path/to/ldplayer")
em = ld.emulator[0].start().wait(10)
em.get_node(By.TEXT, "node text")
```

### get_nodes
Trả về một `list` là tất cả các node trong window_dump có giá trị khới với gía trị đã cho
```python
import emulator
from emulator.node import By


ld = emulator.LDPlayer("path/to/ldplayer")
em = ld.emulators[0].start().wait(10)
nodes = em.get_nodes(By.TEXT, "text node")
```
### wait
Dừng chương trình trong second giây
```python
em.wait(second)
```
### hide
Ẩn player
### show
Hiển thị player
### quit
Tắt player