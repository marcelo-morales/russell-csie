import './App.css';
import characters from './characters';
import Container from './components/Container'

function App() {
  return (
    <>
      <Container characters={characters}></Container>
    </>
  );
}

export default App;
