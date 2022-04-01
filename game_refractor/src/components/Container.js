import React, { Component } from "react";

import Menus from "./Menu/Menus.js";
import Card from "./Card/Card.js"
import Notification from "./Notification"

import logo from "../assets/logo.png"

import axios from "axios";

class Container extends Component {

  constructor(props) {
    super(props);
    var hidden = []
    for (var i = 0; i < this.props.characters.length; i++) {
      hidden.push(false);
    }
    var randomNo = Math.floor(Math.random() * 8);

    this.state = {
      unknownCharacter: this.props.characters[randomNo],
      hiddenCharacters: hidden,
      synth: window.speechSynthesis
    }
  }

  questionSelected = async (question, answer) => {

    const response = await axios.get("http://127.0.0.1:5000/");
    const data = response.data;

    question = "hairColour";
    answer = data["adjective"];

    console.log(question);
    console.log(answer);

    // If the answer is YES remove all those that do not share the attribute
    // If the answer is NO remove all those that share the attribute
    var hidden = [];
    var characters = this.props.characters;
    var answerIsYes = (this.state.unknownCharacter[question] === answer);
    var answerIsNo = !answerIsYes
    for (var i = 0; i < characters.length; i++) {
      hidden[i] = ((answerIsNo && (characters[i][question] === answer)) ||
                  (answerIsYes && (characters[i][question] !== answer)) ||
                  this.state.hiddenCharacters[i]);
    }
    if (answerIsYes) {
      this.state.synth.speak(new SpeechSynthesisUtterance("Yes, my person has that"));
    }
    else if (answerIsNo) {
      this.state.synth.speak(new SpeechSynthesisUtterance("No, my person does not have that"));
    }
    // These changes will force the re-render.
    this.setState( {
      hiddenCharacters: hidden,
      answerIsYes: answerIsYes
    } )
  }

  gameOver = () => {
    var count = 0;
    this.state.hiddenCharacters.forEach(function(flag) {
      if (!flag) count++;
    })
    return (count === 1);
  }

  render() {
    var message = "";
    if (this.state.answerIsYes !== undefined) {
      if (this.gameOver()) {
        message = this.state.unknownCharacter.name + " is the chosen one.";
        this.state.synth.speak(new SpeechSynthesisUtterance(message));
      }
      else {
        message = "The answer is ";
        message += (this.state.answerIsYes) ? "'Yes'." : "'No'." ;
        this.state.synth.speak(new SpeechSynthesisUtterance(message));
      }
    }

    var cards = this.props.characters.map(function(character, index){
      return <Card
                key={index}
                character={character}
                hide={this.state.hiddenCharacters[index]}>
              </Card>
    }.bind(this))

    return (
      <div className="container">
        <div className="menu-container">
          <img src={logo} />
          <Menus
            characters={this.props.characters}
            handleChange={this.questionSelected}>
          </Menus>
          <Notification>{message}</Notification>
        </div>
        {cards}
      </div>
    )
  }
}

export default Container;