var STOCK_CODES = ["VHM","VIC","VRE","NVL","PDR","DXG","KDH","NLG","CEO","DIG","KBC","BCM","SZC","VCG","CTD","HHV","CII"];

var STOCK_PATTERN = new RegExp("\\b(" + STOCK_CODES.join("|") + ")\\b");

var COMPANY_KEYWORDS = {
  VHM: ["Vinhomes","Vinh Homes","Vinhome","C\u00f4ng ty C\u1ed5 ph\u1ea7n Vinhomes","Vinhomes Joint Stock Company"],
  VIC: ["Vingroup","T\u1eadp \u0111o\u00e0n Vingroup","Vin Group","Vinpearl","Vincom","Vingroup Joint Stock Company"],
  VRE: ["Vincom Retail","Vincom Mega Mall","Vincom Center","C\u00f4ng ty C\u1ed5 ph\u1ea7n Vincom Retail","Vincom Retail Joint Stock Company"],
  NVL: ["Novaland","Novaland Group","\u0110\u1ecba \u1ed1c Nova","NovaGroup","T\u1eadp \u0111o\u00e0n Novaland","C\u00f4ng ty C\u1ed5 ph\u1ea7n T\u1eadp \u0111o\u00e0n \u0110\u1ea7u t\u01b0 \u0110\u1ecba \u1ed1c Nova"],
  PDR: ["Ph\u00e1t \u0110\u1ea1t","Phat Dat","B\u1ea5t \u0111\u1ed9ng s\u1ea3n Ph\u00e1t \u0110\u1ea1t","C\u00f4ng ty C\u1ed5 ph\u1ea7n Ph\u00e1t tri\u1ec3n B\u1ea5t \u0111\u1ed9ng s\u1ea3n Ph\u00e1t \u0110\u1ea1t","Phat Dat Real Estate Development Corp"],
  DXG: ["\u0110\u1ea5t Xanh","Dat Xanh","T\u1eadp \u0111o\u00e0n \u0110\u1ea5t Xanh","Dat Xanh Group","\u0110\u1ea5t Xanh Group"],
  KDH: ["Khang \u0110i\u1ec1n","Nh\u00e0 Khang \u0110i\u1ec1n","Khang Dien","C\u00f4ng ty C\u1ed5 ph\u1ea7n \u0110\u1ea7u t\u01b0 v\u00e0 Kinh doanh Nh\u00e0 Khang \u0110i\u1ec1n","Khang Dien House Trading"],
  NLG: ["Nam Long","\u0110\u1ea7u t\u01b0 Nam Long","Nam Long Group","C\u00f4ng ty C\u1ed5 ph\u1ea7n \u0110\u1ea7u t\u01b0 Nam Long","Nam Long Investment Corporation"],
  CEO: ["CEO Group","T\u1eadp \u0111o\u00e0n CEO","CEO Group JSC","T\u1eadp \u0111o\u00e0n CEO Group"],
  DIG: ["DIC Corp","DIC Corporation","DIC Group","\u0110\u1ea7u t\u01b0 Ph\u00e1t tri\u1ec3n X\u00e2y d\u1ef1ng","T\u1ed5ng C\u00f4ng ty C\u1ed5 ph\u1ea7n \u0110\u1ea7u t\u01b0 Ph\u00e1t tri\u1ec3n X\u00e2y d\u1ef1ng","DIC Investment Development Construction"],
  KBC: ["Kinh B\u1eafc","\u0110\u00f4 th\u1ecb Kinh B\u1eafc","Kinh Bac","Khu c\u00f4ng nghi\u1ec7p Kinh B\u1eafc","T\u1ed5ng C\u00f4ng ty Ph\u00e1t tri\u1ec3n \u0110\u00f4 th\u1ecb Kinh B\u1eafc","Kinh Bac City Development"],
  BCM: ["Becamex","Becamex IDC","Becamex T\u1ed5ng C\u00f4ng ty \u0110\u1ea7u t\u01b0","T\u1ed5ng C\u00f4ng ty \u0110\u1ea7u t\u01b0 v\u00e0 Ph\u00e1t tri\u1ec3n C\u00f4ng nghi\u1ec7p Becamex","Becamex Investment and Industrial Development"],
  SZC: ["Sonadezi Ch\u00e2u \u0110\u1ee9c","S\u01a1n \u0110\u00e0i","Sonadezi","C\u00f4ng ty C\u1ed5 ph\u1ea7n Sonadezi Ch\u00e2u \u0110\u1ee9c","Khu c\u00f4ng nghi\u1ec7p Ch\u00e2u \u0110\u1ee9c"],
  VCG: ["Vinaconex","T\u1ed5ng C\u00f4ng ty C\u1ed5 ph\u1ea7n Xu\u1ea5t nh\u1eadp kh\u1ea9u X\u00e2y d\u1ef1ng Vi\u1ec7t Nam","Xu\u1ea5t nh\u1eadp kh\u1ea9u X\u00e2y d\u1ef1ng Vi\u1ec7t Nam","Vietnam Construction Import Export"],
  CTD: ["Coteccons","X\u00e2y d\u1ef1ng Coteccons","Coteccons Construction","C\u00f4ng ty C\u1ed5 ph\u1ea7n X\u00e2y d\u1ef1ng Coteccons","Coteccons Construction Joint Stock Company"],
  HHV: ["\u0110\u00e8o C\u1ea3","Deo Ca","H\u1ea1 t\u1ea7ng Giao th\u00f4ng \u0110\u00e8o C\u1ea3","C\u00f4ng ty C\u1ed5 ph\u1ea7n \u0110\u1ea7u t\u01b0 H\u1ea1 t\u1ea7ng Giao th\u00f4ng \u0110\u00e8o C\u1ea3","Highway Infrastructure Investment"],
  CII: ["CII Infrastructure","C\u00f4ng ty C\u1ed5 ph\u1ea7n \u0110\u1ea7u t\u01b0 H\u1ea1 t\u1ea7ng K\u1ef9 thu\u1eadt Th\u00e0nh ph\u1ed1 H\u1ed3 Ch\u00ed Minh","H\u1ea1 t\u1ea7ng K\u1ef9 thu\u1eadt TP HCM","CII Infrastructure Investment"]
};

