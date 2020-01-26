# Được trích từ dự án openpose
Adapted from the openpose project

**Vì tất cả kích thước model và một số file khá lớn không thể lưu trên github nên chúng ta cần download từ một nguồn khác**

Đây là một bộ thư viện hỗ trợ cho bài tập lớn Danca, sử dụng dự án openpose. Cảm ơn tất cả các tác giả của dự án openpose. Đường dẫn github: https://github.com/CMU-Perceptual-Computing-Lab/openpose

## Để sử dụng thư viện này, thực hiện các hướng dẫn sau:
Cài đặt cần thiết:

- Cuda 10.1

```
git clone https://github.com/vinhphuctadang/danpo.git
```

Sau đó, vào thư mục models. Thực hiện:
Trên windows, vào ./models/, chạy **getModels.bat**
Hiện tại chưa test trên linux, unix, macos
Trên Linux, vào ./models/, chạy **getModels.sh**

--- 

- Since model sizes are too large to be stored on github, we needs to download them from internet, from other source

- This is an independent package from Danca project, which takes advantages of openpose projects
Thanks all contributors of the project: https://github.com/CMU-Perceptual-Computing-Lab/openpose