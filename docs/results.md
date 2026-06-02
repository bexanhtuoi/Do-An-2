> [!success] Đầu ra dự kiến

## 1. Google Sheet chứa dữ liệu tin tức ô tô niêm yết
- Tối thiểu **3 năm dữ liệu** (backfill từ các nguồn)
- Cập nhật **hằng ngày** với tin mới
- Mỗi dòng là 1 bài viết + cờ mention 7 mã CK

## 2. Hệ thống tự động Google Apps Script
- Chạy không tốn phí server
- Dễ bảo trì, sửa nguồn

---

## Lợi ích
- Phân tích truyền thông của từng công ty theo thời gian
- Phát hiện sự kiện, tin tức ảnh hưởng đến giá cổ phiếu
- Dữ liệu đầu vào cho các mô hình phân tích sentiment, dự đoán

## Chỉ số đánh giá

| Chỉ số | Mô tả |
|--------|-------|
| Số lượng bài viết/tháng | ≥ 500 |
| Tỷ lệ phát hiện mention chính xác | ≥ 90% |
| Thời gian chạy crawl mỗi lần | ≤ 10 phút |
| Tỷ lệ lỗi nguồn | ≤ 5% |
