> [!example] Các Phase
> Dự án chia làm 4 phase, hoàn thành tuần tự.

## Phase 1: Nghiên cứu & Chuẩn bị
- [x] Xác định danh sách nguồn tin
- [x] Xây dựng Python prototype ([[main.py]])
- [ ] Test crawl thử từng nguồn
- [ ] Xác định cấu trúc HTML/RSS mỗi nguồn

## Phase 2: Xây dựng Google Apps Script
- [ ] Tạo Google Sheet với header cột
- [ ] Viết hàm fetch RSS/HTML từng nguồn
- [ ] Viết hàm parse nội dung (title, content, datetime public)
- [ ] Viết hàm phát hiện mention mã CK
- [ ] Viết hàm append row vào Sheet
- [ ] Viết hàm backfill dữ liệu lịch sử
- [ ] Cài đặt time-driven trigger hằng ngày

## Phase 3: Crawl lịch sử
- [ ] Chạy backfill 3+ năm từ các nguồn có sẵn
- [ ] Kiểm tra dữ liệu, loại bỏ trùng lặp

## Phase 4: Vận hành
- [ ] Crawl hằng ngày tự động
- [ ] Monitoring lỗi (timeout, thay đổi cấu trúc trang)
- [ ] Bảo trì nguồn (thêm/bớt khi nguồn thay đổi)

---

> [!todo] Backlog
> - [ ] Dashboard thống kê trên Google Sheets
> - [ ] Alert khi có tin mới về mã nào đó
