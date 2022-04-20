var React = require('react');
var ReactDOM = require('react-dom');
var Container = require('./components/container.jsx');
var characters = require("./characters")

window.onload = function(){
  //console.log('hello');
  this.state.synth.speak(new SpeechSynthesisUtterance("Welcome to Russell! I’m thinking of one of the characters below, can you guess who it is? To start guessing, click the question mark button and ask me a question about a physical trait about one of the characters. For example, you could ask “Does your person have blond hair”"));
  ReactDOM.render(
    <Container characters={characters}></Container>,
    document.getElementById('app')
  );
}
