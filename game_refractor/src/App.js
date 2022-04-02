import './App.css';
import characters from './characters';
import Container from './components/Container'
import dog_avatar from '../src/assets/russell-dog.png';

function App() {
  return (
    <body>
      <div className="image-container">
        <img src={dog_avatar} alt="Logo" />
      </div>
      <Container characters={characters}></Container>
    </body>
  );
}

export default App;
