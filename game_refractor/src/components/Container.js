import React, { Component } from "react";

import Menus from "./Menu/Menus.js";
import Card from "./Card/Card.js"
import Notification from "./Notification"

import logo from "../assets/logo.png"

import axios from "axios";
import getAudio from "../services/api";

const myComponentStyle = {
  paddingTop: '200px',
}

class Container extends Component {

   sayInstructions = () => {
    this.speak("Hello, welcome to russell !");
  }

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
      synth: window.speechSynthesis,
      messageToDisplay: "Click on button to ask a question",
      listening: false
    }

    this.sayInstructions();
  }

   formatSpeakingOutput =  (adjective, trait) => {
    let returnList = []

    console.log('this is adj ' + adjective)
    console.log('this is trait ' + trait)

    if (trait === "hair_color") {
      if (adjective === "blond") {
        returnList.push("blonde")
        returnList.push("hair")
        return returnList;
      }

      returnList.push(adjective)
      returnList.push("hair")
      return returnList;
    }


    else if (trait === "wearing_a_hat") {
      if (adjective === "true" ) {
        returnList.push("a")
        returnList.push("hat")
      }
     
    }

    else if (trait === "hat_color") {
      returnList.push("a " + adjective)
      returnList.push("hat")
    }

    else if (trait === "glasses") {
        returnList.push("glasses")
        returnList.push("")
    }

    else if (trait === "bald") {
      returnList.push("glasses")
      returnList.push("")
    } 

    return returnList;

}

noResponse =  (adjective, entity) => {
  let choices = [];

  if (entity === "bald") {
    choices[0] = "No my person is  not bald";
    choices[1] = "Nope, my character I’m thinking of is  not bald try another guess";
    choices[2] = "Nice try, but my person is not bald guess again";

    return choices[Math.floor(Math.random() * 3)];
  }
  
  if (entity === "glasses") {
    adjective = "";
  }

  if (entity === "hair_color") {
    entity = "hair";
  }

  if (entity === "hat_color") {
    adjective = "a " + adjective;
    entity = "hat";
  }

  if (entity === "wearing_a_hat") {
    adjective = "a ";
    entity = "hat";
  }

  choices[0] = "No my person does not have " + adjective +  entity;
  choices[1] = "Nope, my character I’m thinking of does not have "  + adjective +  entity +  " try another guess";
  choices[2] = "Nice try, but my person does not have " + adjective + entity + " guess again";

  return choices[Math.floor(Math.random() * 3)];
}

yesresponses  =  (adjective, entity) => {
  let choices = [];

  if (entity === "bald") {
    choices[0] = "Good guess! My person is bald";
    choices[1] = "That’s right, my person is bald";
    return choices[Math.floor(Math.random() * 3)];
  }


  if (entity === "glasses") {
    adjective = "";
  }

  if (entity === "hair_color") {
    entity = "hair";
  }

  if (entity === "hat_color") {
    adjective = "a " + adjective;
    entity = "hat";
  }

  if (entity === "wearing_a_hat") {
    adjective = "a ";
    entity = "hat";
  }


  choices[0] = "Good guess! My person does have " + adjective +  entity;
  choices[1] = "That’s right, my person has "  + adjective +  entity;
  return choices[Math.floor(Math.random() * 2)];
}

congratsResponses  =  (name) => {
  let choices = [];
  choices[0] = "Great job, my person is " + name;
  choices[1] = "Wow you’re good at this! The character I was thinking of is "  + name;
  choices[2] = name + " is the chosen one. Congrats!";
  console.log('saying congrats here');
  return choices[Math.floor(Math.random() * 3)];
}


  questionSelected = async (question, answer) => {

    let response = "";
    this.setState({messageToDisplay: "Listening now!!"})
    try {
      response = await axios.get("http://127.0.0.1:5000/");
    } catch {
      this.speak("I'm sorry can you repeat that? I was not able to catch what you were saying");
      this.setState({messageToDisplay: "I did not undestand you, try asking again!"});
      return;
    }
    const data = response.data;    

    question = data["trait"];
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
    var count = 0;
    hidden.forEach(function(flag) {
      if (!flag) count++;
    })

    if (count === 1) {
      this.setState({messageToDisplay: "Congrats, you got the character!"});
      let message;
      console.log('repeating here');

      setTimeout(100);

      message = this.congratsResponses(this.state.unknownCharacter.name);
      this.speak(message);
    } else {
      this.setState({messageToDisplay: "I heard you, click on button to ask another question"});
      if (answerIsYes) {
        let resultArray = this.formatSpeakingOutput(data["adjective"], data["trait"]);
        if (data["trait"] === "bald") {
          this.speak("Yes, my person is bald");
        } else {
          if (resultArray && resultArray.length > 0) {
            console.log('this is result ' + data["adjective"] + " " + data["trait"]);
            console.log('getting expression ' + this.yesresponses(data["adjective"], data["trait"]));
          this.speak(this.yesresponses(data["adjective"], data["trait"]));
          }
          else {
            this.speak("I'm sorry can you repeat that? I was not able to catch what you were saying");
          }
        }
      }
      else if (answerIsNo) {
        let resultArray = this.formatSpeakingOutput(data["adjective"], data["trait"]);
        if (data["trait"] === "bald") {
          this.speak("No, my person is not bald");
        } else {
          if (resultArray && resultArray.length > 0) {
            console.log('this is result ' + data["adjective"] + " " +  data["trait"]);
            console.log('getting expression ' + this.noResponse(data["adjective"], data["trait"]));
            this.speak(this.noResponse(data["adjective"], data["trait"]));
          }
          else {
            this.speak("I'm sorry can you repeat that? I was not able to catch what you were saying");
          }
        }
      }
    }


    // These changes will force the re-render.
    this.setState( {
      hiddenCharacters: hidden,
      answerIsYes: answerIsYes
    } )

    console.log('only appear once');
  }

  gameOver = () => {
    var count = 0;
    this.state.hiddenCharacters.forEach(function(flag) {
      if (!flag) count++;
    })
    console.log('only appear once');
    return (count === 1);
  }

  speak = async (message) => {
    const response = await getAudio(message);
    const audio = new Audio("data:audio/wav;base64," + response);
    audio.play();
  }


  render() {
 
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
            handleChange={this.questionSelected}
            listening={this.state.listening}>
          </Menus>
          {this.state.hiddenCharacters ? ( 
          <Notification style={myComponentStyle}>{this.state.messageToDisplay}</Notification>
          ) : (<Notification>{this.state.messageToDisplay}</Notification>)}
        </div>
        {cards}
      </div>
    )
  }
}

export default Container;