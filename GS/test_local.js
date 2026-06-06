/**
 * test_local.js — Local GAS test harness for Node.js
 * 
 * HOW TO USE:
 *   npm install       # install dependencies
 *   node test_local.js [--validate|--list-functions]
 * 
 * This provides mock GAS APIs so you can validate the .gs files
 * for syntax errors, missing references, and logical correctness
 * BEFORE pushing to Google Cloud.
 * 
 * DEPLOY (when ready):
 *   npm install -g @google/clasp
 *   clasp login
 *   clasp create --type sheets --title "K4 Crawl Test"
 *   clasp push
 *   clasp open
 *   clasp run daily
 */

// ─── Mock GAS Globals ───────────────────────────────────────────────────────

global.SpreadsheetApp = {
  _sheets: {},
  _active: null,
  getActiveSpreadsheet: function() {
    if (!global.SpreadsheetApp._active) {
      global.SpreadsheetApp._active = global.SpreadsheetApp._createMock();
    }
    return global.SpreadsheetApp._active;
  },
  _createMock: function() {
    return {
      _name: "MockSheet",
      _sheets: {},
      getSheetByName: function(name) {
        return this._sheets[name] || null;
      },
      insertSheet: function(name) {
        var sheet = {
          _name: name,
          _rows: [],
          _data: [],
          _headers: [],
          getLastRow: function() { return this._rows.length + 1; },
          getRange: function(row, col, numRows, numCols) {
            return {
              _sheet: this, _row: row, _col: col,
              _numRows: numRows || 1, _numCols: numCols || 1,
              getValues: function() {
                var result = [];
                for (var r = 0; r < (numRows || 1); r++) {
                  var rowArr = [];
                  for (var c = 0; c < (numCols || 1); c++) {
                    var idx = (row - 1 + r);
                    var val = this._sheet._rows[idx] ? this._sheet._rows[idx][col - 1 + c] : null;
                    rowArr.push(val);
                  }
                  result.push(rowArr);
                }
                return result;
              },
              setValues: function(values) {
                for (var r = 0; r < values.length; r++) {
                  var actualRow = row - 1 + r;
                  for (var c = 0; c < values[r].length; c++) {
                    var actualCol = col - 1 + c;
                    if (!this._sheet._rows[actualRow]) {
                      this._sheet._rows[actualRow] = [];
                    }
                    this._sheet._rows[actualRow][actualCol] = values[r][c];
                  }
                }
              },
              setValue: function(v) {
                if (!this._sheet._rows[row - 1]) this._sheet._rows[row - 1] = [];
                this._sheet._rows[row - 1][col - 1] = v;
              },
              setFontWeight: function() { return this; },
              setBackground: function() { return this; },
              setFontColor: function() { return this; }
            };
          },
          appendRow: function(arr) {
            this._rows.push(arr);
          }
        };
        this._sheets[name] = sheet;
        return sheet;
      }
    };
  },
  flush: function() { /* noop */ }
};

global.UrlFetchApp = {
  _responses: {},
  mockResponse: function(url, content, code) {
    code = code || 200;
    global.UrlFetchApp._responses[url] = { content: content || "", code: code };
  },
  fetch: function(url, params) {
    var resp = global.UrlFetchApp._responses[url];
    if (!resp) {
      console.log("  [MOCK] UrlFetchApp.fetch: NO MOCK for " + url);
      return {
        getResponseCode: function() { return 404; },
        getContentText: function() { return ""; }
      };
    }
    return {
      getResponseCode: function() { return resp.code; },
      getContentText: function() { return resp.content; }
    };
  },
  fetchAll: function(requests) {
    var self = this;
    return requests.map(function(req) {
      return self.fetch(req.url, req);
    });
  }
};

global.XmlService = {
  _namespaces: {},
  getNamespace: function(prefix) {
    return { _prefix: prefix };
  },
  parse: function(xmlText) {
    // Simple mock — returns a minimal structure
    var doc = { _root: null };
    try {
      // Basic XML parsing for test validation
      var channelMatch = xmlText.match(/<channel>([\s\S]*)<\/channel>/i);
      if (!channelMatch) throw new Error("No <channel> found");
      var items = [];
      var itemRegex = /<item>([\s\S]*?)<\/item>/gi;
      var m;
      while ((m = itemRegex.exec(channelMatch[1])) !== null) {
        var itemXml = m[1];
        var children = {};
        var titleM = itemXml.match(/<title[^>]*>([^<]*)<\/title>/i);
        if (titleM) children.title = titleM[1];
        var linkM = itemXml.match(/<link[^>]*>([^<]*)<\/link>/i);
        if (linkM) children.link = linkM[1];
        var descM = itemXml.match(/<description[^>]*>([^<]*)<\/description>/i);
        if (descM) children.description = descM[1];
        var pubM = itemXml.match(/<pubDate[^>]*>([^<]*)<\/pubDate>/i);
        if (pubM) children.pubDate = pubM[1];
        var item = {
          getChild: function(name) {
            var val = children[name];
            return val !== undefined ? { getText: function() { return val; } } : null;
          }
        };
        items.push(item);
      }
      var mockRoot = {
        getChild: function(name) {
          if (name === "channel") {
            return {
              getChildren: function(name) {
                if (name === "item") return items;
                return [];
              }
            };
          }
          return null;
        }
      };
    doc.getRootElement = function() { return mockRoot; };
    } catch (e) {
      doc._parseError = e.message;
    }
    return doc;
  }
};