var COMPANY_INFO = [
  {code:"VHM",full_name:"C\u00f4ng ty C\u1ed5 ph\u1ea7n Vinhomes",english_name:"Vinhomes Joint Stock Company",former_name:"",exchange:"HOSE",industry:"B\u1ea5t \u0111\u1ed9ng s\u1ea3n nh\u00e0 \u1edf",website:"https://vinhomes.vn",established:"2008",employees:"18.000+",business:"Ph\u00e1t tri\u1ec3n khu \u0111\u00f4 th\u1ecb, c\u0103n h\u1ed9 chung c\u01b0, nh\u00e0 \u1edf x\u00e3 h\u1ed9i",keywords:"Vinhomes, Vinh Homes, VHM"},
  {code:"VIC",full_name:"T\u1eadp \u0111o\u00e0n Vingroup",english_name:"Vingroup Joint Stock Company",former_name:"Vinpearl, Vincom",exchange:"HOSE",industry:"\u0110a ng\u00e0nh (B\u0110S, b\u00e1n l\u1ebb, y t\u1ebf, gi\u00e1o d\u1ee5c)",website:"https://vingroup.net",established:"1993",employees:"70.000+",business:"\u0110\u1ea7u t\u01b0, ph\u00e1t tri\u1ec3n b\u1ea5t \u0111\u1ed9ng s\u1ea3n, trung t\u00e2m th\u01b0\u01a1ng m\u1ea1i, kh\u00e1ch s\u1ea1n, b\u1ec7nh vi\u1ec7n",keywords:"Vingroup, VIC"},
  {code:"VRE",full_name:"C\u00f4ng ty C\u1ed5 ph\u1ea7n Vincom Retail",english_name:"Vincom Retail Joint Stock Company",former_name:"",exchange:"HOSE",industry:"B\u1ea5t \u0111\u1ed9ng s\u1ea3n b\u00e1n l\u1ebb",website:"https://vincom.com.vn",established:"2012",employees:"3.000+",business:"S\u1edf h\u1eefu, v\u1eadn h\u00e0nh trung t\u00e2m th\u01b0\u01a1ng m\u1ea1i Vincom, Vincom Mega Mall",keywords:"Vincom Retail, VRE"},
  {code:"NVL",full_name:"C\u00f4ng ty C\u1ed5 ph\u1ea7n T\u1eadp \u0111o\u00e0n \u0110\u1ea7u t\u01b0 \u0110\u1ecba \u1ed1c Nova (Novaland)",english_name:"Novaland Group",former_name:"",exchange:"HOSE",industry:"B\u1ea5t \u0111\u1ed9ng s\u1ea3n nh\u00e0 \u1edf, ngh\u1ec9 d\u01b0\u1ee1ng",website:"https://novaland.com.vn",established:"2007",employees:"5.000+",business:"Ph\u00e1t tri\u1ec3n b\u1ea5t \u0111\u1ed9ng s\u1ea3n nh\u00e0 \u1edf, khu \u0111\u00f4 th\u1ecb, resort",keywords:"Novaland, NVL, \u0110\u1ecba \u1ed1c Nova"},
  {code:"PDR",full_name:"C\u00f4ng ty C\u1ed5 ph\u1ea7n Ph\u00e1t tri\u1ec3n B\u1ea5t \u0111\u1ed9ng s\u1ea3n Ph\u00e1t \u0110\u1ea1t",english_name:"Phat Dat Real Estate Development Corp",former_name:"",exchange:"HOSE",industry:"B\u1ea5t \u0111\u1ed9ng s\u1ea3n nh\u00e0 \u1edf",website:"https://phatdat.com.vn",established:"2004",employees:"800+",business:"\u0110\u1ea7u t\u01b0, ph\u00e1t tri\u1ec3n d\u1ef1 \u00e1n b\u1ea5t \u0111\u1ed9ng s\u1ea3n nh\u00e0 \u1edf, khu d\u00e2n c\u01b0",keywords:"Ph\u00e1t \u0110\u1ea1t, PDR, B\u1ea5t \u0111\u1ed9ng s\u1ea3n Ph\u00e1t \u0110\u1ea1t"},
  {code:"DXG",full_name:"T\u1eadp \u0111o\u00e0n \u0110\u1ea5t Xanh",english_name:"Dat Xanh Group",former_name:"",exchange:"HOSE",industry:"D\u1ecbch v\u1ee5 v\u00e0 m\u00f4i gi\u1edbi b\u1ea5t \u0111\u1ed9ng s\u1ea3n",website:"https://datxanh.vn",established:"2003",employees:"6.000+",business:"M\u00f4i gi\u1edbi, s\u00e0n giao d\u1ecbch b\u1ea5t \u0111\u1ed9ng s\u1ea3n, ph\u00e1t tri\u1ec3n d\u1ef1 \u00e1n",keywords:"\u0110\u1ea5t Xanh, Dat Xanh, DXG"},
  {code:"KDH",full_name:"C\u00f4ng ty C\u1ed5 ph\u1ea7n \u0110\u1ea7u t\u01b0 v\u00e0 Kinh doanh Nh\u00e0 Khang \u0110i\u1ec1n",english_name:"Khang Dien House Trading and Investment JSC",former_name:"",exchange:"HOSE",industry:"B\u1ea5t \u0111\u1ed9ng s\u1ea3n nh\u00e0 \u1edf",website:"https://khangdien.com.vn",established:"2001",employees:"500+",business:"Ph\u00e1t tri\u1ec3n nh\u00e0 \u1edf, khu d\u00e2n c\u01b0, c\u0103n h\u1ed9",keywords:"Khang \u0110i\u1ec1n, KDH, Nh\u00e0 Khang \u0110i\u1ec1n"},
  {code:"NLG",full_name:"C\u00f4ng ty C\u1ed5 ph\u1ea7n \u0110\u1ea7u t\u01b0 Nam Long",english_name:"Nam Long Investment Corporation",former_name:"",exchange:"HOSE",industry:"B\u1ea5t \u0111\u1ed9ng s\u1ea3n nh\u00e0 \u1edf",website:"https://namlong.com",established:"1992",employees:"1.500+",business:"Ph\u00e1t tri\u1ec3n khu \u0111\u00f4 th\u1ecb, nh\u00e0 \u1edf, c\u0103n h\u1ed9",keywords:"Nam Long, NLG, \u0110\u1ea7u t\u01b0 Nam Long"},
  {code:"CEO",full_name:"T\u1eadp \u0111o\u00e0n CEO",english_name:"CEO Group",former_name:"CEO Group",exchange:"HNX",industry:"B\u1ea5t \u0111\u1ed9ng s\u1ea3n v\u00e0 d\u1ecbch v\u1ee5 li\u00ean quan",website:"https://ceogroup.com.vn",established:"2005",employees:"1.000+",business:"Ph\u00e1t tri\u1ec3n b\u1ea5t \u0111\u1ed9ng s\u1ea3n, kh\u00e1ch s\u1ea1n, \u0111\u00e0o t\u1ea1o",keywords:"CEO Group, CEO"},
  {code:"DIG",full_name:"T\u1ed5ng C\u00f4ng ty C\u1ed5 ph\u1ea7n \u0110\u1ea7u t\u01b0 Ph\u00e1t tri\u1ec3n X\u00e2y d\u1ef1ng",english_name:"DIC Corporation",former_name:"DIC Corp",exchange:"HOSE",industry:"B\u1ea5t \u0111\u1ed9ng s\u1ea3n v\u00e0 x\u00e2y d\u1ef1ng",website:"https://dic.vn",established:"2000",employees:"2.000+",business:"\u0110\u1ea7u t\u01b0, ph\u00e1t tri\u1ec3n d\u1ef1 \u00e1n b\u1ea5t \u0111\u1ed9ng s\u1ea3n, h\u1ea1 t\u1ea7ng khu c\u00f4ng nghi\u1ec7p",keywords:"DIC Corp, DIG, DIC Corporation, \u0110\u1ea7u t\u01b0 Ph\u00e1t tri\u1ec3n X\u00e2y d\u1ef1ng"},
  {code:"KBC",full_name:"T\u1ed5ng C\u00f4ng ty Ph\u00e1t tri\u1ec3n \u0110\u00f4 th\u1ecb Kinh B\u1eafc",english_name:"Kinh Bac City Development Holding Corporation",former_name:"",exchange:"HOSE",industry:"Khu c\u00f4ng nghi\u1ec7p v\u00e0 \u0111\u00f4 th\u1ecb",website:"https://kinhbac.com.vn",established:"2000",employees:"700+",business:"Ph\u00e1t tri\u1ec3n khu c\u00f4ng nghi\u1ec7p, khu \u0111\u00f4 th\u1ecb",keywords:"Kinh B\u1eafc, KBC, \u0110\u00f4 th\u1ecb Kinh B\u1eafc"},
  {code:"BCM",full_name:"T\u1ed5ng C\u00f4ng ty \u0110\u1ea7u t\u01b0 v\u00e0 Ph\u00e1t tri\u1ec3n C\u00f4ng nghi\u1ec7p Becamex",english_name:"Becamex Investment and Industrial Development Corporation",former_name:"",exchange:"HOSE",industry:"Khu c\u00f4ng nghi\u1ec7p v\u00e0 h\u1ea1 t\u1ea7ng",website:"https://becamex.com.vn",established:"1976",employees:"3.000+",business:"Ph\u00e1t tri\u1ec3n h\u1ea1 t\u1ea7ng khu c\u00f4ng nghi\u1ec7p, \u0111\u00f4 th\u1ecb, d\u1ecbch v\u1ee5",keywords:"Becamex, BCM, Becamex T\u1ed5ng C\u00f4ng ty \u0110\u1ea7u t\u01b0"},
  {code:"SZC",full_name:"C\u00f4ng ty C\u1ed5 ph\u1ea7n Sonadezi Ch\u00e2u \u0110\u1ee9c",english_name:"Sonadezi Chau Duc Company Limited",former_name:"S\u01a1n \u0110\u00e0i",exchange:"HOSE",industry:"Khu c\u00f4ng nghi\u1ec7p",website:"https://sonadezi.edu.vn",established:"2004",employees:"200+",business:"Ph\u00e1t tri\u1ec3n h\u1ea1 t\u1ea7ng khu c\u00f4ng nghi\u1ec7p, b\u1ea5t \u0111\u1ed9ng s\u1ea3n cho thu\u00ea",keywords:"Sonadezi Ch\u00e2u \u0110\u1ee9c, SZC, S\u01a1n \u0110\u00e0i"},
  {code:"VCG",full_name:"T\u1ed5ng C\u00f4ng ty C\u1ed5 ph\u1ea7n Xu\u1ea5t nh\u1eadp kh\u1ea9u v\u00e0 X\u00e2y d\u1ef1ng Vi\u1ec7t Nam (Vinaconex)",english_name:"Vietnam Construction and Import-Export Joint Stock Corporation",former_name:"",exchange:"HOSE",industry:"X\u00e2y d\u1ef1ng v\u00e0 b\u1ea5t \u0111\u1ed9ng s\u1ea3n",website:"https://vinaconex.com.vn",established:"1988",employees:"5.000+",business:"X\u00e2y d\u1ef1ng d\u00e2n d\u1ee5ng, c\u00f4ng nghi\u1ec7p, ph\u00e1t tri\u1ec3n khu \u0111\u00f4 th\u1ecb",keywords:"Vinaconex, VCG, Xu\u1ea5t nh\u1eadp kh\u1ea9u X\u00e2y d\u1ef1ng Vi\u1ec7t Nam"},
  {code:"CTD",full_name:"C\u00f4ng ty C\u1ed5 ph\u1ea7n X\u00e2y d\u1ef1ng Coteccons",english_name:"Coteccons Construction Joint Stock Company",former_name:"",exchange:"HOSE",industry:"X\u00e2y d\u1ef1ng",website:"https://coteccons.vn",established:"2004",employees:"10.000+",business:"T\u1ed5ng th\u1ea7u x\u00e2y d\u1ef1ng d\u00e2n d\u1ee5ng, c\u00f4ng nghi\u1ec7p, h\u1ea1 t\u1ea7ng",keywords:"Coteccons, CTD, X\u00e2y d\u1ef1ng Coteccons"},
  {code:"HHV",full_name:"C\u00f4ng ty C\u1ed5 ph\u1ea7n \u0110\u1ea7u t\u01b0 H\u1ea1 t\u1ea7ng Giao th\u00f4ng \u0110\u00e8o C\u1ea3",english_name:"Highway Infrastructure Investment Joint Stock Company",former_name:"",exchange:"HOSE",industry:"H\u1ea1 t\u1ea7ng giao th\u00f4ng",website:"https://deoca.vn",established:"2015",employees:"300+",business:"\u0110\u1ea7u t\u01b0, x\u00e2y d\u1ef1ng v\u00e0 v\u1eadn h\u00e0nh c\u00f4ng tr\u00ecnh h\u1ea1 t\u1ea7ng giao th\u00f4ng",keywords:"\u0110\u00e8o C\u1ea3, HHV, H\u1ea1 t\u1ea7ng Giao th\u00f4ng \u0110\u00e8o C\u1ea3"},
  {code:"CII",full_name:"C\u00f4ng ty C\u1ed5 ph\u1ea7n \u0110\u1ea7u t\u01b0 H\u1ea1 t\u1ea7ng K\u1ef9 thu\u1eadt Th\u00e0nh ph\u1ed1 H\u1ed3 Ch\u00ed Minh",english_name:"CII Infrastructure Investment Joint Stock Company",former_name:"",exchange:"HOSE",industry:"H\u1ea1 t\u1ea7ng k\u1ef9 thu\u1eadt",website:"https://cii.vn",established:"2001",employees:"800+",business:"\u0110\u1ea7u t\u01b0, x\u00e2y d\u1ef1ng h\u1ea1 t\u1ea7ng giao th\u00f4ng, c\u1ea7u \u0111\u01b0\u1eddng, n\u01b0\u1edbc s\u1ea1ch",keywords:"H\u1ea1 t\u1ea7ng K\u1ef9 thu\u1eadt TP HCM, CII, CII Infrastructure"}
];

