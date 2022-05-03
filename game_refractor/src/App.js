import './App.css';
import characters from './characters';
import Container from './components/Container'
import dog_avatar from '../src/assets/russell-dog.png';


// function sayInstructions() {
//   window.speechSynthesis.speak("Hello welcome to russell");
// }

function App() {

  //sayInstructions();


  return (


    <body>
      <div className="image-container">
      <p >&nbsp;&nbsp; My name is Russell!<br></br>
      <br></br>
      &nbsp;&nbsp; I'm thinking of a person,<br></br>
      &nbsp;&nbsp; try to guess who it is!</p>
        <img src={dog_avatar} alt="Logo" />
        <p>Click the <span style={{color:"red"}}>?</span> button each time to ask about:<br></br>
         Hair color, baldness, hats, hat color, glasses<br></br>
         <br></br>
         Example question: "Is your person wearing a hat?"
         </p>
      </div>
      <Container characters={characters}></Container>
    </body>
  );
}

export default App;