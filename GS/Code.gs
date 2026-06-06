var _stats = null;

function remainingTime() {
  try {
    return ScriptApp.getRemainingTime();
  } catch (e) {
    return 1800;
  }
}

function daily() {
  logInfo("=== DAILY CRAWL STARTED ===");
  var startTime = new Date();
  var ss = initWorkbook();
  var existingLinks = getExistingLinks(ss);

  _stats = { found: 0, added: 0, matchedNewsraw: 0, oldSkipped: 0, dupByHash: 0, failed: 0, sourcesUpdated: 0 };

  var today = new Date();
  var todayStr = today.toISOString().slice(0, 10);
  var yesterdayStr = new Date(today.getTime() - 86400000).toISOString().slice(0, 10);

  logInfo("--- B1: Crawl RSS (" + RSS_SOURCES.length + " feeds) ---");
  for (var i = 0; i < RSS_SOURCES.length; i++) {
    crawlRssSource(RSS_SOURCES[i], existingLinks, yesterdayStr, todayStr);
    if (remainingTime() < 60) break;
  }

  logInfo("--- B1: Crawl API page 1 (" + API_SOURCES.length + " zones) ---");
  for (var j = 0; j < API_SOURCES.length; j++) {
    crawlApiPage1(API_SOURCES[j], existingLinks, yesterdayStr, todayStr);
    if (remainingTime() < 60) break;
  }

  logInfo("--- B5: Flush ra sheets ---");
  var nIdx = flushAccumulator(ss);
  var nRaw = flushRawAccumulator(ss);
  logInfo("SOURCE_INDEX +" + nIdx + ", NEWS_RAW +" + nRaw);

  var totalRecords = 0;
  var ws = ss.getSheetByName(SOURCE_INDEX_NAME);
  if (ws) totalRecords = ws.getLastRow() - 1;

  logInfo("--- B6: Ghi CRAWL_LOG ---");
  appendCrawlLog(ss, {
    log_date: todayStr,
    member: "GAS_Daily",
    source: "All (" + RSS_SOURCES.length + " RSS + " + API_SOURCES.length + " API)",
    keyword_group: "B\u1ea5t \u0111\u1ed9ng s\u1ea3n, X\u00e2y d\u1ef1ng, KCN",
    date_range_from: todayStr,
    date_range_to: todayStr,
    records_found: _stats.found,
    records_added: _stats.added,
    duplicates: _stats.found - _stats.added + _stats.dupByHash,
    failed: _stats.failed,
    status: "done",
    note: "matched=" + _stats.matchedNewsraw + ", old_skipped=" + _stats.oldSkipped
  });

  logInfo("--- B7: C\u1eadp nh\u1eadt DAILY_SUMMARY ---");
  updateDailySummary(ss, {
    date: todayStr,
    total_records: totalRecords,
    new_records_today: _stats.matchedNewsraw,
    sources_updated: _stats.sourcesUpdated,
    date_coverage_from: yesterdayStr,
    date_coverage_to: todayStr,
    missing_days: "",
    duplicate_count: _stats.found - _stats.added + _stats.dupByHash,
    issue_status: _stats.failed > 0 ? "WARN: " + _stats.failed + " failed" : "OK",
    next_action: "Daily " + todayStr
  });

  flushLog();
  var elapsed = (new Date() - startTime) / 1000;
  logInfo("=== DAILY DONE: found=" + _stats.found + " added=" + _stats.added +
    " old_skipped=" + _stats.oldSkipped + " matched_newsraw=" + _stats.matchedNewsraw +
    " (" + elapsed.toFixed(0) + "s) ===");
}

function isRecentDate(pubDate, yesterdayStr, todayStr) {
  if (!pubDate) return true;
  var d = pubDate.slice(0, 10);
  return d === todayStr || d === yesterdayStr;
}

