import React from 'react';
import './App.css';
import styled from 'styled-components';
import EntityCard from './components/EntityCard';  // The correct import statement
import Me from './images/IMG_0019.JPG'
import Game from './components/Game'
import * as THREE from 'three';
import { Canvas, useFrame } from '@react-three/fiber';
import { Plane } from '@react-three/drei';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import LandingPage from './LandingPage'


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
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage/>}/>
          <Route path="/game" element={<Game/>}/>
        </Routes>
      </Router>


    </div>

  );
}

export default App;
