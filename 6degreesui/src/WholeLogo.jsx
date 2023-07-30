import React from 'react'
import Logo from './Logo.jsx'
import styled, {keyframes} from 'styled-components'

const Container = styled.div`
  width: ${props => props.width};
  height: ${props => props.height};
  display: flex;

  
  &:hover {
    opacity: .45;
}

`;
const TitleContainer = styled.div`
    text-align: center;
    font-family: 'IBM Plex Serif', serif;  // Make sure you've imported Orbitron font in your project
    font-weight: bold;
    
; // Adjust according to your preference
    color: #FFF;  // Change color as needed
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);  // This will give the text a shadow, adjust as needed
    z-index: 10;  // This ensures the title stays on top of the backdrop    
    font-size: ${props => props.fontSize}vw;
`;


const StyledLogo = styled.div`
    margin-left:-10%;
    margin-top:-12.7%;
  // You can adjust this to position your logo vertically  // This will center the logo horizontally  // This ensures the center of the logo is at the position specified by top and left
    z-index: 3;  // This ensures the logo stays on top of the backdrop
    filter:brightness(110%);

`;
function WholeLogo({width,height}) {
    const numericalWidth = parseFloat(width);
    const fontSize = numericalWidth / 6.6;

    return (
        <div>
            <Container>
            <TitleContainer fontSize={fontSize}>6degrees</TitleContainer>
            <StyledLogo><Logo size={height}></Logo></StyledLogo>
            </Container>
        </div>
    )
}

export default WholeLogo;