function processNewEntry(entry, existingLinks, yesterdayStr, todayStr) {
  var link = (entry.link || "").trim();
  if (!link) return;
  if (existingLinks[link]) return;

  existingLinks[link] = true;
  _stats.found++;

  var pubDate = normalizeDate(entry.datetime_public || "");
  if (!isRecentDate(pubDate, yesterdayStr, todayStr)) {
    _stats.oldSkipped++;
    return;
  }

  _stats.added++;

  accumulateEntry(entry);

  var title = entry.title || "";
  var kw = findMatchingKeyword(title);
  if (kw) {
    accumulateRawEntry({
      title: title,
      summary: entry.summary || "",
      content: "",
      published_date: pubDate,
      source: entry.source || "",
      url: link,
      industry_group: kw.industry_group,
      tickers: kw.related_tickers,
      keywords: kw.keyword,
      event_type: kw.event_type_suggestion,
      crawl_status: "keyword_matched"
    });
    _stats.matchedNewsraw++;
  } else {
    var mentions = detectMentionsInText(title);
    var filtered = filterFalsePositives(mentions, title, link);
    var tickers = [];
    for (var code in filtered) {
      if (filtered[code]) tickers.push(code);
    }
    if (tickers.length > 0) {
      accumulateRawEntry({
        title: title,
        summary: entry.summary || "",
        content: "",
        published_date: pubDate,
        source: entry.source || "",
        url: link,
        industry_group: "",
        tickers: tickers.join(", "),
        keywords: "",
        event_type: "stock_mention, company_news",
        crawl_status: "stock_detected"
      });
      _stats.matchedNewsraw++;
    }
  }
}

function crawlRssSource(rssEntry, existingLinks, yesterdayStr, todayStr) {
  try {
    var xmlText = fetchUrl(rssEntry.url);
    if (!xmlText) return;
    var entries = parseRssArticles(xmlText, rssEntry.name, rssEntry.cat || "");
    for (var i = 0; i < entries.length; i++) {
      processNewEntry(entries[i], existingLinks, yesterdayStr, todayStr);
    }
    _stats.sourcesUpdated++;
  } catch (e) {
    logWarn("RSS error [" + rssEntry.name + "]: " + e.message);
    _stats.failed++;
  }
}

function crawlApiPage1(src, existingLinks, yesterdayStr, todayStr) {
  try {
    var t = src.type;
    var data, entries;
    if (t === "cafef" || t === "cafebiz") {
      var url = apiBuildUrl(src, 1);
      if (!url) return;
      var html = fetchUrl(url);
      if (!html) return;
      if (t === "cafef") entries = extractCafefArticles(html, src.domain, src.name, src.cat || "");
      else entries = extractCafebizArticles(html, src.domain, src.name, src.cat || "");
    } else if (t === "vietnamnet") {
      data = apiFetch(src, 0);
      if (!data) return;
      entries = extractVietnamnetArticles(data, src.name, src.cat || "");
    } else return;
    for (var i = 0; i < entries.length; i++) {
      processNewEntry(entries[i], existingLinks, yesterdayStr, todayStr);
    }
    _stats.sourcesUpdated++;
  } catch (e) {
    logWarn("API error [" + src.name + "]: " + e.message);
    _stats.failed++;
  }
}

function crawlLinks() {
  logInfo("=== FULL CRAWL LINKS STARTED ===");
  var ss = initWorkbook();
  var existingLinks = getExistingLinks(ss);
  var totalAdded = 0;
  var stateKey = "CRAWL_LINKS_STATE";
  var props = PropertiesService.getScriptProperties();
  var stateStr = props.getProperty(stateKey);
  var state = stateStr ? JSON.parse(stateStr) : null;

  var allSources = RSS_SOURCES.concat(API_SOURCES.map(function(a) {
    return { name: a.name, url: apiBuildUrl(a, 1), cat: a.cat, isApi: true, apiSource: a };
  }));
  RSS_SOURCES.forEach(function(r) {
    r.isApi = false;
  });

  var idx = state ? state.idx : 0;
  var recurse = state ? state.recurse : false;
  var apiIdx = state ? state.apiIdx : 0;

  logInfo("Resuming from source index " + idx + ", api index " + apiIdx);

  for (var i = idx; i < RSS_SOURCES.length; i++) {
    indexRssSource(RSS_SOURCES[i], existingLinks, ss);
    props.setProperty(stateKey, JSON.stringify({ idx: i + 1, apiIdx: apiIdx, recurse: false }));
    if (remainingTime() < 60) {
      logInfo("Pausing RSS at index " + (i + 1) + " - time running low");
      flushAccumulator(ss);
      logInfo("Resume trigger scheduled");
      return;
    }
  }

  for (var j = apiIdx; j < API_SOURCES.length; j++) {
    indexApiSource(API_SOURCES[j], existingLinks, ss, true);
    props.setProperty(stateKey, JSON.stringify({ idx: RSS_SOURCES.length, apiIdx: j + 1, recurse: true }));
    if (remainingTime() < 60) {
      logInfo("Pausing API at index " + (j + 1) + " - time running low");
      flushAccumulator(ss);
      return;
    }
  }

  flushAccumulator(ss);
  props.deleteProperty(stateKey);

  logInfo("=== FULL CRAWL LINKS DONE: " + totalAdded + " total ===");
}

