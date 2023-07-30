import React, { useState } from 'react';
import styled from 'styled-components';
import ReactCardFlip from 'react-card-flip';
import Me from '../images/headshot_jevin_thumbnail.png'
import StarIcon from '@mui/icons-material/Star';
import WholeLogo from '../WholeLogo.jsx'
const CardFront = styled.div`
  width: 12vw;  // This could be any percentage you find suitable.
  aspect-ratio: 6.4 / 8.9;  // This is the aspect ratio of the card.
  background-color: #ffsdd;
  position: relative;  // This allows absolute positioning inside the container.
  padding:6px;
  border: 3px solid #000;
  box-shadow: 0 10px 20px 0 rgba(0,0,0,0.2);
  transition: 0.3s;
  border-radius: 15px;
  background-image: linear-gradient(to top right, #669999, #003300);
  &:hover {
    box-shadow: 0 20px 30px 0 rgba(0,0,0,0.2);
  }
  &::after {
    content: '';
    position: absolute;
    top: .5%;
    left: .5%;
    right: .5%;
    bottom: .5%;
    border: 1px solid #fff;
    z-index: 1;
    border-radius:15px;
    overflow:hidden;
  }
`;
const CardBack = styled.div`
  width: 22vw;    // This could be any percentage you find suitable.
  aspect-ratio: 6.4 / 8.9;  // This is the aspect ratio of the card.
  background-color: #ffsdd;
  border: 2px solid #000;
  color: #000;
  display: flex;
  justify-content: center;
  font-size:1.1vw;
  align-items: center;
  position: relative;  // This allows absolute positioning inside the container.
  background-image: linear-gradient(to bottom right, #669999, #006600);
  box-shadow: 0 10px 20px 0 rgba(0,0,0,0.2);
  transition: 0.3s;
  overflow:hidden;
  border-radius:15px;
  
  &:hover {
    box-shadow: 0 20px 30px 0 rgba(0,0,0,0.2);
  }
  &::after {
    content: '';
    position: absolute;
    top: 1%;
    left: 1%;
    right: 1%;
    bottom: 1%;
    border: 2px solid #fff;
    z-index: 1;
    border-radius:15px;
    
    
  }
`;
const ImageContainer = styled.div`

  background-size: cover;
  transition: 0.3s;
  height:100%;
  border-radius:15px;
  overflow:hidden;
  height:100%;
  position:relative;
  

`;
const StyledLogo = styled.div`
    position: absolute;
    background-size: cover;
    top:-5%;
    left:-7%;  // You can adjust this to position your logo vertically  // This will center the logo horizontally  // This ensures the center of the logo is at the position specified by top and left
    z-index: 3;  // This ensures the logo stays on top of the backdrop
    transform-origin: 50% 50%;
    filter:brightness(90%);
    &:hover {
        opacity: .75;
    }
`;
const OverlayImage = styled.div`
  position: absolute;
  width: 100%;
  min-height: 100%;
  border-radius: 15px;
  top:0%;
  left:0%;
  background: url(${props => props.src}) no-repeat center center/cover;
  &::after {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background: rgba(102, 153, 153, 0.8); /* White with 30% opacity */
    border-radius: 10px;
    background: rgba(0, 0, 0, 0.5);
  }
`;

const InsideFrame = styled.div`

  background-image: url('');
  background-size: cover;
  box-shadow: 0 12px 15px rgba(0, 0, 0, 0.2)
  border: 2px solid #fff;
  box-shadow: 0 10px 20px 0 rgba(0,0,0,0.2);
  transition: 0.3s;
  overflow:hidden;
  &::after {
    content: '';
    position: absolute;
    top: 0%;
    left: 0%;
    right: 0%;
    bottom: 0%;
    border: 1px solid #fff;
    z-index: 1;
    border-radius:15px;
    overflow:hidden;
  }
  
`;

