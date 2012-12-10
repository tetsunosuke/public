/**
 * background.js
 * 拡張が起動している間に実行されているファイルです
 * Chrome側からの指示を待ち、指定されたイベント発生時に起動します
 */
 
//// Context menu のサンプル ////
/**
 * yahoo検索する Context Menu
 * 右クリックのコンテキストメニューにYahoo検索のためのメニューを表示
 * 選択された文字列を使ってURLを生成し、新しいタブで開きます
 */
chrome.contextMenus.create({
    "title": "拡張機能を実行します[Yahoo検索]",
    "contexts": ["selection"],                             
    "onclick": function(onClickData, tab) { 
        // コンテキストメニュー表示時に選択していた文字列
        word = encodeURIComponent(onClickData.selectionText);
        chrome.tabs.create({
            "url" : "http://search.yahoo.co.jp/search?p=" + word
        });
    }
});


////  omnibox のサンプル ////
////  Ctrl+L +  ggrks + " " でコマンド候補が出る
/**
 * 入力があったときに表示されるsuggest文字列と実際のコマンドの対応
 */ 
chrome.omnibox.onInputChanged.addListener(
  function(text, suggest) {
    suggest([
      {content: "is:unread",            description: "未読"},
      {content: "has:red-bang",         description: "！（重要）"},
      {content: "has:yellow-star",      description: "★通常"},
      {content: "has:red-star",         description: "★重要"},
      {content: "has:blue-star",        description: "★期限あり"},
    ]);
  }
);

/**
 * 実行されたコマンドをそのままGmail検索に投げる
 * URLを生成し新しいタブで開きます
 */
chrome.omnibox.onInputEntered.addListener(
  function(text) {
    chrome.tabs.create({
      "url" : "https://mail.google.com/mail/u/0/?shva=1#search/" + encodeURIComponent(text)
    });
  }
);