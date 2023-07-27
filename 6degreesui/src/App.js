import React from 'react';
import './App.css';
import styled from 'styled-components';
import EntityCard from './components/EntityCard';  // The correct import statement
import Me from './images/IMG_0019.JPG'
import Game from './components/Game'
import * as THREE from 'three';
import { Canvas, useFrame } from '@react-three/fiber';
import { Plane } from '@react-three/drei';
import {BoxGeometry} from 'three'
function Box() {
  

  return (
    <group>
      <Plane args={[5, 5]} />
      <mesh
        geometry={new THREE.BoxGeometry(4, 4, 4)}
        material={new THREE.MeshBasicMaterial({ color: 'ed' })}
      ></mesh>
    </group>
  );
}

const AppContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
`;


function App() {
  return (
  
    <div className="App" style={{color: 'black'}}>
      <Game category="cinema">
      </Game>
      <Canvas>
        <Box>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
        </Box>
      </Canvas>
    </div>

  );
}

export default App;