global.Utilities = {
  DigestAlgorithm: { MD5: "MD5" },
  computeDigest: function(algo, str) {
    // Simple hash for testing
    var hash = 0;
    for (var i = 0; i < str.length; i++) {
      var c = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + c;
      hash = hash & hash;
    }
    // Return array of bytes (simulating GAS behavior)
    var bytes = [];
    for (var b = 0; b < 16; b++) {
      bytes.push((hash >> (b * 2)) & 0xFF);
    }
    return bytes;
  },
  sleep: function(ms) { /* noop for test */ }
};

global.ScriptApp = {
  getRemainingTime: function() { return 300; },
  getProjectTriggers: function() { return []; },
  newTrigger: function(name) {
    return {
      timeBased: function() {
        return {
          everyDays: function() { return { atHour: function() { return { create: function() {} }; } }; }
        };
      }
    };
  }
};

global.PropertiesService = {
  _store: {},
  getScriptProperties: function() {
    return {
      getProperty: function(key) { return global.PropertiesService._store[key] || null; },
      setProperty: function(key, val) { global.PropertiesService._store[key] = val; },
      deleteProperty: function(key) { delete global.PropertiesService._store[key]; }
    };
  }
};

// ─── Load .gs files ─────────────────────────────────────────────────────────

var fs = require("fs");
var path = require("path");
var vm = require("vm");
var gsDir = __dirname;

var gsFiles = [
  "Models.gs", "Config.gs", "Log.gs", "Fetch.gs",
  "Store.gs", "Extract.gs", "Enrich.gs", "Code.gs"
];

gsFiles.forEach(function(f) {
  var content = fs.readFileSync(path.join(gsDir, f), "utf8");
  try {
    vm.runInThisContext(content, { filename: f });
    console.log("  [OK] Loaded " + f);
  } catch (e) {
    console.log("  [FAIL] " + f + ": " + e.message);
  }
});

// ─── Test suite ─────────────────────────────────────────────────────────────

