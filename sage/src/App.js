/* global chrome */

import React, { Component } from "react";
import icon from "./imgs/actIco.png";
import "./App.css";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      title: "",
      description: "",
      link: ""
    };
  }

  componentDidMount() {
    let getInfo = function() {
      return new Promise(function(resolve, reject) {
        chrome.tabs.query({ active: true, currentWindow: true }, function(
          tabs
        ) {
          chrome.tabs.sendMessage(tabs[0].id, { from: "reactapp" }, function(
            response
          ) {
            var data = {
              title: response.title,
              description: response.description,
              link: response.link
            };
            resolve(data);
          });
        });
      });
    };
    getInfo().then(data => {
      return this.setState({
        title: data.title,
        description: data.description,
        link: data.link
      });
    });
  }

  render() {
    return (
      <div className="modalBody">
        <div className="row">
          <div className="left">
            <img className="icon" src={icon} />
          </div>
          <div className="right">
            <p className="titleText">
              Act Now:{" "}
              <a className="titleLink" href={this.state.link} target="_blank">
                {this.state.title}
              </a>
            </p>
            <p className="genText">{this.state.description}</p>
          </div>
        </div>
      </div>
    );
  }
}
export default App;
