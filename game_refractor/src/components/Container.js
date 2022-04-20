import React, { Component } from "react";

import Menus from "./Menu/Menus.js";
import Card from "./Card/Card.js"
import Notification from "./Notification"

import logo from "../assets/logo.png"

import axios from "axios";
//import fs from 'fs';

// Imports the Google Cloud client library
const textToSpeech = require('@google-cloud/text-to-speech');


// Creates a client
const client = new textToSpeech.TextToSpeechClient();

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

    const response = await axios.get("http://127.0.0.1:5000/");
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
    if (answerIsYes) {
      //this.state.synth.speak(new SpeechSynthesisUtterance("Yes, my person has " + data["adjective"] + data["trait"]));
      let resultArray = this.formatSpeakingOutput(data["adjective"], data["trait"]);
      if (data["trait"] === "bald") {
        this.state.synth.speak(new SpeechSynthesisUtterance("Yes, my person is bald"));
      } else {
        if (resultArray && resultArray.length > 0) {
          console.log('this is result ' + data["adjective"] + " " + data["trait"]);
          console.log('getting expression ' + this.yesresponses(data["adjective"], data["trait"]));


         this.state.synth.speak(new SpeechSynthesisUtterance(this.yesresponses(data["adjective"], data["trait"])));

         const requestYes = {
          input: {text: this.yesresponses(data["adjective"], data["trait"])},
          // Select the language and SSML voice gender (optional)
          voice: {languageCode: 'en-US', ssmlGender: 'NEUTRAL'},
          // select the type of audio encoding
          audioConfig: {audioEncoding: 'MP3'},
        };

        const [response] = await client.synthesizeSpeech(requestYes);

        //this.state.synth.speak(new SpeechSynthesisUtterance("Yes, my person has " +   resultArray[0] + resultArray[1]));
        }
        else {


          this.state.synth.speak(new SpeechSynthesisUtterance("I'm sorry can you repeat that? I was not able to catch what you were saying"));
        }
      }
      //this.state.synth.speak(new SpeechSynthesisUtterance("Yes, my person has that"));
    }
    else if (answerIsNo) {

      //this.state.synth.speak(new SpeechSynthesisUtterance("No, my person does not have " +   data["adjective"] + data["trait"]));
      let resultArray = this.formatSpeakingOutput(data["adjective"], data["trait"]);
      if (data["trait"] === "bald") {
        this.state.synth.speak(new SpeechSynthesisUtterance("No, my person is not bald"));
      } else {
        if (resultArray && resultArray.length > 0) {
          //this.state.synth.speak(new SpeechSynthesisUtterance("No, my person does not have " +   resultArray[0] + resultArray[1]));
          console.log('this is result ' + data["adjective"] + " " +  data["trait"]);
          console.log('getting expression ' + this.noResponse(data["adjective"], data["trait"]));
          this.state.synth.speak(new SpeechSynthesisUtterance(this.noResponse(data["adjective"], data["trait"])));
        }
        else {
          this.state.synth.speak(new SpeechSynthesisUtterance("I'm sorry can you repeat that? I was not able to catch what you were saying"));
        }
      }
      // this.state.synth.speak(new SpeechSynthesisUtterance("No, my person does not have " +   resultArray[0] + resultArray[1]));
      // console.log('this is what i am saying ' + 'No, my person does not have ' +   resultArray[0] + ' ' +  resultArray[1]);
    }


    // These changes will force the re-render.
    this.setState( {
      hiddenCharacters: hidden,
      answerIsYes: answerIsYes
    } )

    var count = 0;
    this.state.hiddenCharacters.forEach(function(flag) {
      if (!flag) count++;
    })
    console.log('only appear once');
    if (count === 1) {
      var message;
      console.log('repeating here');
      message = this.congratsResponses(this.state.unknownCharacter.name);
      this.finalSpeak(message);
    }
    else {
      message = "The answer is ";
      message += (this.state.answerIsYes) ? "'Yes'." : "'No'." ;
    }

  }

  gameOver = () => {
    var count = 0;
    this.state.hiddenCharacters.forEach(function(flag) {
      if (!flag) count++;
    })
    console.log('only appear once');
    return (count === 1);
  }

  finalSpeak = (message) => {
    this.state.synth.speak(new SpeechSynthesisUtterance(message));
    return;
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
            handleChange={this.questionSelected}>
          </Menus>
          {/* <Notification>{message}</Notification> */}
        </div>
        {cards}
      </div>
    )
  }
}

export default Container;