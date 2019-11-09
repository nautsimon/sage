var contentTabId;
// add geolocation

// add organization logos to the banner
var eventResp = {
  isEvent: "false",
  title: "false",
  description: "false",
  link: "false"
};
let getUrl = function() {
  return new Promise((resolve, reject) => {
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
      var domain = tabs[0].url;
      resolve(domain);
    });
  });
};
let getApi = function(pageUrl) {
  return new Promise(function(resolve, reject) {
    var percentage = "94%";
    var link1 = "https://pornhub.com";
    var link2 = "https://twitter.com";
    var link3 = "https://google.com";
    eventResp = {
      isEvent: "true",
      percentage: percentage,
      link1: link1,
      link2: link2,
      link3: link3
    };
  });
  // var pageUrl = pageUrl;
  // var xhr = new XMLHttpRequest(),
  //   method = "POST",
  //   url = "http://actnow-chrome.herokuapp.com/getevent/";
  // return new Promise(function(resolve, reject) {
  //   xhr.onreadystatechange = function() {
  //     if (xhr.readyState === 4 && xhr.status === 200) {
  //       response = JSON.parse(xhr.responseText);
  //       if (response != "none") {
  //         eventResp = {
  //           isEvent: "true",
  //           title: response.name,
  //           description: response.description,
  //           link: response.link
  //         };
  //         resolve(eventResp);
  //       } else {
  //         eventResp = {
  //           isEvent: "false",
  //           title: "false",
  //           description: "false",
  //           link: "false"
  //         };
  //         console.log("Act Now: nothing found");
  //         resolve(eventResp);
  //       }
  //     }
  //   };
  //   xhr.open(method, url);
  //   xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  //   xhr.send(
  //     JSON.stringify({
  //       url: pageUrl
  //     })
  //   );
  // });
};
let sendMessage = function(msg, sender, result) {
  var response = eventResp;
  return new Promise((resolve, reject) => {
    chrome.tabs.sendMessage(contentTabId, {
      percentage: response.percentage,
      event: response.isEvent,
      link1: response.link1,
      link2: response.link2,
      link3: response.link3
    });
    resolve("message sent");
  });
};
chrome.runtime.onMessage.addListener(function(msg, sender) {
  if (msg.from == "content" || msg.from == "reactapp") {
    contentTabId = sender.tab.id;
    getUrl()
      .then(result => {
        return getApi(result);
      })
      .then(() => {
        return sendMessage(msg, sender);
      })
      .then(result => {
        console.log(result);
      });
  }
});
