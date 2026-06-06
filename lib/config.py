import re

STOCK_CODES = ["VHM", "VIC", "VRE", "NVL", "PDR", "DXG", "KDH", "NLG", "CEO", "DIG", "KBC", "BCM", "SZC", "VCG", "CTD", "HHV", "CII"]

STOCK_PATTERN = re.compile(r"\b(" + "|".join(STOCK_CODES) + r")\b")

COMPANY_KEYWORDS: dict[str, list[str]] = {
    "VHM": [
        "Vinhomes", "Vinh Homes", "Vinhome",
        "Công ty Cổ phần Vinhomes",
        "Vinhomes Joint Stock Company",
    ],
    "VIC": [
        "Vingroup", "Tập đoàn Vingroup", "Vin Group",
        "Vinpearl", "Vincom",
        "Vingroup Joint Stock Company",
    ],
    "VRE": [
        "Vincom Retail", "Vincom Mega Mall", "Vincom Center",
        "Công ty Cổ phần Vincom Retail",
        "Vincom Retail Joint Stock Company",
    ],
    "NVL": [
        "Novaland", "Novaland Group", "Địa ốc Nova",
        "NovaGroup", "Tập đoàn Novaland",
        "Công ty Cổ phần Tập đoàn Đầu tư Địa ốc Nova",
    ],
    "PDR": [
        "Phát Đạt", "Phat Dat", "Bất động sản Phát Đạt",
        "Công ty Cổ phần Phát triển Bất động sản Phát Đạt",
        "Phat Dat Real Estate Development Corp",
    ],
    "DXG": [
        "Đất Xanh", "Dat Xanh", "Tập đoàn Đất Xanh",
        "Dat Xanh Group", "Đất Xanh Group",
    ],
    "KDH": [
        "Khang Điền", "Nhà Khang Điền", "Khang Dien",
        "Công ty Cổ phần Đầu tư và Kinh doanh Nhà Khang Điền",
        "Khang Dien House Trading",
    ],
    "NLG": [
        "Nam Long", "Đầu tư Nam Long", "Nam Long Group",
        "Công ty Cổ phần Đầu tư Nam Long",
        "Nam Long Investment Corporation",
    ],
    "CEO": [
        "CEO Group", "Tập đoàn CEO", "CEO Group JSC",
        "Tập đoàn CEO Group",
    ],
    "DIG": [
        "DIC Corp", "DIC Corporation", "DIC Group",
        "Đầu tư Phát triển Xây dựng",
        "Tổng Công ty Cổ phần Đầu tư Phát triển Xây dựng",
        "DIC Investment Development Construction",
    ],
    "KBC": [
        "Kinh Bắc", "Đô thị Kinh Bắc", "Kinh Bac",
        "Khu công nghiệp Kinh Bắc",
        "Tổng Công ty Phát triển Đô thị Kinh Bắc",
        "Kinh Bac City Development",
    ],
    "BCM": [
        "Becamex", "Becamex IDC",
        "Becamex Tổng Công ty Đầu tư",
        "Tổng Công ty Đầu tư và Phát triển Công nghiệp Becamex",
        "Becamex Investment and Industrial Development",
    ],
    "SZC": [
        "Sonadezi Châu Đức", "Sơn Đài", "Sonadezi",
        "Công ty Cổ phần Sonadezi Châu Đức",
        "Khu công nghiệp Châu Đức",
    ],
    "VCG": [
        "Vinaconex",
        "Tổng Công ty Cổ phần Xuất nhập khẩu Xây dựng Việt Nam",
        "Xuất nhập khẩu Xây dựng Việt Nam",
        "Vietnam Construction Import Export",
    ],
    "CTD": [
        "Coteccons", "Xây dựng Coteccons", "Coteccons Construction",
        "Công ty Cổ phần Xây dựng Coteccons",
        "Coteccons Construction Joint Stock Company",
    ],
    "HHV": [
        "Đèo Cả", "Deo Ca", "Hạ tầng Giao thông Đèo Cả",
        "Công ty Cổ phần Đầu tư Hạ tầng Giao thông Đèo Cả",
        "Highway Infrastructure Investment",
    ],
    "CII": [
        "CII Infrastructure",
        "Công ty Cổ phần Đầu tư Hạ tầng Kỹ thuật Thành phố Hồ Chí Minh",
        "Hạ tầng Kỹ thuật TP HCM",
        "CII Infrastructure Investment",
    ],
}

COMPANY_NAME_PATTERNS: dict[str, re.Pattern] = {}
for code, keywords in COMPANY_KEYWORDS.items():
    escaped = [re.escape(kw) for kw in keywords]
    COMPANY_NAME_PATTERNS[code] = re.compile(r"(?i)(" + "|".join(escaped) + r")")

