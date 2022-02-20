# emulator
this package hỗ trợ điều khiển các phần mềm giả lập như LDPlayer một cách dễ dàng

## Installation
```bash
git clone https://github.com/Thachj-Thw/emulator.git
```

## Usage
just type `import emulator` in the module you want to use.

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
### push
### capture
### adb_connected
### tap
### swipe
### send_text
### send_event
### home
### back
### app_switcher
### tap_to_img
### tap_to_imgs
### wait_img_existed
### dump_xml
### get_node
### get_nodes
### wait
### hide
### show
### quit