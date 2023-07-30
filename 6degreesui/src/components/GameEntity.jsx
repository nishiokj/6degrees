import {useState,React, useRef,useEffect} from 'react';
import styled from 'styled-components';
import img from '../images/node.png';
import normalPlusIcon from '../images/unselectedPlus.png';
import pressedPlusIcon from '../images/selectedPlus.png';

const EntityContainer = styled.div`
  position: relative;
  width: ${props => props.width};
  height: ${props => props.height};
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  background: url(${img}) no-repeat center center;
  background-size: cover;
`;

const Initials = styled.div`
  font-weight: bold;
  color: #FFF; // Change color as needed
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); // Adjust as needed
  z-index: 1;
  font-size:4vw;
`;

const DetailsContainer = styled.div`
  position: absolute;
  width: 200px; 
  height: 300px;
  background-color: white;
  border: 1px solid #ddd;
  z-index:2;
  display: ${props => (props.navOpen ? 'block' : 'none')};
`;
const PlusIcon = styled.img`
  width: 5vw; // Adjust size as needed

  cursor: pointer;
  position: absolute;
  top: 22.4%; // Adjust position as needed
  left: ${props => (props.position === 'right' ? '-10px' : 'auto')};
  right: ${props => (props.position === 'left' ? '-10px' : 'auto')};
  transition: all 0.2s;

  &:hover {
    opacity: 0.7; // Add a hover effect if desired
  }

  &:active {
    transform: scale(0.95); // Add a press effect if desired
  }
`;
const SearchBar = styled.input`
  width: 90%;
  padding: 10px;
  border: 1px solid #ddd;
`;

const ScrollBar = styled.div`
  overflow-y: scroll;
  height: 70%;
`;

function GameEntity({ initials,width,height,position }) {
    const [isOpen, setIsOpen] = useState(true);
  const [isPressed, setIsPressed] = useState(false);
  const [navOpen,setNavOpen] = useState(false);
  const detailsRef = useRef(null);
  const handlePlusClick = (event) => {
    event.stopPropagation();
    setNavOpen(true);
 
  }
  const handleConnection = () =>{
    setIsOpen(false);
  }
  const handleClickOutside = (event) => {
    if (detailsRef.current && !detailsRef.current.contains(event.target)) {
      setNavOpen(false);
    }
  
  };

  useEffect(() => {
    if (navOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    } else {
      document.removeEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [navOpen]);
  return (
    <EntityContainer height={height} width={width}>
      <Initials>{initials}</Initials>
      {isOpen && (
        <PlusIcon
          position={position}
          src={isPressed ?  pressedPlusIcon:normalPlusIcon}
          onClick={handlePlusClick}
        />
      )}
      <DetailsContainer ref={detailsRef}navOpen={navOpen}>
        <SearchBar type="text" placeholder="Search" />
        <ScrollBar>
          {/* Content for the scrollable area */}
        </ScrollBar>
      </DetailsContainer>
    </EntityContainer>
  );
}

export default GameEntity;