function crawlContent() {
  logInfo("=== CRAWL CONTENT STARTED ===");
  var ss = initWorkbook();
  var enriched = enrichFromIndex(ss, 500);
  logInfo("=== CRAWL CONTENT DONE: " + enriched + " enriched ===");
}

function testDiagnostic() {
  var LOG = function(level, msg) {
    var ts = new Date().toISOString().slice(0, 19).replace("T", " ");
    var row = [ts, level, msg];
    try {
      var sh = getSS().getSheetByName("_LOG");
      if (!sh) {
        sh = getSS().insertSheet("_LOG");
        sh.appendRow(["Timestamp", "Level", "Message"]);
      }
      sh.appendRow(row);
    } catch (e) {
      console.log("[DIAG] " + level + " " + msg + " (write error: " + e.message + ")");
    }
  };

  try {
    LOG("INFO", "=== DIAGNOSTIC START ===");
    var ss = getSS();
    LOG("INFO", "SS OK: " + ss.getName() + " sheets=" + ss.getSheets().length);

    LOG("INFO", "Fetch RSS: https://cafef.vn/bat-dong-san.rss");
    var xmlText = fetchUrl("https://cafef.vn/bat-dong-san.rss");
    LOG("INFO", "fetchUrl returned: " + (xmlText ? xmlText.length + " chars" : "NULL"));
    if (xmlText && xmlText.length > 50) {
      try {
        var doc = XmlService.parse(xmlText);
        var root = doc.getRootElement();
        var channel = root.getChild("channel") || root;
        var items = channel.getChildren("item");
        LOG("INFO", "Parsed OK: " + items.length + " items");
        if (items.length > 0) {
          var title = getChildText(items[0], "title");
          var pubDate = getChildText(items[0], "pubDate");
          LOG("INFO", "Item 0: " + (title || "").slice(0, 60));
          LOG("INFO", "  date=" + (pubDate || "N/A") + " recent=" + isRecentDate(pubDate || ""));
        }
      } catch (e) {
        LOG("ERROR", "Xml parse: " + e.message);
        LOG("INFO", "First 200: " + xmlText.slice(0, 200));
      }
    } else {
      LOG("INFO", "Raw response: " + (xmlText || "").slice(0, 200));
    }

    LOG("INFO", "Fetch API: cafef zoneId=18835");
    var apiText = fetchUrl("https://cafef.vn/ajax/timelinelist.chn?zoneId=18835&page=1&pageSize=15");
    LOG("INFO", "API cafef: " + (apiText ? apiText.length + " chars" : "NULL"));
    if (apiText) LOG("INFO", "  first 150: " + apiText.slice(0, 150));
  } catch (e) {
    LOG("ERROR", "UNCAUGHT: " + e.message);
  }
  LOG("INFO", "=== DIAGNOSTIC END ===");
}

function testSimple() {
  var msg = "OK: " + getSS().getName() + " sheets=" + getSS().getSheets().length;
  SpreadsheetApp.getUi().alert(msg);
}

function setupTriggers() {
  var triggers = ScriptApp.getProjectTriggers();
  var hasDaily = false;
  for (var i = 0; i < triggers.length; i++) {
    if (triggers[i].getHandlerFunction() === "daily") hasDaily = true;
  }
  if (!hasDaily) {
    ScriptApp.newTrigger("daily").timeBased().everyDays(1).atHour(8).create();
    ScriptApp.newTrigger("daily").timeBased().everyDays(1).atHour(20).create();
    logInfo("Daily triggers created (08:00 and 20:00)");
  } else {
    logInfo("Daily triggers already exist");
  }
}
