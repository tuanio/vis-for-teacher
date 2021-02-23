- After deploy to the heroku cloud server:
    + login heroku
    + run init_db.py when using heroku terminal

- Các file trong thư mục dashboard:
    + callbacks.py: chứa các callback để cập nhật biểu đồ
    + dashboard.py: chứa html dash components
    + datas.py: chứa các biến dữ liệu, các dataframe. Biến toàn cục sẽ để vào hàm init,\
        khi chạy thì `gọi datas.<tên biến>`
    + models.py: chứa các khởi tạo về bảng của database
    + tools.py: chứa các hàm, mục đích cộng thêm cho các file khác
    + `__init__`.py: chứa các khởi tạo cho app, server, database, được import tất cả các file ở trên, và giúp định nghĩa thư mục dashboard trở thành một package
