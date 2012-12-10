/**
 *Yahoo検索結果のGmailショートカット的な処理
 */
$(function() {
  links = [];     // 対象のリンク
  var index = 1;  // 選択中を表すリンク

  // 背景色設定
  setBackgroundColor = function(jqobj, color) {
    jqobj.css("background-color", color);
  };
  // 選択されているリンクは黄色
  setSelected = function(jqobj) {
    // 黄色
    setBackgroundColor(jqobj, "#FFA");
  };
  // 非選択のリンクはうすい青
  setNotSelected = function(jqobj) {
    // 青色
    setBackgroundColor(jqobj, "#DDF");
  };
  
  
  // 表示された時に背景色を設定、リンクを配列にして保持
  $(".hd").each(function(e) {
    setNotSelected($(this), "#");
    links.push($(this));
  });  
  // 先頭を選択状態へ
  setSelected($(links[0]));
  
  // jが押された時のショートカット
  // 次のリンクを選択状態に。自身のリンクを非選択に。
  // 次のリンクが無ければなにもしない
  shortcut.add("j", function() {
    if(index > 0) {
      setNotSelected($(links[index-1]));
    }  
    setSelected($(links[index]));
    if (links[index+1] !== undefined) {
      index++;
    }
  }, {"disable_in_input":true});
  
  
  // kが押された時のショートカット
  // 前のリンクを選択状態に。
  shortcut.add("k", function() {
    if(index > 1) {
      index--;
      setSelected($(links[index-1]));
    }  
    setNotSelected($(links[index]));
  }, {"disable_in_input":true});
  
  // oが押された時のショートカット
  // 選択状態のリンクを開く
  shortcut.add("o", function() {
    href = $(links[index]).find("a").attr("href");
    window.open(href);
  }, {"disable_in_input": true});
});