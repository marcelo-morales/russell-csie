import './App.css';
import characters from './characters';
import Container from './components/Container'
import dog_avatar from '../src/assets/russell-dog.png';

function App() {
  return (
    <body>
      <div className="image-container">
      <p >&nbsp;&nbsp; My name is Russell!<br></br>
      &nbsp;&nbsp; I'm thinking of a character,<br></br>
      &nbsp;&nbsp; try to guess it!</p>
        <img src={dog_avatar} alt="Logo" />
        <p>Click the <span style={{color:"red"}}>?</span> button to ask a question about:<br></br>
         Hair color, baldness, hats, hat color, glasses</p>
      </div>
      <Container characters={characters}></Container>
    </body>
  );
}

export default App;
