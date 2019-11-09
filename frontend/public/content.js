var title;
var description;
var link;
chrome.runtime.sendMessage({ from: "content" });
chrome.runtime.onMessage.addListener(function(msg, sender, sendResponse) {
  if (msg.from == "background" && msg.event == "true") {
    title = msg.title;
    description = msg.description;
    link = msg.link;
    const eventDiv = document.createElement("div");
    eventDiv.id = "myDivIdAct";
    eventDiv.style.position = "fixed";
    eventDiv.style.margin = "0px";
    eventDiv.style.padding = "0px";
    eventDiv.style.bottom = "-15vh";
    eventDiv.style.left = "0px";
    eventDiv.style.transition = "bottom 1.2s";
    eventDiv.style.zIndex = "2147483647";
    eventDiv.style.width = "100%";
    eventDiv.style.height = "16vh";
    eventDiv.style.opacity = "0.9";
    eventDiv.style.backgroundColor = "#FF8686";
    eventDiv.innerHTML = `<iframe id="actNow"style="height:100%; width:100%"></iframe><link href="https://fonts.googleapis.com/css?family=Roboto:300&display=swap" rel="stylesheet"/>
            <div-z style="position:absolute; top:6vh; right:18px; ">  
                <h6-z id="unique" style="cursor:pointer; transition: color 0.3s; font-family: 'Roboto', sans-serif; font-size: 30px; padding:0px; margin:0px; color:#ffffff;" onmouseout="this.style.color='#ffffff'" onmouseover="this.style.color='#ff6464'">x</h6-z>
            </div-z>`;
    document.body.appendChild(eventDiv);
    const iframe = document.getElementById("actNow");
    iframe.src = chrome.extension.getURL("index.html");
    iframe.frameBorder = 0;

    eventDiv.querySelector("h6-z").addEventListener("click", () => {
      eventDiv.remove();
    });
  } else if (msg.from == "reactapp") {
    sendResponse({
      from: "content",
      title: title,
      description: description,
      link: link
    });
    document.getElementById("myDivIdAct").style.bottom = "0px";
  } else {
    console.log("Act Now App: Nothing Found");
  }
});
