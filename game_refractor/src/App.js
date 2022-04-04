import './App.css';
import characters from './characters';
import Container from './components/Container'
import dog_avatar from '../src/assets/russell-dog.png';

function App() {
  return (
    <body>
      <div className="image-container">
        <p><h1>Hi, my name is Russell!<br></br></h1>
        <h1>Try asking questions about:<br></br></h1>
        <h2> Hair color, baldness, hats, glasses</h2></p>
        <img src={dog_avatar} alt="Logo" />
      </div>
      <Container characters={characters}></Container>
    </body>
  );
}

export default App;