function runTests() {
  var passed = 0;
  var failed = 0;

  function assert(condition, msg) {
    if (condition) {
      passed++;
    } else {
      failed++;
      console.log("  [FAIL] " + msg);
    }
  }

  console.log("\n=== STRUCTURAL VALIDATION ===\n");

  // 1. Constants exist
  assert(typeof STOCK_CODES !== "undefined", "STOCK_CODES defined");
  assert(STOCK_CODES.length === 17, "STOCK_CODES has 17 codes");
  assert(typeof RSS_SOURCES !== "undefined", "RSS_SOURCES defined");
  assert(RSS_SOURCES.length === 96, "RSS_SOURCES has 96 feeds");
  assert(typeof API_SOURCES !== "undefined", "API_SOURCES defined");
  assert(API_SOURCES.length === 22, "API_SOURCES has 22 zones");

  // 2. Headers exist
  assert(typeof SOURCE_INDEX_HEADERS !== "undefined", "SOURCE_INDEX_HEADERS");
  assert(SOURCE_INDEX_HEADERS.length === 6, "SOURCE_INDEX_HEADERS has 6 cols");
  assert(typeof NEWS_RAW_HEADERS !== "undefined", "NEWS_RAW_HEADERS");
  assert(NEWS_RAW_HEADERS.length === 18, "NEWS_RAW_HEADERS has 18 cols");

  // 3. Functions exist
  assert(typeof fetchUrl === "function", "fetchUrl() defined");
  assert(typeof fetchMultiple === "function", "fetchMultiple() defined");
  assert(typeof stripHtmlTags === "function", "stripHtmlTags() defined");
  assert(typeof normalizeDate === "function", "normalizeDate() defined");
  assert(typeof md5Hash === "function", "md5Hash() defined");
  assert(typeof extractArticleBody === "function", "extractArticleBody() defined");
  assert(typeof parseRssArticles === "function", "parseRssArticles() defined");
  assert(typeof indexRssSource === "function", "indexRssSource() defined");
  assert(typeof extractCafefArticles === "function", "extractCafefArticles() defined");
  assert(typeof extractCafebizArticles === "function", "extractCafebizArticles() defined");
  assert(typeof extractVietnamnetArticles === "function", "extractVietnamnetArticles() defined");
  assert(typeof apiFetch === "function", "apiFetch() defined");
  assert(typeof detectMentionsInText === "function", "detectMentionsInText() defined");
  assert(typeof filterFalsePositives === "function", "filterFalsePositives() defined");
  assert(typeof enrichFromIndex === "function", "enrichFromIndex() defined");
  assert(typeof findMatchingKeyword === "function", "findMatchingKeyword() defined");
  assert(typeof isRecentDate === "function", "isRecentDate() defined");
  assert(typeof processNewEntry === "function", "processNewEntry() defined");
  assert(typeof crawlRssSource === "function", "crawlRssSource() defined");
  assert(typeof crawlApiPage1 === "function", "crawlApiPage1() defined");
  assert(typeof initWorkbook === "function", "initWorkbook() defined");
  assert(typeof getExistingLinks === "function", "getExistingLinks() defined");
  assert(typeof accumulateEntry === "function", "accumulateEntry() defined");
  assert(typeof flushAccumulator === "function", "flushAccumulator() defined");
  assert(typeof accumulateRawEntry === "function", "accumulateRawEntry() defined");
  assert(typeof flushRawAccumulator === "function", "flushRawAccumulator() defined");
  assert(typeof makeNewsId === "function", "makeNewsId() defined");
  assert(typeof appendCrawlLog === "function", "appendCrawlLog() defined");
  assert(typeof updateDailySummary === "function", "updateDailySummary() defined");
  assert(typeof daily === "function", "daily() defined");
  assert(typeof crawlLinks === "function", "crawlLinks() defined");
  assert(typeof crawlContent === "function", "crawlContent() defined");
  assert(typeof setupTriggers === "function", "setupTriggers() defined");
  assert(typeof logInfo === "function", "logInfo() defined");
  assert(typeof logFetch === "function", "logFetch() defined");

  // 4. COMPANY_NAME_PATTERNS built correctly
  assert(typeof COMPANY_NAME_PATTERNS !== "undefined", "COMPANY_NAME_PATTERNS defined");
  var vhmRe = COMPANY_NAME_PATTERNS["VHM"];
  assert(vhmRe instanceof RegExp, "COMPANY_NAME_PATTERNS.VHM is regex");
  assert(vhmRe.test("Vinhomes"), "VHM pattern matches 'Vinhomes'");

  // 5. detectMentionsInText works
  var mentions = detectMentionsInText("VHM t\u0103ng tr\u01b0\u1edfng m\u1ea1nh");
  assert(mentions["VHM"] === 1, "detectMentionsInText finds VHM");
  assert(mentions["VIC"] === 0, "detectMentionsInText no false positive");

  // 6. filterFalsePositives filters correctly
  var filtered = filterFalsePositives(mentions, "VHM t\u0103ng tr\u01b0\u1edfng", "https://cafef.vn/abc");
  assert(filtered["VHM"] === 1, "filterFalsePositives keeps VHM with Vietnamese text");

  // 7. stripHtmlTags works
  assert(stripHtmlTags("<p>Hello <b>World</b></p>") === "Hello World", "stripHtmlTags");
  assert(stripHtmlTags("") === "", "stripHtmlTags empty");

  // 8. md5Hash produces consistent length
  var h = md5Hash("test_url");
  assert(typeof h === "string" && h.length === 32, "md5Hash produces 32 char hex");

  // 9. RSS parsing with mock
  var testXml = '<?xml version="1.0"?><rss><channel><item><title>Test Article</title><link>https://test.vn/a</link><description>Desc</description><pubDate>Mon, 01 Jan 2024 00:00:00 GMT</pubDate></item></channel></rss>';
  var entries = parseRssArticles(testXml, "TestSource", "B\u0110S");
  assert(entries.length === 1, "parseRssArticles returns 1 entry");
  assert(entries[0].title === "Test Article", "parseRssArticles title correct");
  assert(entries[0].link === "https://test.vn/a", "parseRssArticles link correct");
  assert(entries[0].source === "RSS:TestSource", "parseRssArticles source prefix");

  // 10. CONFIG_KEYWORDS_DATA generated
  assert(CONFIG_KEYWORDS_DATA.length > 50, "CONFIG_KEYWORDS_DATA generated");
  var firstKw = CONFIG_KEYWORDS_DATA[0];
  assert(firstKw.keyword_id === "KW001", "First keyword is KW001");

  // 11. findMatchingKeyword works
  var kw = findMatchingKeyword("VHM c\u1ed5 phi\u1ebfu h\u00f4m nay");
  assert(kw !== null, "findMatchingKeyword finds 'VHM c\u1ed5 phi\u1ebfu'");
  assert(kw.related_tickers === "VHM", "findMatchingKeyword returns VHM ticker");

  var kw2 = findMatchingKeyword("b\u1ea5t \u0111\u1ed9ng s\u1ea3n tr\u00e1i phi\u1ebfu doanh nghi\u1ec7p");
  assert(kw2 !== null, "findMatchingKeyword finds industry keyword");

  var kw3 = findMatchingKeyword("th\u1eddi ti\u1ebft h\u00f4m nay \u0111\u1eb9p");
  assert(kw3 === null, "findMatchingKeyword returns null for unrelated");

  // 12. isRecentDate handles today/yesterday
  var today = new Date();
  var todayStr = today.toISOString().slice(0, 10);
  var yesterdayStr = new Date(today.getTime() - 86400000).toISOString().slice(0, 10);
  assert(isRecentDate(todayStr + " 10:00:00", yesterdayStr, todayStr) === true, "isRecentDate today");
  assert(isRecentDate(yesterdayStr + " 10:00:00", yesterdayStr, todayStr) === true, "isRecentDate yesterday");
  assert(isRecentDate("2020-01-01", yesterdayStr, todayStr) === false, "isRecentDate old date");
  assert(isRecentDate("", yesterdayStr, todayStr) === true, "isRecentDate empty date treated as recent");

  // 13. processNewEntry flow
  var mockExisting = {};
  var entry = {
    link: "https://test.vn/vhm-co-phieu",
    source: "RSS:Test",
    category: "CK",
    title: "VHM c\u1ed5 phi\u1ebfu t\u0103ng tr\u01b0\u1edfng",
    datetime_public: todayStr + " 10:00:00",
    status: "new"
  };
  _stats = { found: 0, added: 0, matchedNewsraw: 0, oldSkipped: 0, dupByHash: 0, failed: 0, sourcesUpdated: 0 };
  processNewEntry(entry, mockExisting, yesterdayStr, todayStr);
  assert(_stats.found === 1, "processNewEntry counts found");
  assert(_stats.added === 1, "processNewEntry counts added");
  assert(_stats.matchedNewsraw === 1, "processNewEntry matched keyword (VHM)");
  assert(mockExisting[entry.link] === true, "processNewEntry marks existing link");
  assert(entry.link in mockExisting, "processNewEntry link in existing set");

  // 14. processNewEntry skips dup
  _stats = { found: 0, added: 0, matchedNewsraw: 0, oldSkipped: 0, dupByHash: 0, failed: 0, sourcesUpdated: 0 };
  processNewEntry(entry, mockExisting, yesterdayStr, todayStr);
  assert(_stats.found === 0, "processNewEntry skips dup link");

  // 15. processNewEntry skips old articles
  var oldEntry = {
    link: "https://test.vn/old-article",
    source: "RSS:Test",
    category: "CK",
    title: "VHM c\u1ed5 phi\u1ebfu c\u0169",
    datetime_public: "2020-06-01 10:00:00",
    status: "new"
  };
  _stats = { found: 0, added: 0, matchedNewsraw: 0, oldSkipped: 0, dupByHash: 0, failed: 0, sourcesUpdated: 0 };
  processNewEntry(oldEntry, {}, yesterdayStr, todayStr);
  assert(_stats.found === 1, "processNewEntry counts old article as found");
  assert(_stats.added === 0, "processNewEntry skips old article (added=0)");
  assert(_stats.oldSkipped === 1, "processNewEntry counts oldSkpped");

  console.log("\n" + "=".repeat(40));
  console.log("RESULTS: " + passed + " passed, " + failed + " failed");
  console.log("=".repeat(40) + "\n");

  return failed === 0;
}

function listFunctions() {
  var gsFiles = ["Models.gs","Config.gs","Log.gs","Fetch.gs","Store.gs","Extract.gs","Enrich.gs","Code.gs"];
  console.log("GAS files and their exports:\n");
  gsFiles.forEach(function(f) {
    var content = fs.readFileSync(path.join(__dirname, f), "utf8");
    var funcs = content.match(/function\s+\w+/g) || [];
    var vars = content.match(/^(?:var|let|const)\s+(\w+)/gm) || [];
    console.log("  " + f + ":");
    funcs.forEach(function(fn) { console.log("    " + fn); });
    vars.forEach(function(v) { console.log("    " + v.split(" ")[1]); });
    console.log();
  });
}

// ─── Main ───────────────────────────────────────────────────────────────────

var args = process.argv.slice(2);
if (args.includes("--list-functions")) {
  listFunctions();
} else {
  var ok = runTests();
  process.exit(ok ? 0 : 1);
}
