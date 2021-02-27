- Đây là package dashboard, chứa:
    + `callbacks.py`: chứa các callback để cập nhật biểu đồ
    + `dashboard.py`: chứa html dash components
    + `datas.py`: chứa các biến dữ liệu, các dataframe. Biến toàn cục sẽ để vào hàm init,\
        khi chạy thì gọi `datas.<tên biến>`
    + `models.py`: chứa các khởi tạo về bảng của database
    + `tools.py`: chứa các hàm, mục đích cộng thêm cho các file khác
    + `__init__`.py: chứa các khởi tạo cho app, server, database, được import tất cả các file ở trên, và giúp định nghĩa thư mục dashboard trở thành một package
    + các thư mục đều có file `Readme.md` để thêm thông tin