const StyledReactCardFlip = styled(ReactCardFlip)`
  width: 100%;
  height: 100%;
`;
const RatingContainer = styled.div`

`;
const Banner = styled.div`
  position:absolute;
  margin-top:18%;
  margin-right:10%;
  background-image: linear-gradient(to bottom right, #FF78, #669999); // Gradient for depth
  box-shadow: 0 1px 10px rgba(0, 0, 0, 0.2); // Deeper shadow for depth
  height:1vw;
  width:4.5vw;
  border-radius: 15px;
  z-index:3;
`;

const TypeContainer = styled.div`
  flex-basis: 42%;
  position:absolute;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  font-size: .8vw;
  right:5%;
  margin-top:10%;
  font-family: 'Courier New', Courier, monospace; // Use your preferred font
  font-weight:900;
  text-transform: uppercase; // Convert text to uppercase
  letter-spacing: 2px; // Increase spacing between letters
  text-shadow: 1px 2px 4px rgba(0,0,0,0.5); // Text shadow for 3D effect
  color:#fff;
  overflow:hidden;
`;
const NameContainer = styled.div`
  display: flex;
  flex-basis:55%;
  margin-right:25px;
  margin-top:10%;
  position:absolute;
  background: transparent;
  font-family: 'Courier New', Courier, monospace; // Use your preferred font
  font-size:.9vw; // Adjust based on your preference
  font-weight:600;
  text-transform: uppercase; // Convert text to uppercase
  text-shadow: 1px 2px 2px rgba(0,0,0,0.5); // Text shadow for 3D effect
  color:#fff;
  overflow:hidden;
  word-wrap:break-word;
`;
const SubContainer = styled.div`
  width: 100%;
  height:20%;
  display:flex;
  left:10%;
  border-radius: 5px;
`;

const TextContainer = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  font-weight:800;
  background-color: rgba(102, 153, 153, 0.5); /* You can adjust the color and opacity as needed */
  color: #ffffff;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 10px;
  padding: 10px;
  box-sizing: border-box;
  overflow: auto;
  text-shadow: 1px 2px 2px rgba(0,0,0,0.8);
`;
const ImgContainer = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  border-radius: 20px;
  overflow: hidden;
  &::after {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background: rgba(0, 0, 0, 0.1); /* White with 30% opacity */
    border-radius: 15px;
  }
`;
const LogoContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  top: 8%;
  left: 22%;
  transform: translate(-50%, -50%);
  width: 100%;
  z-index:10;
  filter:brightness(110%);
`;
const BackLogoContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  bottom:-1%;
  left: 14%;
  transform: translate(-50%, -50%);
  width: 100%;
  z-index:10;
  filter:brightness(110%);
`;
// Our Card component
function Card({name,funFacts,img,rating,id,type,background}) {
  const [isFlipped, setIsFlipped] = useState(false);
  const handleClick = () => {
    setIsFlipped(!isFlipped);
  };
  return (
    <StyledReactCardFlip isFlipped={isFlipped} flipDirection="horizontal">
      <CardFront onClick={handleClick} >
      <OverlayImage src={background}/>
      <ImageContainer>
      
        <ImgContainer><img src={Me} style={{borderRadius:'20px',width:'100%'}}/></ImgContainer>
        <InsideFrame></InsideFrame>
        <LogoContainer><WholeLogo  width="4vw" height="3.9vh"></WholeLogo></LogoContainer>
      </ImageContainer>
          <SubContainer>
          <NameContainer>{name}</NameContainer>
          
          <TypeContainer>{type}</TypeContainer>
          <Banner>{Array.from({length:5},(_,i) =>(
          <StarIcon style={{color:'gold',position: 'relative', fontSize: '.9vw'}}key={i} sx={{ shadow: 4 }}/>
          ))}</Banner> 
          </SubContainer>
      </CardFront>
      <CardBack onClick={handleClick}>
        <OverlayImage src={background}/>
        <TextContainer>{funFacts}</TextContainer>
        <BackLogoContainer><WholeLogo  width="4vw" height="3.9vh"></WholeLogo></BackLogoContainer>
      </CardBack>
    </StyledReactCardFlip>
  );
}

export default Card;
