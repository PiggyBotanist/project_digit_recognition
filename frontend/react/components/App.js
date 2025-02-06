import { createRoot } from 'react-dom/client';
import React, { Component } from "react";
import { render } from "react-dom";
import DrawingBoard from './DrawingBoard';

const App = (props) => {
    return(
        <DrawingBoard/>
    )
};

// integrate the react component inside the root container we defined
const rootDiv = document.getElementById("react_root");
const root = createRoot(rootDiv);
root.render(<App />);