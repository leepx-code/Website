/**
 * LeepX lead sheet. Paste this whole file into Extensions → Apps Script of your Google Sheet, then Deploy as a Web app.
 * It creates two tabs on its own:
 *   "Leads"    – one row for every person who finished the assessment and shared contact details.
 *   "Progress" – one row for every person who started, updated after each question, so you can see where people stop.
 * New columns are added automatically if the website starts sending new fields.
 */
function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var d = JSON.parse(e.postData.contents);
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    if (d.kind === 'progress') {
      upsert_(sheet_(ss, 'Progress'), 'Session ID', d.row);
    } else {
      append_(sheet_(ss, 'Leads'), d.row);
    }
    return ContentService.createTextOutput('ok');
  } catch (err) {
    return ContentService.createTextOutput('error: ' + err);
  } finally {
    lock.releaseLock();
  }
}

function doGet() {
  return ContentService.createTextOutput('LeepX lead sheet is connected.');
}

function sheet_(ss, name) {
  var sh = ss.getSheetByName(name);
  if (!sh) { sh = ss.insertSheet(name); sh.setFrozenRows(1); }
  return sh;
}

// Returns {columnName: columnNumber}, adding any missing columns to the header row.
function headers_(sh, keys) {
  var last = sh.getLastColumn();
  var head = last ? sh.getRange(1, 1, 1, last).getValues()[0] : [];
  var map = {};
  head.forEach(function (h, i) { if (h !== '') map[h] = i + 1; });
  keys.forEach(function (k) {
    if (!map[k]) {
      head.push(k);
      map[k] = head.length;
      sh.getRange(1, head.length).setValue(k).setFontWeight('bold');
    }
  });
  return map;
}

function rowValues_(map, row, existing) {
  var width = 0;
  Object.keys(map).forEach(function (k) { width = Math.max(width, map[k]); });
  var out = existing ? existing.slice() : [];
  while (out.length < width) out.push('');
  Object.keys(row).forEach(function (k) {
    var v = row[k];
    out[map[k] - 1] = (v === null || v === undefined) ? '' : String(v);
  });
  return out;
}

function append_(sh, row) {
  var map = headers_(sh, Object.keys(row));
  sh.appendRow(rowValues_(map, row));
}

function upsert_(sh, keyCol, row) {
  var map = headers_(sh, Object.keys(row));
  var key = String(row[keyCol]);
  var lastRow = sh.getLastRow();
  if (lastRow > 1) {
    var ids = sh.getRange(2, map[keyCol], lastRow - 1, 1).getValues();
    for (var i = 0; i < ids.length; i++) {
      if (String(ids[i][0]) === key) {
        var r = i + 2;
        var width = sh.getLastColumn();
        var existing = sh.getRange(r, 1, 1, width).getValues()[0];
        var vals = rowValues_(map, row, existing);
        sh.getRange(r, 1, 1, vals.length).setValues([vals]);
        return;
      }
    }
  }
  sh.appendRow(rowValues_(map, row));
}