COMPANY_INFO: list[dict] = [
    {"code": "VHM", "full_name": "Công ty Cổ phần Vinhomes", "english_name": "Vinhomes Joint Stock Company", "former_name": "", "exchange": "HOSE", "industry": "Bất động sản nhà ở", "website": "https://vinhomes.vn", "established": "2008", "employees": "18.000+", "business": "Phát triển khu đô thị, căn hộ chung cư, nhà ở xã hội", "keywords": "Vinhomes, Vinh Homes, VHM"},
    {"code": "VIC", "full_name": "Tập đoàn Vingroup", "english_name": "Vingroup Joint Stock Company", "former_name": "Vinpearl, Vincom", "exchange": "HOSE", "industry": "Đa ngành (BĐS, bán lẻ, y tế, giáo dục)", "website": "https://vingroup.net", "established": "1993", "employees": "70.000+", "business": "Đầu tư, phát triển bất động sản, trung tâm thương mại, khách sạn, bệnh viện", "keywords": "Vingroup, VIC"},
    {"code": "VRE", "full_name": "Công ty Cổ phần Vincom Retail", "english_name": "Vincom Retail Joint Stock Company", "former_name": "", "exchange": "HOSE", "industry": "Bất động sản bán lẻ", "website": "https://vincom.com.vn", "established": "2012", "employees": "3.000+", "business": "Sở hữu, vận hành trung tâm thương mại Vincom, Vincom Mega Mall", "keywords": "Vincom Retail, VRE"},
    {"code": "NVL", "full_name": "Công ty Cổ phần Tập đoàn Đầu tư Địa ốc Nova (Novaland)", "english_name": "Novaland Group", "former_name": "", "exchange": "HOSE", "industry": "Bất động sản nhà ở, nghỉ dưỡng", "website": "https://novaland.com.vn", "established": "2007", "employees": "5.000+", "business": "Phát triển bất động sản nhà ở, khu đô thị, resort", "keywords": "Novaland, NVL, Địa ốc Nova"},
    {"code": "PDR", "full_name": "Công ty Cổ phần Phát triển Bất động sản Phát Đạt", "english_name": "Phat Dat Real Estate Development Corp", "former_name": "", "exchange": "HOSE", "industry": "Bất động sản nhà ở", "website": "https://phatdat.com.vn", "established": "2004", "employees": "800+", "business": "Đầu tư, phát triển dự án bất động sản nhà ở, khu dân cư", "keywords": "Phát Đạt, PDR, Bất động sản Phát Đạt"},
    {"code": "DXG", "full_name": "Tập đoàn Đất Xanh", "english_name": "Dat Xanh Group", "former_name": "", "exchange": "HOSE", "industry": "Dịch vụ và môi giới bất động sản", "website": "https://datxanh.vn", "established": "2003", "employees": "6.000+", "business": "Môi giới, sàn giao dịch bất động sản, phát triển dự án", "keywords": "Đất Xanh, Dat Xanh, DXG"},
    {"code": "KDH", "full_name": "Công ty Cổ phần Đầu tư và Kinh doanh Nhà Khang Điền", "english_name": "Khang Dien House Trading and Investment JSC", "former_name": "", "exchange": "HOSE", "industry": "Bất động sản nhà ở", "website": "https://khangdien.com.vn", "established": "2001", "employees": "500+", "business": "Phát triển nhà ở, khu dân cư, căn hộ", "keywords": "Khang Điền, KDH, Nhà Khang Điền"},
    {"code": "NLG", "full_name": "Công ty Cổ phần Đầu tư Nam Long", "english_name": "Nam Long Investment Corporation", "former_name": "", "exchange": "HOSE", "industry": "Bất động sản nhà ở", "website": "https://namlong.com", "established": "1992", "employees": "1.500+", "business": "Phát triển khu đô thị, nhà ở, căn hộ", "keywords": "Nam Long, NLG, Đầu tư Nam Long"},
    {"code": "CEO", "full_name": "Tập đoàn CEO", "english_name": "CEO Group", "former_name": "CEO Group", "exchange": "HNX", "industry": "Bất động sản và dịch vụ liên quan", "website": "https://ceogroup.com.vn", "established": "2005", "employees": "1.000+", "business": "Phát triển bất động sản, khách sạn, đào tạo", "keywords": "CEO Group, CEO"},
    {"code": "DIG", "full_name": "Tổng Công ty Cổ phần Đầu tư Phát triển Xây dựng", "english_name": "DIC Corporation", "former_name": "DIC Corp", "exchange": "HOSE", "industry": "Bất động sản và xây dựng", "website": "https://dic.vn", "established": "2000", "employees": "2.000+", "business": "Đầu tư, phát triển dự án bất động sản, hạ tầng khu công nghiệp", "keywords": "DIC Corp, DIG, DIC Corporation, Đầu tư Phát triển Xây dựng"},
    {"code": "KBC", "full_name": "Tổng Công ty Phát triển Đô thị Kinh Bắc", "english_name": "Kinh Bac City Development Holding Corporation", "former_name": "", "exchange": "HOSE", "industry": "Khu công nghiệp và đô thị", "website": "https://kinhbac.com.vn", "established": "2000", "employees": "700+", "business": "Phát triển khu công nghiệp, khu đô thị", "keywords": "Kinh Bắc, KBC, Đô thị Kinh Bắc"},
    {"code": "BCM", "full_name": "Tổng Công ty Đầu tư và Phát triển Công nghiệp Becamex", "english_name": "Becamex Investment and Industrial Development Corporation", "former_name": "", "exchange": "HOSE", "industry": "Khu công nghiệp và hạ tầng", "website": "https://becamex.com.vn", "established": "1976", "employees": "3.000+", "business": "Phát triển hạ tầng khu công nghiệp, đô thị, dịch vụ", "keywords": "Becamex, BCM, Becamex Tổng Công ty Đầu tư"},
    {"code": "SZC", "full_name": "Công ty Cổ phần Sonadezi Châu Đức", "english_name": "Sonadezi Chau Duc Company Limited", "former_name": "Sơn Đài", "exchange": "HOSE", "industry": "Khu công nghiệp", "website": "https://sonadezi.edu.vn", "established": "2004", "employees": "200+", "business": "Phát triển hạ tầng khu công nghiệp, bất động sản cho thuê", "keywords": "Sonadezi Châu Đức, SZC, Sơn Đài"},
    {"code": "VCG", "full_name": "Tổng Công ty Cổ phần Xuất nhập khẩu và Xây dựng Việt Nam (Vinaconex)", "english_name": "Vietnam Construction and Import-Export Joint Stock Corporation", "former_name": "", "exchange": "HOSE", "industry": "Xây dựng và bất động sản", "website": "https://vinaconex.com.vn", "established": "1988", "employees": "5.000+", "business": "Xây dựng dân dụng, công nghiệp, phát triển khu đô thị", "keywords": "Vinaconex, VCG, Xuất nhập khẩu Xây dựng Việt Nam"},
    {"code": "CTD", "full_name": "Công ty Cổ phần Xây dựng Coteccons", "english_name": "Coteccons Construction Joint Stock Company", "former_name": "", "exchange": "HOSE", "industry": "Xây dựng", "website": "https://coteccons.vn", "established": "2004", "employees": "10.000+", "business": "Tổng thầu xây dựng dân dụng, công nghiệp, hạ tầng", "keywords": "Coteccons, CTD, Xây dựng Coteccons"},
    {"code": "HHV", "full_name": "Công ty Cổ phần Đầu tư Hạ tầng Giao thông Đèo Cả", "english_name": "Highway Infrastructure Investment Joint Stock Company", "former_name": "", "exchange": "HOSE", "industry": "Hạ tầng giao thông", "website": "https://deoca.vn", "established": "2015", "employees": "300+", "business": "Đầu tư, xây dựng và vận hành công trình hạ tầng giao thông", "keywords": "Đèo Cả, HHV, Hạ tầng Giao thông Đèo Cả"},
    {"code": "CII", "full_name": "Công ty Cổ phần Đầu tư Hạ tầng Kỹ thuật Thành phố Hồ Chí Minh", "english_name": "CII Infrastructure Investment Joint Stock Company", "former_name": "", "exchange": "HOSE", "industry": "Hạ tầng kỹ thuật", "website": "https://cii.vn", "established": "2001", "employees": "800+", "business": "Đầu tư, xây dựng hạ tầng giao thông, cầu đường, nước sạch", "keywords": "Hạ tầng Kỹ thuật TP HCM, CII, CII Infrastructure"},
]

