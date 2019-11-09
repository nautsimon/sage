/* global chrome */

import React, { Component } from "react";
import icon from "./imgs/actIco.png";
import "./App.css";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      percentage: "",
      link1: "",
      link2: "",
      link3: ""
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
              percentage: response.percentage,
              link1: response.link1,
              link2: response.link2,
              link3: response.link3
            };
            resolve(data);
          });
        });
      });
    };
    getInfo().then(data => {
      return this.setState({
        percentage: data.percentage,
        link1: data.link1,
        link2: data.link2,
        link3: data.link3
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
              {/* <a className="titleLink" href={this.state.link} target="_blank">
                {this.state.title}
              </a> */}
            </p>
            <p className="genText">{this.state.percentage}</p>
            <p className="genText">{this.state.link1}</p>
            <p className="genText">{this.state.link2}</p>
            <p className="genText">{this.state.link3}</p>
          </div>
        </div>
      </div>
    );
  }
}
export default App;