var SOURCE_INFO = [
  {name:"CafeF",domain:"cafef.vn",categories:"B\u0110S, CK, DN, TC, V\u0129 m\u00f4, Th\u1ecb tr\u01b0\u1eddng, B\u0110S-TT, B\u0110S-NT, B\u0110S-DL",type:"RSS+API",rss:"C\u00f3",articles:"50k+",note:"API timelinelist, 15 b\u00e0i/trang, crawl \u0111\u1ebfn empty",has_rss:true,has_api:true},
  {name:"CafeBiz",domain:"cafebiz.vn",categories:"B\u0110S, CK, TC, SX, Startup",type:"RSS+API",rss:"C\u00f3",articles:"20k+",note:"API timelinelist, 15 b\u00e0i/trang, crawl \u0111\u1ebfn empty",has_rss:true,has_api:true},
  {name:"VietnamNet",domain:"vietnamnet.vn",categories:"KD, TC, \u0110T, TT, CK, B\u0110S, DN, D\u1ef1 \u00e1n, TT B\u0110S",type:"RSS+API",rss:"C\u00f3",articles:"30k+",note:"API JSON POST, 50 b\u00e0i/trang, crawl \u0111\u1ebfn empty",has_rss:true,has_api:true},
  {name:"VnExpress",domain:"vnexpress.net",categories:"KD, B\u0110S, TG, TT",type:"RSS",rss:"C\u00f3",articles:"15k+",note:"Ch\u1ec9 RSS (kh\u00f4ng c\u00f3 API)",has_rss:true,has_api:false},
  {name:"VnBusiness",domain:"vnbusiness.vn",categories:"B\u0110S, CK, TC, DN, TT",type:"RSS",rss:"C\u00f3",articles:"5k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"VnEconomy",domain:"vneconomy.vn",categories:"B\u0110S, CK, \u0110T, DN, TC, TT, KD",type:"RSS",rss:"C\u00f3",articles:"5k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"Thanh Ni\u00ean",domain:"thanhnien.vn",categories:"KT, KD",type:"RSS",rss:"C\u00f3",articles:"3k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"D\u00e2n tr\u00ed",domain:"dantri.com.vn",categories:"KD, B\u0110S",type:"RSS",rss:"C\u00f3",articles:"5k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"B\u00e1o X\u00e2y d\u1ef1ng",domain:"baoxaydung.vn",categories:"KT, B\u0110S",type:"RSS",rss:"C\u00f3",articles:"3k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"NLD",domain:"nld.com.vn",categories:"Kinh t\u1ebf",type:"RSS",rss:"C\u00f3",articles:"2k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"VietnamPlus",domain:"vietnamplus.vn",categories:"KT",type:"RSS",rss:"C\u00f3",articles:"2k+",note:"Ch\u1ec9 RSS, c\u00e1c feed \u0111\u1ed3ng nh\u1ea5t (KT=B\u0110S=TT=CK=DN)",has_rss:true,has_api:false},
  {name:"Tu\u1ed5i Tr\u1ebb",domain:"tuoitre.vn",categories:"KT, B\u0110S",type:"RSS",rss:"C\u00f3",articles:"5k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"Nh\u00e2n D\u00e2n",domain:"nhandan.vn",categories:"Kinh t\u1ebf",type:"RSS",rss:"C\u00f3",articles:"2k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"Ti\u1ec1n Phong",domain:"tienphong.vn",categories:"Kinh t\u1ebf",type:"RSS",rss:"C\u00f3",articles:"2k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"Soha",domain:"soha.vn",categories:"Kinh doanh",type:"RSS",rss:"C\u00f3",articles:"2k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"ANT\u0110",domain:"anninhthudo.vn",categories:"KT, B\u0110S",type:"RSS",rss:"C\u00f3",articles:"2k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"CAND",domain:"cand.com.vn",categories:"Kinh t\u1ebf",type:"RSS",rss:"C\u00f3",articles:"2k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"C\u00f4ng Th\u01b0\u01a1ng",domain:"congthuong.vn",categories:"Kinh t\u1ebf",type:"RSS",rss:"C\u00f3",articles:"1k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"S\u1ee9c Kh\u1ecfe & \u0110S",domain:"suckhoedoisong.vn",categories:"KT, B\u0110S, TC",type:"RSS",rss:"C\u00f3",articles:"2k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"Infonet",domain:"infonet.vietnamnet.vn",categories:"Kinh doanh",type:"RSS",rss:"C\u00f3",articles:"1k+",note:"Ch\u1ec9 RSS, thu\u1ed9c VietnamNet",has_rss:true,has_api:false},
  {name:"Ki\u1ebfn Th\u1ee9c",domain:"kienthuc.net.vn",categories:"Kinh doanh",type:"RSS",rss:"C\u00f3",articles:"2k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"PLO",domain:"plo.vn",categories:"T\u1ed5ng h\u1ee3p",type:"RSS",rss:"C\u00f3",articles:"2k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"VTC News",domain:"vtcnews.vn",categories:"KT, B\u0110S, TT, TC",type:"RSS",rss:"C\u00f3",articles:"1k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"24h",domain:"24h.com.vn",categories:"Kinh doanh",type:"RSS",rss:"C\u00f3",articles:"1k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"Docnhanh",domain:"docnhanh.vn",categories:"Kinh t\u1ebf",type:"RSS",rss:"C\u00f3",articles:"1k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"Nguoiduatin",domain:"nguoiduatin.vn",categories:"KT, B\u0110S",type:"RSS",rss:"C\u00f3",articles:"2k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"KTVN Times",domain:"kinhtevn.com.vn",categories:"Kinh t\u1ebf",type:"RSS",rss:"C\u00f3",articles:"1k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"VietTimes",domain:"viettimes.vn",categories:"KT, B\u0110S",type:"RSS",rss:"C\u00f3",articles:"2k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"Di\u1ec5n \u0111\u00e0n KT",domain:"diendankinhte.vn",categories:"Kinh t\u1ebf",type:"RSS",rss:"C\u00f3",articles:"1k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"C\u00f4ng Lu\u1eadn",domain:"congluan.vn",categories:"Kinh t\u1ebf",type:"RSS",rss:"C\u00f3",articles:"2k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"Biz Vi\u1ec7t",domain:"bizviet.vn",categories:"Kinh doanh",type:"RSS",rss:"C\u00f3",articles:"1k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"Reatimes",domain:"reatimes.vn",categories:"B\u0110S",type:"RSS",rss:"C\u00f3",articles:"1k+",note:"Ch\u1ec9 RSS, chuy\u00ean B\u0110S",has_rss:true,has_api:false},
  {name:"VTV",domain:"vtv.vn",categories:"KT, TC, TT, TG",type:"RSS",rss:"C\u00f3",articles:"5k+",note:"\u0110\u00e0i Truy\u1ec1n h\u00ecnh Vi\u1ec7t Nam",has_rss:true,has_api:false},
  {name:"ZNEWS",domain:"znews.vn",categories:"KD, TT",type:"RSS",rss:"C\u00f3",articles:"3k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"TINMOI",domain:"tinmoi.vn",categories:"KT, B\u0110S, TC",type:"RSS",rss:"C\u00f3",articles:"2k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"DAU_TU_VIET_NAM",domain:"dautuvietnam.com.vn",categories:"B\u0110S, CK, DN, KD, TC",type:"RSS",rss:"C\u00f3",articles:"3k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"AN_NINH_TIEN_TE",domain:"antt.vn",categories:"CK, TC, B\u0110S, KD",type:"RSS",rss:"C\u00f3",articles:"2k+",note:"An Ninh Ti\u1ec1n T\u1ec7",has_rss:true,has_api:false},
  {name:"VIETNAM_BIZ",domain:"vietnambiz.vn",categories:"B\u0110S, CK, KD",type:"RSS",rss:"C\u00f3",articles:"1k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"NGAN_HANG_VN",domain:"nganhangvietnam.vn",categories:"CK, TC, TT, B\u0110S, KD",type:"RSS",rss:"C\u00f3",articles:"1k+",note:"Chuy\u00ean ng\u00e2n h\u00e0ng, t\u00e0i ch\u00ednh",has_rss:true,has_api:false},
  {name:"DOI_SONG_VN",domain:"doisongvietnam.vn",categories:"B\u0110S, KD",type:"RSS",rss:"C\u00f3",articles:"1k+",note:"Ch\u1ec9 RSS",has_rss:true,has_api:false},
  {name:"DOANH_NGHIEP_VN",domain:"doanhnghiepvn.vn",categories:"B\u0110S_TT, B\u0110S_PL, B\u0110S_CS, B\u0110S_DN, KD",type:"RSS",rss:"C\u00f3",articles:"2k+",note:"Chuy\u00ean B\u0110S, nhi\u1ec1u chuy\u00ean m\u1ee5c",has_rss:true,has_api:false}
];

var RSS_SOURCES = [
  {name:"Cafef BDS",url:"https://cafef.vn/bat-dong-san.rss",cat:"B\u0110S"},
  {name:"Cafef CK",url:"https://cafef.vn/thi-truong-chung-khoan.rss",cat:"CK"},
  {name:"Cafef DN",url:"https://cafef.vn/doanh-nghiep.rss",cat:"DN"},
  {name:"Cafef TC",url:"https://cafef.vn/tai-chinh-ngan-hang.rss",cat:"TC"},
  {name:"VnExpress KD",url:"https://vnexpress.net/rss/kinh-doanh.rss",cat:"KD"},
  {name:"VnExpress BDS",url:"https://vnexpress.net/rss/bat-dong-san.rss",cat:"B\u0110S"},
  {name:"Vietnamnet KD",url:"https://vietnamnet.vn/rss/kinh-doanh.rss",cat:"KD"},
  {name:"Vietnamnet BDS",url:"https://vietnamnet.vn/rss/bat-dong-san.rss",cat:"B\u0110S"},
  {name:"Vietnamnet DN",url:"https://vietnamnet.vn/rss/doanh-nghiep.rss",cat:"DN"},
  {name:"VnBusiness BDS",url:"https://vnbusiness.vn/rss/bat-dong-san.rss",cat:"B\u0110S"},
  {name:"VnBusiness CK",url:"https://vnbusiness.vn/rss/chung-khoan.rss",cat:"CK"},
  {name:"VnBusiness TC",url:"https://vnbusiness.vn/rss/tai-chinh.rss",cat:"TC"},
  {name:"VnBusiness DN",url:"https://vnbusiness.vn/rss/doanh-nghiep.rss",cat:"DN"},
  {name:"VTC News KT",url:"https://vtcnews.vn/rss/kinh-te.rss",cat:"KD"},
  {name:"VnBusiness TT",url:"https://vnbusiness.vn/rss/thi-truong.rss",cat:"TT"},
  {name:"VnEconomy BDS",url:"https://vneconomy.vn/bat-dong-san.rss",cat:"B\u0110S"},
  {name:"VnEconomy CK",url:"https://vneconomy.vn/chung-khoan.rss",cat:"CK"},
  {name:"VnEconomy DK",url:"https://vneconomy.vn/dau-tu.rss",cat:"\u0110T"},
  {name:"VnEconomy DN",url:"https://vneconomy.vn/doanh-nhan.rss",cat:"DN"},
  {name:"VnEconomy TC",url:"https://vneconomy.vn/tai-chinh.rss",cat:"TC"},
  {name:"Thanh Ni\u00ean KT",url:"https://thanhnien.vn/rss/kinh-te.rss",cat:"KD"},
  {name:"D\u00e2n tr\u00ed KD",url:"https://dantri.com.vn/rss/kinh-doanh.rss",cat:"KD"},
  {name:"D\u00e2n tr\u00ed B\u0110S",url:"https://dantri.com.vn/rss/bat-dong-san.rss",cat:"B\u0110S"},
  {name:"B\u00e1o X\u00e2y d\u1ef1ng KT",url:"https://baoxaydung.vn/rss/kinh-te.rss",cat:"XD"},
  {name:"B\u00e1o X\u00e2y d\u1ef1ng B\u0110S",url:"https://baoxaydung.vn/rss/bat-dong-san.rss",cat:"B\u0110S"},
  {name:"NLD Kinh t\u1ebf",url:"https://nld.com.vn/rss/kinh-te.rss",cat:"KD"},
  {name:"VietnamPlus KT",url:"https://www.vietnamplus.vn/rss/kinh-te.rss",cat:"KD"},
  {name:"CafeBiz B\u0110S",url:"https://cafebiz.vn/rss/bat-dong-san.rss",cat:"B\u0110S"},
  {name:"CafeBiz CK",url:"https://cafebiz.vn/rss/chung-khoan.rss",cat:"CK"},
  {name:"Tu\u1ed5i Tr\u1ebb KT",url:"https://tuoitre.vn/rss/kinh-te.rss",cat:"KD"},
  {name:"Tu\u1ed5i Tr\u1ebb B\u0110S",url:"https://tuoitre.vn/rss/nha-dat.rss",cat:"B\u0110S"},
  {name:"Nh\u00e2n D\u00e2n KT",url:"https://nhandan.vn/rss/kinh-te.rss",cat:"KD"},
  {name:"Ti\u1ec1n Phong KT",url:"https://tienphong.vn/rss/kinh-te.rss",cat:"KD"},
  {name:"Soha KD",url:"https://soha.vn/rss/kinh-doanh.rss",cat:"KD"},
  {name:"ANT\u0110 KT",url:"https://anninhthudo.vn/rss/kinh-te.rss",cat:"KD"},
  {name:"CAND KT",url:"https://cand.com.vn/rss/kinh-te.rss",cat:"KD"},
  {name:"C\u00f4ng Th\u01b0\u01a1ng",url:"https://congthuong.vn/rss/trang-chu.rss",cat:"KD"},
  {name:"Infonet KD",url:"https://infonet.vietnamnet.vn/rss/kinh-doanh.rss",cat:"KD"},
  {name:"Ki\u1ebfn Th\u1ee9c KD",url:"https://kienthuc.net.vn/rss/kinh-doanh.rss",cat:"KD"},
  {name:"PLO",url:"https://plo.vn/rss/home.rss",cat:"TT"},
  {name:"Nguoiduatin KT",url:"https://nguoiduatin.vn/rss/kinh-te.rss",cat:"KD"},
  {name:"Nguoiduatin B\u0110S",url:"https://nguoiduatin.vn/rss/bat-dong-san.rss",cat:"B\u0110S"},
  {name:"KTVN Times",url:"https://kinhtevn.com.vn/rss",cat:"KD"},
  {name:"VietTimes KT",url:"https://viettimes.vn/rss/kinh-te.rss",cat:"KD"},
  {name:"VietTimes B\u0110S",url:"https://viettimes.vn/rss/bat-dong-san.rss",cat:"B\u0110S"},
  {name:"Di\u1ec5n \u0111\u00e0n KT",url:"https://diendankinhte.vn/rss",cat:"KD"},
  {name:"C\u00f4ng Lu\u1eadn KT",url:"https://congluan.vn/rss/kinh-te.rss",cat:"KD"},
  {name:"Biz Vi\u1ec7t",url:"https://bizviet.vn/rss",cat:"KD"},
  {name:"Reatimes",url:"https://reatimes.vn/rss",cat:"B\u0110S"},
  {name:"VTC News B\u0110S",url:"https://vtcnews.vn/rss/bat-dong-san.rss",cat:"B\u0110S"},
  {name:"24h KD",url:"https://www.24h.com.vn/upload/rss/kinhdoanh.rss",cat:"KD"},
  {name:"Docnhanh KT",url:"https://docnhanh.vn/rss/kinh-te.rss",cat:"KD"},
  {name:"VnExpress TG",url:"https://vnexpress.net/rss/the-gioi.rss",cat:"TG"},
  {name:"VnExpress TT",url:"https://vnexpress.net/rss/thoi-su.rss",cat:"TT"},
  {name:"Vietnamnet CK",url:"https://vietnamnet.vn/rss/chung-khoan.rss",cat:"CK"},
  {name:"Vietnamnet DT",url:"https://vietnamnet.vn/rss/dau-tu.rss",cat:"DT"},
  {name:"Vietnamnet TC",url:"https://vietnamnet.vn/rss/tai-chinh.rss",cat:"TC"},
  {name:"Vietnamnet TT",url:"https://vietnamnet.vn/rss/thi-truong.rss",cat:"TT"},
  {name:"VTV KT",url:"https://vtv.vn/rss/kinh-te.rss",cat:"KD"},
  {name:"VTV TC",url:"https://vtv.vn/rss/kinh-te/tai-chinh.rss",cat:"TC"},
  {name:"VTV TT",url:"https://vtv.vn/rss/kinh-te/thi-truong.rss",cat:"TT"},
  {name:"ZNEWS KD",url:"https://znews.vn/rss/kinh-doanh-tai-chinh.rss",cat:"KD"},
  {name:"ZNEWS TT",url:"https://znews.vn/rss/thoi-su.rss",cat:"TT"},
  {name:"TINMOI KT",url:"https://tinmoi.vn/rss/kinh-te.rss",cat:"KD"},
  {name:"DAU_TU_VIET_NAM BDS",url:"https://dautuvietnam.com.vn/rss/bat-dong-san.rss",cat:"B\u0110S"},
  {name:"DAU_TU_VIET_NAM CK",url:"https://dautuvietnam.com.vn/rss/chung-khoan.rss",cat:"CK"},
  {name:"DAU_TU_VIET_NAM DN",url:"https://dautuvietnam.com.vn/rss/doanh-nghiep.rss",cat:"DN"},
  {name:"DAU_TU_VIET_NAM KD",url:"https://dautuvietnam.com.vn/rss/kinh-doanh.rss",cat:"KD"},
  {name:"DAU_TU_VIET_NAM TC",url:"https://dautuvietnam.com.vn/rss/tai-chinh-ngan-hang.rss",cat:"TC"},
  {name:"AN_NINH_TIEN_TE CK",url:"https://antt.vn/rss/chung-khoan.rss",cat:"CK"},
  {name:"AN_NINH_TIEN_TE TC",url:"https://antt.vn/rss/tai-chinh.rss",cat:"TC"},
  {name:"NGAN_HANG_VN CK",url:"https://nganhangvietnam.vn/rss/chung-khoan.rss",cat:"CK"},
  {name:"NGAN_HANG_VN TC",url:"https://nganhangvietnam.vn/rss/tai-chinh.rss",cat:"TC"},
  {name:"NGAN_HANG_VN TT",url:"https://nganhangvietnam.vn/rss/tin-tuc.rss",cat:"TT"},
  {name:"NGAN_HANG_VN BDS",url:"https://nganhangvietnam.vn/rss/bat-dong-san.rss",cat:"B\u0110S"},
  {name:"NGAN_HANG_VN KD",url:"https://nganhangvietnam.vn/rss/kinh-te.rss",cat:"KD"},
  {name:"DOI_SONG_VN BDS",url:"https://doisongvietnam.vn/rss/bat-dong-san.rss",cat:"B\u0110S"},
  {name:"DOI_SONG_VN KD",url:"https://doisongvietnam.vn/rss/kinh-doanh.rss",cat:"KD"},
  {name:"DOANH_NGHIEP_VN BDS_TT",url:"https://doanhnghiepvn.vn/rss/thi-truong-bat-dong-san-1047.rss",cat:"B\u0110S"},
  {name:"DOANH_NGHIEP_VN BDS_PL",url:"https://doanhnghiepvn.vn/rss/phap-ly-bat-dong-san-1049.rss",cat:"B\u0110S"},
  {name:"DOANH_NGHIEP_VN BDS_CS",url:"https://doanhnghiepvn.vn/rss/bat-dong-san-va-cuoc-song-1050.rss",cat:"B\u0110S"},
  {name:"DOANH_NGHIEP_VN BDS_DN",url:"https://doanhnghiepvn.vn/rss/doanh-nghiep-bat-dong-san-1051.rss",cat:"B\u0110S"},
  {name:"DOANH_NGHIEP_VN KD",url:"https://doanhnghiepvn.vn/rss/kinh-doanh-va-tieu-dung-1052.rss",cat:"KD"},
  {name:"SUC_KHOE_DS KT",url:"https://suckhoedoisong.vn/rss/kinh-te.rss",cat:"KD"},
  {name:"SUC_KHOE_DS BDS",url:"https://suckhoedoisong.vn/rss/bat-dong-san.rss",cat:"B\u0110S"},
  {name:"SUC_KHOE_DS TC",url:"https://suckhoedoisong.vn/rss/tai-chinh.rss",cat:"TC"},
  {name:"VIETNAM_BIZ BDS",url:"https://vietnambiz.vn/rss/bat-dong-san.rss",cat:"B\u0110S"},
  {name:"VTV TG",url:"https://vtv.vn/rss/the-gioi.rss",cat:"TG"},
  {name:"TINMOI BDS",url:"https://tinmoi.vn/rss/bat-dong-san.rss",cat:"B\u0110S"},
  {name:"TINMOI TC",url:"https://tinmoi.vn/rss/tai-chinh.rss",cat:"TC"},
  {name:"AN_NINH_TIEN_TE BDS",url:"https://antt.vn/rss/bat-dong-san.rss",cat:"B\u0110S"},
  {name:"AN_NINH_TIEN_TE KD",url:"https://antt.vn/rss/kinh-te-dau-tu.rss",cat:"KD"},
  {name:"VTC News TT",url:"https://vtcnews.vn/rss/thoi-su.rss",cat:"TT"},
  {name:"VTC News TC",url:"https://vtcnews.vn/rss/tai-chinh.rss",cat:"TC"},
  {name:"VnEconomy TT",url:"https://vneconomy.vn/thi-truong.rss",cat:"TT"},
  {name:"VnEconomy KD2",url:"https://vneconomy.vn/kinh-doanh.rss",cat:"KD"}
];

var API_SOURCES = [
  {type:"cafef",name:"CafeF B\u0110S",cat:"B\u0110S",zone_id:18835,domain:"https://cafef.vn"},
  {type:"cafef",name:"CafeF CK",cat:"CK",zone_id:18831,domain:"https://cafef.vn"},
  {type:"cafef",name:"CafeF DN",cat:"DN",zone_id:18836,domain:"https://cafef.vn"},
  {type:"cafef",name:"CafeF TC",cat:"TC",zone_id:18834,domain:"https://cafef.vn"},
  {type:"cafef",name:"CafeF V\u0129 m\u00f4",cat:"\u0110T",zone_id:18833,domain:"https://cafef.vn"},
  {type:"cafef",name:"CafeF Th\u1ecb tr\u01b0\u1eddng",cat:"TT",zone_id:18839,domain:"https://cafef.vn"},
  {type:"cafef",name:"CafeF B\u0110S - Th\u1ecb tr\u01b0\u1eddng",cat:"B\u0110S",zone_id:18843,domain:"https://cafef.vn"},
  {type:"cafef",name:"CafeF B\u0110S - N\u1ed9i th\u1ea5t PT",cat:"B\u0110S",zone_id:18846,domain:"https://cafef.vn"},
  {type:"cafef",name:"CafeF B\u0110S - Du l\u1ecbch",cat:"B\u0110S",zone_id:188120,domain:"https://cafef.vn"},
  {type:"cafebiz",name:"CafeBiz B\u0110S",cat:"B\u0110S",zone_id:176127,domain:"https://cafebiz.vn"},
  {type:"cafebiz",name:"CafeBiz CK",cat:"CK",zone_id:176132,domain:"https://cafebiz.vn"},
  {type:"cafebiz",name:"CafeBiz TC",cat:"TC",zone_id:176117,domain:"https://cafebiz.vn"},
  {type:"cafebiz",name:"CafeBiz S\u1ea3n xu\u1ea5t",cat:"SX",zone_id:176144,domain:"https://cafebiz.vn"},
  {type:"cafebiz",name:"CafeBiz Startup",cat:"KD",zone_id:176120,domain:"https://cafebiz.vn"},
  {type:"vietnamnet",name:"VietnamNet KD",cat:"KD",category_id:"000003",domain:"https://vietnamnet.vn"},
  {type:"vietnamnet",name:"VietnamNet TC",cat:"TC",category_id:"00000G",domain:"https://vietnamnet.vn"},
  {type:"vietnamnet",name:"VietnamNet \u0110\u1ea7u t\u01b0",cat:"\u0110T",category_id:"00000H",domain:"https://vietnamnet.vn"},
  {type:"vietnamnet",name:"VietnamNet Th\u1ecb tr\u01b0\u1eddng",cat:"TT",category_id:"00000J",domain:"https://vietnamnet.vn"},
  {type:"vietnamnet",name:"VietnamNet CK",cat:"CK",category_id:"00002N",domain:"https://vietnamnet.vn"},
  {type:"vietnamnet",name:"VietnamNet B\u0110S",cat:"B\u0110S",category_id:"00000E",domain:"https://vietnamnet.vn"},
  {type:"vietnamnet",name:"VietnamNet D\u1ef1 \u00e1n",cat:"B\u0110S",category_id:"00001C",domain:"https://vietnamnet.vn"},
  {type:"vietnamnet",name:"VietnamNet Th\u1ecb tr\u01b0\u1eddng B\u0110S",cat:"B\u0110S",category_id:"00004V",domain:"https://vietnamnet.vn"}
];

var SEARCH_TERMS = {
  VHM: ["VHM c\u1ed5 phi\u1ebfu","VHM ch\u1ee9ng kho\u00e1n","VHM Vinhomes"],
  VIC: ["VIC c\u1ed5 phi\u1ebfu","VIC ch\u1ee9ng kho\u00e1n","VIC Vingroup"],
  VRE: ["VRE c\u1ed5 phi\u1ebfu","VRE ch\u1ee9ng kho\u00e1n","VRE Vincom"],
  NVL: ["NVL c\u1ed5 phi\u1ebfu","NVL ch\u1ee9ng kho\u00e1n","NVL Novaland"],
  PDR: ["PDR c\u1ed5 phi\u1ebfu","PDR ch\u1ee9ng kho\u00e1n","PDR Ph\u00e1t \u0110\u1ea1t"],
  DXG: ["DXG c\u1ed5 phi\u1ebfu","DXG ch\u1ee9ng kho\u00e1n","DXG \u0110\u1ea5t Xanh"],
  KDH: ["KDH c\u1ed5 phi\u1ebfu","KDH ch\u1ee9ng kho\u00e1n","KDH Khang \u0110i\u1ec1n"],
  NLG: ["NLG c\u1ed5 phi\u1ebfu","NLG ch\u1ee9ng kho\u00e1n","NLG Nam Long"],
  CEO: ["CEO c\u1ed5 phi\u1ebfu","CEO ch\u1ee9ng kho\u00e1n","CEO Group"],
  DIG: ["DIG c\u1ed5 phi\u1ebfu","DIG ch\u1ee9ng kho\u00e1n","DIG DIC Corp"],
  KBC: ["KBC c\u1ed5 phi\u1ebfu","KBC ch\u1ee9ng kho\u00e1n","KBC Kinh B\u1eafc"],
  BCM: ["BCM c\u1ed5 phi\u1ebfu","BCM ch\u1ee9ng kho\u00e1n","BCM Becamex"],
  SZC: ["SZC c\u1ed5 phi\u1ebfu","SZC ch\u1ee9ng kho\u00e1n","SZC Sonadezi"],
  VCG: ["VCG c\u1ed5 phi\u1ebfu","VCG ch\u1ee9ng kho\u00e1n","VCG Vinaconex"],
  CTD: ["CTD c\u1ed5 phi\u1ebfu","CTD ch\u1ee9ng kho\u00e1n","CTD Coteccons"],
  HHV: ["HHV c\u1ed5 phi\u1ebfu","HHV ch\u1ee9ng kho\u00e1n","HHV \u0110\u00e8o C\u1ea3"],
  CII: ["CII c\u1ed5 phi\u1ebfu","CII ch\u1ee9ng kho\u00e1n","CII h\u1ea1 t\u1ea7ng"]
};

var INDUSTRY_SEARCH = [
  "b\u1ea5t \u0111\u1ed9ng s\u1ea3n tr\u00e1i phi\u1ebfu doanh nghi\u1ec7p",
  "khu c\u00f4ng nghi\u1ec7p \u0111\u1ea7u t\u01b0 h\u1ea1 t\u1ea7ng",
  "\u0111\u1ea7u t\u01b0 c\u00f4ng gi\u1ea3i ng\u00e2n cao t\u1ed1c",
  "c\u1ed5 phi\u1ebfu b\u1ea5t \u0111\u1ed9ng s\u1ea3n h\u00f4m nay",
  "d\u1ef1 \u00e1n nh\u00e0 \u1edf ph\u00e1p l\u00fd",
  "KCN khu ch\u1ebf xu\u1ea5t",
  "tr\u00e1i phi\u1ebfu b\u1ea5t \u0111\u1ed9ng s\u1ea3n ph\u00e1t h\u00e0nh"
];

var CONFIG_KEYWORDS_DATA = [];
(function buildKwData() {
  var kwid = 0;
  for (var code in SEARCH_TERMS) {
    var terms = SEARCH_TERMS[code];
    for (var i = 0; i < terms.length; i++) {
      kwid++;
      CONFIG_KEYWORDS_DATA.push({
        keyword_id: "KW" + ("000" + kwid).slice(-3),
        keyword: terms[i],
        industry_group: "B\u1ea5t \u0111\u1ed9ng s\u1ea3n",
        related_tickers: code,
        event_type_suggestion: "stock_mention, company_news",
        priority: "High",
        note: "M\u00e3 c\u1ed5 phi\u1ebfu " + code
      });
    }
  }
  for (var j = 0; j < INDUSTRY_SEARCH.length; j++) {
    kwid++;
    CONFIG_KEYWORDS_DATA.push({
      keyword_id: "KW" + ("000" + kwid).slice(-3),
      keyword: INDUSTRY_SEARCH[j],
      industry_group: "B\u1ea5t \u0111\u1ed9ng s\u1ea3n / H\u1ea1 t\u1ea7ng",
      related_tickers: STOCK_CODES.join(", "),
      event_type_suggestion: "industry_analysis, policy_update",
      priority: "Medium",
      note: "T\u00ecm ki\u1ebfm theo ng\u00e0nh"
    });
  }
})();

var SPREADSHEET_ID = "1XI1yWODMICqPupNruMCzZK2uAhLzE_HvYrNfogOD7pk";

function getSS() {
  return SpreadsheetApp.openById(SPREADSHEET_ID);
}

var HTTP_HEADERS = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
};

var REQUEST_TIMEOUT = 30;
var MAX_RETRIES = 2;

var BLOCKED_DOMAINS = [
  "wikipedia.org","hhs.gov","grokipedia","wikidata.org",
  "wikimedia.org","windy.com","pinterest","nordinvasion.com",
  "youtube.com","facebook.com"
];

var VIETNAMESE_CHARS_REGEX = new RegExp(
  "[\u0103\u00e2\u0111\u00ea\u00f4\u01a1\u01b0\u00e0\u1ea3\u00e3\u00e1\u1ea1\u0103\u1eb1\u1eb3\u1eb5\u1eaf\u1eb7\u00e2\u1ea7\u1ea9\u1eab\u1ea5\u1ead\u0111\u00e8\u1ebb\u1ebd\u00e9\u1eb9\u00ea\u1ec1\u1ec3\u1ec5\u1ebf\u1ec7\u00ec\u1ec9\u0129\u00ed\u1ecb\u00f2\u1ecf\u00f5\u00f3\u1ecd\u00f4\u1ed3\u1ed5\u1ed7\u1ed1\u1ed9\u01a1\u1edd\u1edf\u1ee1\u1edb\u1ee3\u00f9\u1ee7\u0169\u00fa\u1ee5\u01b0\u1eeb\u1eed\u1eef\u1ef1\u1ef3\u1ef7\u00fd\u1ef5]",
  "i"
);

var COMPANY_NAME_PATTERNS = {};
(function buildNamePatterns() {
  for (var code in COMPANY_KEYWORDS) {
    var escaped = COMPANY_KEYWORDS[code].map(function(kw) {
      return kw.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
    });
    COMPANY_NAME_PATTERNS[code] = new RegExp("(" + escaped.join("|") + ")", "i");
  }
})();
