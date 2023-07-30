import React, { useState, useEffect } from 'react';
import axios from 'axios';
import moment from 'moment-timezone';
import Card from './EntityCard'; // assuming you have a Card component

const Game = (category) => {
    const [data, setData] = useState([]); // holds the game data

    useEffect(() => {
        // Function to get the date in US/Eastern timezone
        const getEasternTime = () => {
            return moment().tz("America/New_York").format('YYYY-MM-DD');
        }

        // Function to fetch game data from your API
        const fetchGameData = async () => {
            const date = getEasternTime();
            try {
                const url = `http://127.0.0.1:5011/fetchCards?date=${date}&category=cinema`
                const response = await axios.get(url);
                console.log(response)
                const entities = Object.keys(response.data)
                .filter(key => key.startsWith('entity'))
                .map(key => response.data[key]);
                setData(entities);
                
            } catch (error) {
                console.error('Error fetching game data: ', error);
            }
        }

        fetchGameData();
    }, []); // empty dependency array to run once on mount
    return (
        <div>
            {data.map((entity, index) => (
                <Card key={index} {...entity} />
            ))}
        </div>
    );
};

export default Game;