SOURCE_INFO: list[dict] = [
    {"name": "CafeF", "domain": "cafef.vn", "categories": "BĐS, CK, DN, TC, Vĩ mô, Thị trường, BĐS-TT, BĐS-NT, BĐS-DL", "type": "RSS+API", "rss": "Có", "articles": "50k+", "note": "API timelinelist, 15 bài/trang, crawl đến empty", "has_rss": True, "has_api": True},
    {"name": "CafeBiz", "domain": "cafebiz.vn", "categories": "BĐS, CK, TC, SX, Startup", "type": "RSS+API", "rss": "Có", "articles": "20k+", "note": "API timelinelist, 15 bài/trang, crawl đến empty", "has_rss": True, "has_api": True},
    {"name": "VietnamNet", "domain": "vietnamnet.vn", "categories": "KD, TC, ĐT, TT, CK, BĐS, DN, Dự án, TT BĐS", "type": "RSS+API", "rss": "Có", "articles": "30k+", "note": "API JSON POST, 50 bài/trang, crawl đến empty", "has_rss": True, "has_api": True},
    {"name": "VnExpress", "domain": "vnexpress.net", "categories": "KD, BĐS, TG, TT", "type": "RSS", "rss": "Có", "articles": "15k+", "note": "Chỉ RSS (không có API)", "has_rss": True, "has_api": False},
    {"name": "VnBusiness", "domain": "vnbusiness.vn", "categories": "BĐS, CK, TC, DN, TT", "type": "RSS", "rss": "Có", "articles": "5k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "VnEconomy", "domain": "vneconomy.vn", "categories": "BĐS, CK, ĐT, DN, TC, TT, KD", "type": "RSS", "rss": "Có", "articles": "5k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "Thanh Niên", "domain": "thanhnien.vn", "categories": "KT, KD", "type": "RSS", "rss": "Có", "articles": "3k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "Dân trí", "domain": "dantri.com.vn", "categories": "KD, BĐS", "type": "RSS", "rss": "Có", "articles": "5k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "Báo Xây dựng", "domain": "baoxaydung.vn", "categories": "KT, BĐS", "type": "RSS", "rss": "Có", "articles": "3k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "NLD", "domain": "nld.com.vn", "categories": "Kinh tế", "type": "RSS", "rss": "Có", "articles": "2k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "VietnamPlus", "domain": "vietnamplus.vn", "categories": "KT", "type": "RSS", "rss": "Có", "articles": "2k+", "note": "Chỉ RSS, các feed đồng nhất (KT=BĐS=TT=CK=DN)", "has_rss": True, "has_api": False},
    {"name": "Tuổi Trẻ", "domain": "tuoitre.vn", "categories": "KT, BĐS", "type": "RSS", "rss": "Có", "articles": "5k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "Nhân Dân", "domain": "nhandan.vn", "categories": "Kinh tế", "type": "RSS", "rss": "Có", "articles": "2k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "Tiền Phong", "domain": "tienphong.vn", "categories": "Kinh tế", "type": "RSS", "rss": "Có", "articles": "2k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "Soha", "domain": "soha.vn", "categories": "Kinh doanh", "type": "RSS", "rss": "Có", "articles": "2k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "ANTĐ", "domain": "anninhthudo.vn", "categories": "KT, BĐS", "type": "RSS", "rss": "Có", "articles": "2k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "CAND", "domain": "cand.com.vn", "categories": "Kinh tế", "type": "RSS", "rss": "Có", "articles": "2k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "Công Thương", "domain": "congthuong.vn", "categories": "Kinh tế", "type": "RSS", "rss": "Có", "articles": "1k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "Sức Khỏe & ĐS", "domain": "suckhoedoisong.vn", "categories": "KT, BĐS, TC", "type": "RSS", "rss": "Có", "articles": "2k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "Infonet", "domain": "infonet.vietnamnet.vn", "categories": "Kinh doanh", "type": "RSS", "rss": "Có", "articles": "1k+", "note": "Chỉ RSS, thuộc VietnamNet", "has_rss": True, "has_api": False},
    {"name": "Kiến Thức", "domain": "kienthuc.net.vn", "categories": "Kinh doanh", "type": "RSS", "rss": "Có", "articles": "2k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "PLO", "domain": "plo.vn", "categories": "Tổng hợp", "type": "RSS", "rss": "Có", "articles": "2k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "VTC News", "domain": "vtcnews.vn", "categories": "KT, BĐS, TT, TC", "type": "RSS", "rss": "Có", "articles": "1k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "24h", "domain": "24h.com.vn", "categories": "Kinh doanh", "type": "RSS", "rss": "Có", "articles": "1k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "Docnhanh", "domain": "docnhanh.vn", "categories": "Kinh tế", "type": "RSS", "rss": "Có", "articles": "1k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "Nguoiduatin", "domain": "nguoiduatin.vn", "categories": "KT, BĐS", "type": "RSS", "rss": "Có", "articles": "2k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "KTVN Times", "domain": "kinhtevn.com.vn", "categories": "Kinh tế", "type": "RSS", "rss": "Có", "articles": "1k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "VietTimes", "domain": "viettimes.vn", "categories": "KT, BĐS", "type": "RSS", "rss": "Có", "articles": "2k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "Diễn đàn KT", "domain": "diendankinhte.vn", "categories": "Kinh tế", "type": "RSS", "rss": "Có", "articles": "1k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "Công Luận", "domain": "congluan.vn", "categories": "Kinh tế", "type": "RSS", "rss": "Có", "articles": "2k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "Biz Việt", "domain": "bizviet.vn", "categories": "Kinh doanh", "type": "RSS", "rss": "Có", "articles": "1k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "Reatimes", "domain": "reatimes.vn", "categories": "BĐS", "type": "RSS", "rss": "Có", "articles": "1k+", "note": "Chỉ RSS, chuyên BĐS", "has_rss": True, "has_api": False},
    {"name": "VTV", "domain": "vtv.vn", "categories": "KT, TC, TT, TG", "type": "RSS", "rss": "Có", "articles": "5k+", "note": "Đài Truyền hình Việt Nam", "has_rss": True, "has_api": False},
    {"name": "ZNEWS", "domain": "znews.vn", "categories": "KD, TT", "type": "RSS", "rss": "Có", "articles": "3k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "TINMOI", "domain": "tinmoi.vn", "categories": "KT, BĐS, TC", "type": "RSS", "rss": "Có", "articles": "2k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "DAU_TU_VIET_NAM", "domain": "dautuvietnam.com.vn", "categories": "BĐS, CK, DN, KD, TC", "type": "RSS", "rss": "Có", "articles": "3k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "AN_NINH_TIEN_TE", "domain": "antt.vn", "categories": "CK, TC, BĐS, KD", "type": "RSS", "rss": "Có", "articles": "2k+", "note": "An Ninh Tiền Tệ", "has_rss": True, "has_api": False},
    {"name": "VIETNAM_BIZ", "domain": "vietnambiz.vn", "categories": "BĐS, CK, KD", "type": "RSS", "rss": "Có", "articles": "1k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "NGAN_HANG_VN", "domain": "nganhangvietnam.vn", "categories": "CK, TC, TT, BĐS, KD", "type": "RSS", "rss": "Có", "articles": "1k+", "note": "Chuyên ngân hàng, tài chính", "has_rss": True, "has_api": False},
    {"name": "DOI_SONG_VN", "domain": "doisongvietnam.vn", "categories": "BĐS, KD", "type": "RSS", "rss": "Có", "articles": "1k+", "note": "Chỉ RSS", "has_rss": True, "has_api": False},
    {"name": "DOANH_NGHIEP_VN", "domain": "doanhnghiepvn.vn", "categories": "BĐS_TT, BĐS_PL, BĐS_CS, BĐS_DN, KD", "type": "RSS", "rss": "Có", "articles": "2k+", "note": "Chuyên BĐS, nhiều chuyên mục", "has_rss": True, "has_api": False},
]

RSS_SOURCES: list[dict] = [
    {"name": "Cafef BDS", "url": "https://cafef.vn/bat-dong-san.rss", "cat": "BĐS"},
    {"name": "Cafef CK", "url": "https://cafef.vn/thi-truong-chung-khoan.rss", "cat": "CK"},
    {"name": "Cafef DN", "url": "https://cafef.vn/doanh-nghiep.rss", "cat": "DN"},
    {"name": "Cafef TC", "url": "https://cafef.vn/tai-chinh-ngan-hang.rss", "cat": "TC"},
    {"name": "VnExpress KD", "url": "https://vnexpress.net/rss/kinh-doanh.rss", "cat": "KD"},
    {"name": "VnExpress BDS", "url": "https://vnexpress.net/rss/bat-dong-san.rss", "cat": "BĐS"},
    {"name": "Vietnamnet KD", "url": "https://vietnamnet.vn/rss/kinh-doanh.rss", "cat": "KD"},
    {"name": "Vietnamnet BDS", "url": "https://vietnamnet.vn/rss/bat-dong-san.rss", "cat": "BĐS"},
    {"name": "Vietnamnet DN", "url": "https://vietnamnet.vn/rss/doanh-nghiep.rss", "cat": "DN"},
    {"name": "VnBusiness BDS", "url": "https://vnbusiness.vn/rss/bat-dong-san.rss", "cat": "BĐS"},
    {"name": "VnBusiness CK", "url": "https://vnbusiness.vn/rss/chung-khoan.rss", "cat": "CK"},
    {"name": "VnBusiness TC", "url": "https://vnbusiness.vn/rss/tai-chinh.rss", "cat": "TC"},
    {"name": "VnBusiness DN", "url": "https://vnbusiness.vn/rss/doanh-nghiep.rss", "cat": "DN"},
    {"name": "VTC News KT", "url": "https://vtcnews.vn/rss/kinh-te.rss", "cat": "KD"},
    {"name": "VnBusiness TT", "url": "https://vnbusiness.vn/rss/thi-truong.rss", "cat": "TT"},
    {"name": "VnEconomy BDS", "url": "https://vneconomy.vn/bat-dong-san.rss", "cat": "BĐS"},
    {"name": "VnEconomy CK", "url": "https://vneconomy.vn/chung-khoan.rss", "cat": "CK"},
    {"name": "VnEconomy DK", "url": "https://vneconomy.vn/dau-tu.rss", "cat": "ĐT"},
    {"name": "VnEconomy DN", "url": "https://vneconomy.vn/doanh-nhan.rss", "cat": "DN"},
    {"name": "VnEconomy TC", "url": "https://vneconomy.vn/tai-chinh.rss", "cat": "TC"},
    {"name": "Thanh Niên KT", "url": "https://thanhnien.vn/rss/kinh-te.rss", "cat": "KD"},
    {"name": "Dân trí KD", "url": "https://dantri.com.vn/rss/kinh-doanh.rss", "cat": "KD"},
    {"name": "Dân trí BĐS", "url": "https://dantri.com.vn/rss/bat-dong-san.rss", "cat": "BĐS"},
    {"name": "Báo Xây dựng KT", "url": "https://baoxaydung.vn/rss/kinh-te.rss", "cat": "XD"},
    {"name": "Báo Xây dựng BĐS", "url": "https://baoxaydung.vn/rss/bat-dong-san.rss", "cat": "BĐS"},
    {"name": "NLD Kinh tế", "url": "https://nld.com.vn/rss/kinh-te.rss", "cat": "KD"},
    {"name": "VietnamPlus KT", "url": "https://www.vietnamplus.vn/rss/kinh-te.rss", "cat": "KD"},
    {"name": "CafeBiz BĐS", "url": "https://cafebiz.vn/rss/bat-dong-san.rss", "cat": "BĐS"},
    {"name": "CafeBiz CK", "url": "https://cafebiz.vn/rss/chung-khoan.rss", "cat": "CK"},
    {"name": "Tuổi Trẻ KT", "url": "https://tuoitre.vn/rss/kinh-te.rss", "cat": "KD"},
    {"name": "Tuổi Trẻ BĐS", "url": "https://tuoitre.vn/rss/nha-dat.rss", "cat": "BĐS"},
    {"name": "Nhân Dân KT", "url": "https://nhandan.vn/rss/kinh-te.rss", "cat": "KD"},
    {"name": "Tiền Phong KT", "url": "https://tienphong.vn/rss/kinh-te.rss", "cat": "KD"},
    {"name": "Soha KD", "url": "https://soha.vn/rss/kinh-doanh.rss", "cat": "KD"},
    {"name": "ANTĐ KT", "url": "https://anninhthudo.vn/rss/kinh-te.rss", "cat": "KD"},
    {"name": "CAND KT", "url": "https://cand.com.vn/rss/kinh-te.rss", "cat": "KD"},
    {"name": "Công Thương", "url": "https://congthuong.vn/rss/trang-chu.rss", "cat": "KD"},
    {"name": "Infonet KD", "url": "https://infonet.vietnamnet.vn/rss/kinh-doanh.rss", "cat": "KD"},
    {"name": "Kiến Thức KD", "url": "https://kienthuc.net.vn/rss/kinh-doanh.rss", "cat": "KD"},
    {"name": "PLO", "url": "https://plo.vn/rss/home.rss", "cat": "TT"},
    {"name": "Nguoiduatin KT", "url": "https://nguoiduatin.vn/rss/kinh-te.rss", "cat": "KD"},
    {"name": "Nguoiduatin BĐS", "url": "https://nguoiduatin.vn/rss/bat-dong-san.rss", "cat": "BĐS"},
    {"name": "KTVN Times", "url": "https://kinhtevn.com.vn/rss", "cat": "KD"},
    {"name": "VietTimes KT", "url": "https://viettimes.vn/rss/kinh-te.rss", "cat": "KD"},
    {"name": "VietTimes BĐS", "url": "https://viettimes.vn/rss/bat-dong-san.rss", "cat": "BĐS"},
    {"name": "Diễn đàn KT", "url": "https://diendankinhte.vn/rss", "cat": "KD"},
    {"name": "Công Luận KT", "url": "https://congluan.vn/rss/kinh-te.rss", "cat": "KD"},
    {"name": "Biz Việt", "url": "https://bizviet.vn/rss", "cat": "KD"},
    {"name": "Reatimes", "url": "https://reatimes.vn/rss", "cat": "BĐS"},
    {"name": "VTC News BĐS", "url": "https://vtcnews.vn/rss/bat-dong-san.rss", "cat": "BĐS"},
    {"name": "24h KD", "url": "https://www.24h.com.vn/upload/rss/kinhdoanh.rss", "cat": "KD"},
    {"name": "Docnhanh KT", "url": "https://docnhanh.vn/rss/kinh-te.rss", "cat": "KD"},
    {"name": "VnExpress TG", "url": "https://vnexpress.net/rss/the-gioi.rss", "cat": "TG"},
    {"name": "VnExpress TT", "url": "https://vnexpress.net/rss/thoi-su.rss", "cat": "TT"},
    {"name": "Vietnamnet CK", "url": "https://vietnamnet.vn/rss/chung-khoan.rss", "cat": "CK"},
    {"name": "Vietnamnet DT", "url": "https://vietnamnet.vn/rss/dau-tu.rss", "cat": "DT"},
    {"name": "Vietnamnet TC", "url": "https://vietnamnet.vn/rss/tai-chinh.rss", "cat": "TC"},
    {"name": "Vietnamnet TT", "url": "https://vietnamnet.vn/rss/thi-truong.rss", "cat": "TT"},
    {"name": "VTV KT", "url": "https://vtv.vn/rss/kinh-te.rss", "cat": "KD"},
    {"name": "VTV TC", "url": "https://vtv.vn/rss/kinh-te/tai-chinh.rss", "cat": "TC"},
    {"name": "VTV TT", "url": "https://vtv.vn/rss/kinh-te/thi-truong.rss", "cat": "TT"},
    {"name": "ZNEWS KD", "url": "https://znews.vn/rss/kinh-doanh-tai-chinh.rss", "cat": "KD"},
    {"name": "ZNEWS TT", "url": "https://znews.vn/rss/thoi-su.rss", "cat": "TT"},
    {"name": "TINMOI KT", "url": "https://tinmoi.vn/rss/kinh-te.rss", "cat": "KD"},
    {"name": "DAU_TU_VIET_NAM BDS", "url": "https://dautuvietnam.com.vn/rss/bat-dong-san.rss", "cat": "BĐS"},
    {"name": "DAU_TU_VIET_NAM CK", "url": "https://dautuvietnam.com.vn/rss/chung-khoan.rss", "cat": "CK"},
    {"name": "DAU_TU_VIET_NAM DN", "url": "https://dautuvietnam.com.vn/rss/doanh-nghiep.rss", "cat": "DN"},
    {"name": "DAU_TU_VIET_NAM KD", "url": "https://dautuvietnam.com.vn/rss/kinh-doanh.rss", "cat": "KD"},
    {"name": "DAU_TU_VIET_NAM TC", "url": "https://dautuvietnam.com.vn/rss/tai-chinh-ngan-hang.rss", "cat": "TC"},
    {"name": "AN_NINH_TIEN_TE CK", "url": "https://antt.vn/rss/chung-khoan.rss", "cat": "CK"},
    {"name": "AN_NINH_TIEN_TE TC", "url": "https://antt.vn/rss/tai-chinh.rss", "cat": "TC"},
    {"name": "NGAN_HANG_VN CK", "url": "https://nganhangvietnam.vn/rss/chung-khoan.rss", "cat": "CK"},
    {"name": "NGAN_HANG_VN TC", "url": "https://nganhangvietnam.vn/rss/tai-chinh.rss", "cat": "TC"},
    {"name": "NGAN_HANG_VN TT", "url": "https://nganhangvietnam.vn/rss/tin-tuc.rss", "cat": "TT"},
    {"name": "NGAN_HANG_VN BDS", "url": "https://nganhangvietnam.vn/rss/bat-dong-san.rss", "cat": "BĐS"},
    {"name": "NGAN_HANG_VN KD", "url": "https://nganhangvietnam.vn/rss/kinh-te.rss", "cat": "KD"},
    {"name": "DOI_SONG_VN BDS", "url": "https://doisongvietnam.vn/rss/bat-dong-san.rss", "cat": "BĐS"},
    {"name": "DOI_SONG_VN KD", "url": "https://doisongvietnam.vn/rss/kinh-doanh.rss", "cat": "KD"},
    {"name": "DOANH_NGHIEP_VN BDS_TT", "url": "https://doanhnghiepvn.vn/rss/thi-truong-bat-dong-san-1047.rss", "cat": "BĐS"},
    {"name": "DOANH_NGHIEP_VN BDS_PL", "url": "https://doanhnghiepvn.vn/rss/phap-ly-bat-dong-san-1049.rss", "cat": "BĐS"},
    {"name": "DOANH_NGHIEP_VN BDS_CS", "url": "https://doanhnghiepvn.vn/rss/bat-dong-san-va-cuoc-song-1050.rss", "cat": "BĐS"},
    {"name": "DOANH_NGHIEP_VN BDS_DN", "url": "https://doanhnghiepvn.vn/rss/doanh-nghiep-bat-dong-san-1051.rss", "cat": "BĐS"},
    {"name": "DOANH_NGHIEP_VN KD", "url": "https://doanhnghiepvn.vn/rss/kinh-doanh-va-tieu-dung-1052.rss", "cat": "KD"},
    {"name": "SUC_KHOE_DS KT", "url": "https://suckhoedoisong.vn/rss/kinh-te.rss", "cat": "KD"},
    {"name": "SUC_KHOE_DS BDS", "url": "https://suckhoedoisong.vn/rss/bat-dong-san.rss", "cat": "BĐS"},
    {"name": "SUC_KHOE_DS TC", "url": "https://suckhoedoisong.vn/rss/tai-chinh.rss", "cat": "TC"},
    {"name": "VIETNAM_BIZ BDS", "url": "https://vietnambiz.vn/rss/bat-dong-san.rss", "cat": "BĐS"},
    {"name": "VTV TG", "url": "https://vtv.vn/rss/the-gioi.rss", "cat": "TG"},
    {"name": "TINMOI BDS", "url": "https://tinmoi.vn/rss/bat-dong-san.rss", "cat": "BĐS"},
    {"name": "TINMOI TC", "url": "https://tinmoi.vn/rss/tai-chinh.rss", "cat": "TC"},
    {"name": "AN_NINH_TIEN_TE BDS", "url": "https://antt.vn/rss/bat-dong-san.rss", "cat": "BĐS"},
    {"name": "AN_NINH_TIEN_TE KD", "url": "https://antt.vn/rss/kinh-te-dau-tu.rss", "cat": "KD"},
    {"name": "VTC News TT", "url": "https://vtcnews.vn/rss/thoi-su.rss", "cat": "TT"},
    {"name": "VTC News TC", "url": "https://vtcnews.vn/rss/tai-chinh.rss", "cat": "TC"},
    {"name": "VnEconomy TT", "url": "https://vneconomy.vn/thi-truong.rss", "cat": "TT"},
    {"name": "VnEconomy KD2", "url": "https://vneconomy.vn/kinh-doanh.rss", "cat": "KD"},
]

API_SOURCES: list[dict] = [
    {"type": "cafef", "name": "CafeF BĐS", "cat": "BĐS", "zone_id": 18835, "domain": "https://cafef.vn"},
    {"type": "cafef", "name": "CafeF CK", "cat": "CK", "zone_id": 18831, "domain": "https://cafef.vn"},
    {"type": "cafef", "name": "CafeF DN", "cat": "DN", "zone_id": 18836, "domain": "https://cafef.vn"},
    {"type": "cafef", "name": "CafeF TC", "cat": "TC", "zone_id": 18834, "domain": "https://cafef.vn"},
    {"type": "cafef", "name": "CafeF Vĩ mô", "cat": "ĐT", "zone_id": 18833, "domain": "https://cafef.vn"},
    {"type": "cafef", "name": "CafeF Thị trường", "cat": "TT", "zone_id": 18839, "domain": "https://cafef.vn"},
    {"type": "cafef", "name": "CafeF BĐS - Thị trường", "cat": "BĐS", "zone_id": 18843, "domain": "https://cafef.vn"},
    {"type": "cafef", "name": "CafeF BĐS - Nội thất PT", "cat": "BĐS", "zone_id": 18846, "domain": "https://cafef.vn"},
    {"type": "cafef", "name": "CafeF BĐS - Du lịch", "cat": "BĐS", "zone_id": 188120, "domain": "https://cafef.vn"},
    {"type": "cafebiz", "name": "CafeBiz BĐS", "cat": "BĐS", "zone_id": 176127, "domain": "https://cafebiz.vn"},
    {"type": "cafebiz", "name": "CafeBiz CK", "cat": "CK", "zone_id": 176132, "domain": "https://cafebiz.vn"},
    {"type": "cafebiz", "name": "CafeBiz TC", "cat": "TC", "zone_id": 176117, "domain": "https://cafebiz.vn"},
    {"type": "cafebiz", "name": "CafeBiz Sản xuất", "cat": "SX", "zone_id": 176144, "domain": "https://cafebiz.vn"},
    {"type": "cafebiz", "name": "CafeBiz Startup", "cat": "KD", "zone_id": 176120, "domain": "https://cafebiz.vn"},
    {"type": "vietnamnet", "name": "VietnamNet KD", "cat": "KD", "category_id": "000003", "domain": "https://vietnamnet.vn"},
    {"type": "vietnamnet", "name": "VietnamNet TC", "cat": "TC", "category_id": "00000G", "domain": "https://vietnamnet.vn"},
    {"type": "vietnamnet", "name": "VietnamNet Đầu tư", "cat": "ĐT", "category_id": "00000H", "domain": "https://vietnamnet.vn"},
    {"type": "vietnamnet", "name": "VietnamNet Thị trường", "cat": "TT", "category_id": "00000J", "domain": "https://vietnamnet.vn"},
    {"type": "vietnamnet", "name": "VietnamNet CK", "cat": "CK", "category_id": "00002N", "domain": "https://vietnamnet.vn"},
    {"type": "vietnamnet", "name": "VietnamNet BĐS", "cat": "BĐS", "category_id": "00000E", "domain": "https://vietnamnet.vn"},
    {"type": "vietnamnet", "name": "VietnamNet Dự án", "cat": "BĐS", "category_id": "00001C", "domain": "https://vietnamnet.vn"},
    {"type": "vietnamnet", "name": "VietnamNet Thị trường BĐS", "cat": "BĐS", "category_id": "00004V", "domain": "https://vietnamnet.vn"},
]

SEARCH_TERMS: dict[str, list[str]] = {
    "VHM": ["VHM cổ phiếu", "VHM chứng khoán", "VHM Vinhomes"],
    "VIC": ["VIC cổ phiếu", "VIC chứng khoán", "VIC Vingroup"],
    "VRE": ["VRE cổ phiếu", "VRE chứng khoán", "VRE Vincom"],
    "NVL": ["NVL cổ phiếu", "NVL chứng khoán", "NVL Novaland"],
    "PDR": ["PDR cổ phiếu", "PDR chứng khoán", "PDR Phát Đạt"],
    "DXG": ["DXG cổ phiếu", "DXG chứng khoán", "DXG Đất Xanh"],
    "KDH": ["KDH cổ phiếu", "KDH chứng khoán", "KDH Khang Điền"],
    "NLG": ["NLG cổ phiếu", "NLG chứng khoán", "NLG Nam Long"],
    "CEO": ["CEO cổ phiếu", "CEO chứng khoán", "CEO Group"],
    "DIG": ["DIG cổ phiếu", "DIG chứng khoán", "DIG DIC Corp"],
    "KBC": ["KBC cổ phiếu", "KBC chứng khoán", "KBC Kinh Bắc"],
    "BCM": ["BCM cổ phiếu", "BCM chứng khoán", "BCM Becamex"],
    "SZC": ["SZC cổ phiếu", "SZC chứng khoán", "SZC Sonadezi"],
    "VCG": ["VCG cổ phiếu", "VCG chứng khoán", "VCG Vinaconex"],
    "CTD": ["CTD cổ phiếu", "CTD chứng khoán", "CTD Coteccons"],
    "HHV": ["HHV cổ phiếu", "HHV chứng khoán", "HHV Đèo Cả"],
    "CII": ["CII cổ phiếu", "CII chứng khoán", "CII hạ tầng"],
}

INDUSTRY_SEARCH = [
    "bất động sản trái phiếu doanh nghiệp",
    "khu công nghiệp đầu tư hạ tầng",
    "đầu tư công giải ngân cao tốc",
    "cổ phiếu bất động sản hôm nay",
    "dự án nhà ở pháp lý",
    "KCN khu chế xuất",
    "trái phiếu bất động sản phát hành",
]

CONFIG_KEYWORDS_DATA: list[dict] = []
_kwid = 0
for code, terms in SEARCH_TERMS.items():
    for term in terms:
        _kwid += 1
        CONFIG_KEYWORDS_DATA.append({
            "keyword_id": f"KW{_kwid:03d}",
            "keyword": term,
            "industry_group": "Bất động sản",
            "related_tickers": code,
            "event_type_suggestion": "stock_mention, company_news",
            "priority": "High",
            "note": f"Mã cổ phiếu {code}",
        })
for i, term in enumerate(INDUSTRY_SEARCH):
    _kwid += 1
    CONFIG_KEYWORDS_DATA.append({
        "keyword_id": f"KW{_kwid:03d}",
        "keyword": term,
        "industry_group": "Bất động sản / Hạ tầng",
        "related_tickers": ", ".join(STOCK_CODES),
        "event_type_suggestion": "industry_analysis, policy_update",
        "priority": "Medium",
        "note": "Tìm kiếm theo ngành",
    })

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

REQUEST_TIMEOUT = 30
MAX_RETRIES = 2

BLOCKED_DOMAINS = [
    "wikipedia.org", "hhs.gov", "grokipedia", "wikidata.org",
    "wikimedia.org", "windy.com", "pinterest", "nordinvasion.com",
    "youtube.com", "facebook.com",
]

VIETNAMESE_CHARS = re.compile(r"[ăâđêôơưàảãáạăằẳẵắặâầẩẫấậđèẻẽéẹêềểễếệìỉĩíịòỏõóọôồổỗốộơờởỡớợùủũúụưừửữứựỳỷỹýỵ]", re.IGNORECASE)

XLXS_PATH = r"C:\Users\PC\Downloads\DA2\data\K4_CRAWL_NHOM_2_BAT_DONG_SAN_XAY_DUNG_KCN.xlsx"

IDX_FLUSH_EVERY = 2000
