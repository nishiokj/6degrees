import React from 'react'
import otherLogo from './images/logo1.png'

function OtherLogo({size}) {
    return (
        <div>
            <img src={otherLogo} alt="logo" style={{width:size, height:size}} />
        </div>
    )
}

export default OtherLogo;