> [!example] Chi tiết từng nguồn — API zone IDs, RSS URLs

## RSS + API Sources

### CafeF (cafef.vn)
- **RSS**: 4 feeds (BĐS, CK, DN, TC)
- **API**: `GET /ajax/timelinelist.chn?zoneId={id}&page={n}&pageSize=15`
- **Zones**: 18835 (BĐS), 18831 (CK), 18836 (DN), 18834 (TC), 18833 (Vĩ mô), 18839 (TT), 18843 (BĐS-TT), 18846 (BĐS-NT), 188120 (BĐS-DL)

### CafeBiz (cafebiz.vn)
- **RSS**: 2 feeds (BĐS, CK)
- **API**: `GET /ajax/timelinelist.chn?zoneId={id}&page={n}&pageSize=15`
- **Zones**: 176127 (BĐS), 176132 (CK), 176117 (TC), 176144 (SX), 176120 (Startup)

### VietnamNet (vietnamnet.vn)
- **RSS**: 3 feeds (KD, BĐS, DN)
- **API**: `POST /newsapi/CategoryCustom/Gets` — JSON, 50 bài/trang
- **Categories**: 000003 (KD), 00000G (TC), 00000H (ĐT), 00000J (TT), 00002N (CK), 00000E (BĐS), 00001C (Dự án), 00004V (TT BĐS)

## RSS Only Sources (38)

| Source | Feeds | Categories |
|--------|-------|------------|
| VnExpress | 4 | KD, BĐS, TG, TT |
| VnBusiness | 4 | BĐS, CK, TC, TT |
| VnEconomy | 6 | BĐS, CK, ĐT, DN, TC, TT, KD |
| Thanh Niên | 1 | KT |
| Dân trí | 2 | KD, BĐS |
| Báo Xây dựng | 2 | KT, BĐS |
| NLD | 1 | Kinh tế |
| VietnamPlus | 1 | KT |
| Tuổi Trẻ | 2 | KT, BĐS |
| Nhân Dân | 1 | Kinh tế |
| Tiền Phong | 1 | Kinh tế |
| Soha | 1 | Kinh doanh |
| ANTĐ | 2 | KT, BĐS |
| CAND | 1 | Kinh tế |
| Công Thương | 1 | Kinh tế |
| SKĐS | 3 | KT, BĐS, TC |
| Infonet | 1 | Kinh doanh |
| Kiến Thức | 1 | Kinh doanh |
| PLO | 1 | Tổng hợp |
| VTC News | 4 | KT, BĐS, TT, TC |
| 24h | 1 | Kinh doanh |
| Docnhanh | 1 | Kinh tế |
| Nguoiduatin | 2 | KT, BĐS |
| KTVN Times | 1 | Kinh tế |
| VietTimes | 2 | KT, BĐS |
| Diễn đàn KT | 1 | Kinh tế |
| Công Luận | 1 | Kinh tế |
| Biz Việt | 1 | Kinh doanh |
| Reatimes | 1 | BĐS (chuyên) |
| VTV | 4 | KT, TC, TT, TG |
| ZNEWS | 2 | KD, TT |
| TINMOI | 3 | KT, BĐS, TC |
| Đầu tư Việt Nam | 5 | BĐS, CK, DN, KD, TC |
| ANTT | 4 | CK, TC, BĐS, KD |
| VietnamBiz | 1 | BĐS |
| Ngân hàng VN | 5 | CK, TC, TT, BĐS, KD |
| Đời sống VN | 2 | BĐS, KD |
| Doanh nghiệp VN | 5 | BĐS (4 mục), KD |

## GAS API URLs
- CafeF API GAS: `GET https://cafef.vn/ajax/timelinelist.chn?zoneId={id}&page=1&pageSize=15`
- CafeBiz API GAS: `GET https://cafebiz.vn/ajax/timelinelist.chn?zoneId={id}&page=1&pageSize=15`
- VietnamNet API GAS: `POST https://vietnamnet.vn/newsapi/CategoryCustom/Gets`

> **Note**: CafeF/CafeBiz API trên GAS hiện đang trả về null. Cần debug.

## Ghi chú
- Nguồn nào có RSS → crawl RSS
- Nguồn nào có cả RSS + API → crawl cả 2
- GAS daily() chỉ crawl RSS + API page 1
- Batch flush accumulator cuối daily()
- 2 triggers daily: 08:00 + 20:00
