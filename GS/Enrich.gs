function detectMentionsInText(text) {
  var upper = (text || "").toUpperCase();
  var stockHits = {};
  var match;
  var re = new RegExp("\\b(" + STOCK_CODES.join("|") + ")\\b", "g");
  while ((match = re.exec(upper)) !== null) {
    stockHits[match[1]] = true;
  }
  var result = {};
  for (var i = 0; i < STOCK_CODES.length; i++) {
    var code = STOCK_CODES[i];
    if (stockHits[code]) {
      result[code] = 1;
    } else if (COMPANY_NAME_PATTERNS[code] && COMPANY_NAME_PATTERNS[code].test(upper)) {
      result[code] = 1;
    } else {
      result[code] = 0;
    }
  }
  return result;
}

function filterFalsePositives(mentions, text, link) {
  var linked = (link || "").toLowerCase();
  for (var d = 0; d < BLOCKED_DOMAINS.length; d++) {
    if (linked.indexOf(BLOCKED_DOMAINS[d]) >= 0) {
      var zeroed = {};
      for (var c in mentions) {
        zeroed[c] = 0;
      }
      return zeroed;
    }
  }
  var upper = (text || "").toUpperCase();
  var hasVi = VIETNAMESE_CHARS_REGEX.test(upper);
  var result = {};
  for (var j = 0; j < STOCK_CODES.length; j++) {
    var code = STOCK_CODES[j];
    result[code] = mentions[code] || 0;
    if (result[code] === 1) {
      var nameMatched = COMPANY_NAME_PATTERNS[code] && COMPANY_NAME_PATTERNS[code].test(upper);
      if (!nameMatched && !hasVi) {
        result[code] = 0;
      }
    }
  }
  return result;
}

function findMatchingKeyword(title) {
  if (!title) return null;
  var lower = title.toLowerCase();
  for (var i = 0; i < CONFIG_KEYWORDS_DATA.length; i++) {
    var kw = CONFIG_KEYWORDS_DATA[i];
    if (lower.indexOf(kw.keyword.toLowerCase()) >= 0) {
      return kw;
    }
  }
  return null;
}

function enrichFromIndex(ss, limit) {
  limit = limit || 500;
  var existingHashes = getExistingHashes(ss);
  var rows = getSourceIndexRows(ss);
  var candidates = [];
  for (var i = 0; i < rows.length; i++) {
    if (rows[i].Status === "new") candidates.push(rows[i]);
  }
  var titleMatched = [];
  for (var j = 0; j < candidates.length; j++) {
    var r = candidates[j];
    var title = r.Title || "";
    var link = r.Link || "";
    var mentions = detectMentionsInText(title);
    var filtered = filterFalsePositives(mentions, title, link);
    var hasMatch = false;
    for (var c in filtered) {
      if (filtered[c]) { hasMatch = true; break; }
    }
    if (hasMatch) titleMatched.push(r);
  }
  var enriched = 0;
  var toProcess = titleMatched.slice(0, limit);
  for (var k = 0; k < toProcess.length; k++) {
    var entry = toProcess[k];
    var link = entry.Link;
    var fullContent = fetchArticleContent(link);
    if (fullContent && fullContent.length >= 500) {
      var text = (entry.Title || "") + " " + fullContent;
      var mentions2 = detectMentionsInText(text);
      var filtered2 = filterFalsePositives(mentions2, text, link);
      var tickers = [];
      for (var c2 in filtered2) {
        if (filtered2[c2]) tickers.push(c2);
      }
      updateEntryStatus(ss, link, "mentioned");
      accumulateRawEntry({
        title: entry.Title || "",
        summary: fullContent.slice(0, 300),
        content: fullContent,
        published_date: entry["Datetime Public"] || "",
        source: entry.Source || "",
        url: link,
        industry_group: "",
        tickers: tickers.join(", "),
        keywords: "",
        event_type: "",
        crawl_status: "success"
      });
      enriched++;
    } else {
      updateEntryStatus(ss, link, fullContent ? "short_content" : "failed");
      accumulateRawEntry({
        title: entry.Title || "",
        summary: "",
        content: fullContent || "",
        published_date: entry["Datetime Public"] || "",
        source: entry.Source || "",
        url: link,
        industry_group: "",
        tickers: "",
        keywords: "",
        event_type: "",
        crawl_status: fullContent ? "short_content" : "failed",
        error_message: fullContent ? "Content too short" : "Fetch failed"
      });
    }
    if ((k + 1) % 50 === 0) {
      flushRawAccumulator(ss);
    }
    if (ScriptApp.getRemainingTime() < 30) break;
  }
  flushRawAccumulator(ss);
  logInfo("Enrichment: " + enriched + " enriched from " + toProcess.length + " candidates");
  return enriched;
}
