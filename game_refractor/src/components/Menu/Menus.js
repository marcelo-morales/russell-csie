import React, { Component } from "react";

import Menu_Question from "./Menu_Question.js"
import Menu_Answer from "./Menu_Answer.js"

import Ask_Question from "./Ask_Question.js"



class Menus extends Component {

  constructor(props) {
    super(props);
    this.state = {
      questionChoice: "name",
      answerChoice: 0
    };
  }

  makeAnswerMenu = function(chosenQuestion) {
    var menuValues = [];
    for (var character of this.props.characters) {
      var value = character[chosenQuestion];
      var index = menuValues.indexOf(value);
      if (index < 0) menuValues.push(value);
    }
    menuValues.sort();
    return menuValues;
  }

  getAnswer = () => {
    var menu = this.makeAnswerMenu(this.state.questionChoice);
    return menu[this.state.answerChoice];
  }

  setQuestionChoice = (chosenItem) => {
    // The top-level menu has been changed. The children must be reset.
    // This change will cause the menus to be redrawn
    this.setState({
      questionChoice: chosenItem,
      answerChoice: 0
    });
  }

  setAnswerChoice = (index, character) => {
    // Have a new list of filtered characters
    // This change will cause the menus to be redrawn
    this.setState({answerChoice: index})
  }

  askQuestion = () => {
    console.log("Queston:", this.state.questionChoice, "Answer:", this.getAnswer());
    this.props.handleChange(this.state.questionChoice, this.getAnswer());
  }

  render() {
    console.log(this.props.listening);
    return(
      <div className="menus">
        <h2>Click to ask:</h2>
        <Ask_Question
          handleClick={this.askQuestion}>
        </Ask_Question>
        {this.props.listening && <p>Listening now...</p>}
      </div>
    )
  }
}

export default Menus;