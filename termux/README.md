# Telegram Shop Bot (aiogram v3)

## Requirements
- Python 3.11+

## Setup
```bash
pip install -r requirements.txt
```

Create `.env` based on `.env.example` and set `BOT_TOKEN` + `ADMIN_IDS`.

## Run
```bash
python -m app.main
```

## UI Improvements ✨

### Icons & Emojis
Tất cả các nút bấm và thông báo đều được trang trí với emoji để giao diện trở nên vui vẻ và dễ hiểu:

- 🏠 **Trang chủ** - Home
- 🎬 **Kéo mem** - Mem list
- 📌 **Hướng dẫn** - Guide
- 💰 **Nạp tiền** - Top up
- 📜 **Điều khoản** - Terms
- 👤 **Cá nhân** - Profile
- 📦 **Dịch vụ** - Services
- ✅ **Duyệt** - Approve
- ❌ **Từ chối** - Reject
- ⬅️ **Quay lại** - Back

### Định dạng HTML
Tất cả các tin nhắn đều sử dụng HTML formatting để:
- **In đậm** cho tiêu đề
- `Code` cho các mã giao dịch
- *Nghiêng* cho chú thích
- Các biểu tượng phân cách đẹp mắt

### File cấu hình Icon
Tất cả các icon được quản lý tập trung trong file `app/utils/icons.py`:

```python
from app.utils.icons import ICON_HOME, ICON_MEM, ICON_GUIDE, ...
```

Điều này giúp dễ dàng thay đổi icon hoặc thêm icon mới mà không cần sửa nhiều file.

### Cấu trúc giao diện
Mỗi màn hình đều có:
- Header với biểu tượng và tiêu đề
- Nội dung chính được định dạng rõ ràng
- Footer hoặc nút quay lại
- Thông báo lỗi được tô sáng với emoji ⚠️

### Ví dụ
```
┌──────────────────────────────┐
🏠 TELEGRAM SHOP BOT 🏠
└──────────────────────────────┘

👤 UserID: 123456789
💳 Số dư ví: 500.000 ₫

⚠️ Vui lòng xem hướng dẫn trước khi sử dụng!
```
