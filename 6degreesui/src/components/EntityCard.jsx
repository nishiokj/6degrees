import React, { useState } from 'react';
import styled from 'styled-components';
import ReactCardFlip from 'react-card-flip';
import Me from '../images/headshot_jevin_thumbnail.png'
import moment from 'moment-timezone';
import axios from 'axios';
import StarIcon from '@mui/icons-material/Star';
import StarHalfIcon from '@mui/icons-material/StarHalf';
import { shadows } from '@mui/system';
// Get current date in Eastern American Time


const CardFront = styled.div`
  width: 9vw;  // This could be any percentage you find suitable.
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
  &:hover {
    box-shadow: 0 20px 30px 0 rgba(0,0,0,0.2);
  }
`;
const ImageContainer = styled.div`

  background-image: url('');
  background-size: cover;
  transition: 0.3s;
  overflow:hidden;
`;

const InsideFrame = styled.div`

  background-image: url('');
  background-size: cover;
  box-shadow: 0 12px 15px rgba(0, 0, 0, 0.2)
  border: 2px solid #fff;
  box-shadow: 0 10px 20px 0 rgba(0,0,0,0.2);
  transition: 0.3s;
  overflow:hidden;
  
  
`;

const StyledReactCardFlip = styled(ReactCardFlip)`
  width: 100%;
  height: 100%;
`;
const RatingContainer = styled.div`

`;
const Banner = styled.div`
  background-image: linear-gradient(to bottom right, #FF78, #669999); // Gradient for depth
  box-shadow: 0 1px 10px rgba(0, 0, 0, 0.2); // Deeper shadow for depth
  width:100%;
  height:30%;
  border-radius: 15px;
`;

const TypeContainer = styled.div`
  color: #fff;
  flex-basis: 45%;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  font-size: .7vw;
  font-family: 'Courier New', Courier, monospace; // Use your preferred font
  font-weight:900;
  text-transform: uppercase; // Convert text to uppercase
  letter-spacing: 3px; // Increase spacing between letters
  text-shadow: 1px 2px 4px rgba(0,0,0,0.5); // Text shadow for 3D effect
  color:#fff;
  overflow:hidden;
`;
const NameContainer = styled.div`
  display: flex;
  flex-basis:55%;
  margin-right:25px;
  align-items: left;
  text-align:left;
  background: transparent;
  font-family: 'Courier New', Courier, monospace; // Use your preferred font
  font-size:.7vw; // Adjust based on your preference
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
  justify-content: space-between;
  box-shadow: 0px 10px 15px rgba(0, 0, 0, 0.3); // this gives the 3D effect
   // you can adjust the thickness as you like
  border-image: inherit;
  border-image-slice: 1;
  overflow:hidden;
  border-radius: 5px;
`;

// Our Card component
function Card({name,funFacts,img,rating,id,type}) {
  const [isFlipped, setIsFlipped] = useState(false);
  const handleClick = () => {
    setIsFlipped(!isFlipped);
  };
  return (
    <StyledReactCardFlip isFlipped={isFlipped} flipDirection="horizontal">
      <CardFront onClick={handleClick} >
      <ImageContainer imageUrl={img}>
        <img src={Me}  style={{borderRadius:'20px',width: '100%', height: '100%',shadows:'0 15px 15px rgba(0, 0, 0, 0.2)'}}></img>
        <InsideFrame></InsideFrame>
</ImageContainer>
          <SubContainer>
          <NameContainer>{name}</NameContainer>
          <TypeContainer><Banner>{Array.from({length:5},(_,i) =>(
          <StarIcon style={{color:'gold',position: 'relative', fontSize: '.65vw'}}key={i} sx={{ shadow: 4 }}/>
          ))}</Banner> {type}</TypeContainer>
          </SubContainer>
      </CardFront>
      <CardBack onClick={handleClick}>
        {funFacts}
      </CardBack>
    </StyledReactCardFlip>
  );
}

export default Card;
