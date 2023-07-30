import React from 'react';
import styled from 'styled-components';
import GameEntity from './GameEntity';

const ArenaContainer = styled.div`
  width: 100vw;
  height: 100vh;
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #ff; // Adjust background color as needed
`;

const LeftEntityContainer = styled.div`
  position: absolute;
  left: 5%;
  top: 50%;
  z-score:5;
`;

const RightEntityContainer = styled.div`
  position: absolute;
  right: 5%;
  top: 50%;

  z-score:5;
`;

function GameEngine() {
  return (
    <ArenaContainer>
      <LeftEntityContainer>
        <GameEntity width="16vw" height="18vh" initials="LE" position="left" />
      </LeftEntityContainer>

      <RightEntityContainer>
        <GameEntity width="16vw" height="18vh" initials="RE" position="right" />
      </RightEntityContainer>
    </ArenaContainer>
  );
}

export default GameEngine;
