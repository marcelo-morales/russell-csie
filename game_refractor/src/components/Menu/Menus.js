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
    var answerMenu = this.makeAnswerMenu(this.state.questionChoice);
    return(
      <div className="menus">
        <Menu_Question
          menuIndex={this.state.questionChoice}
          handleChange={this.setQuestionChoice}>
        </Menu_Question>
        <Menu_Answer
          menuIndex={this.state.answerChoice}
          answerMenu={answerMenu}
          handleChange={this.setAnswerChoice}>
        </Menu_Answer>
        <Ask_Question
          handleClick={this.askQuestion}>
        </Ask_Question>
      </div>
    )
  }
}

export default Menus;