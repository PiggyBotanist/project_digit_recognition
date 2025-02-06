import React, { useRef, useEffect, useState } from "react";
import { Button, Grid2, Typography, TextField } from "@mui/material";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Collapse, Alert } from "@mui/material";

const DrawingBoard = ({ scale = 10 }) => {
  // References and state management
  const canvasRef = useRef(null);  // Reference to the canvas element
  const [isDrawing, setIsDrawing] = useState(false);  // Whether the user is drawing
  const [prediction, setPrediction] = useState("Prediction: ");  // Stores the prediction result
  const [probabilities, setProbabilities] = useState([]);  // Stores the prediction probabilities
  const [successMsg, setSuccessMsg] = useState("");  // Stores success message
  const [errorMsg, setErrorMsg] = useState("");  // Stores error message
  const [label, setLabel] = useState("");  // Stores the label for the drawing

  // Constants for canvas grid size and scale
  const PIXEL_SIZE = 28;  // MNIST style 28x28 pixel grid
  const SCALED_SIZE = PIXEL_SIZE * scale;  // Scaled size for better visibility

  // Initialize canvas properties and scale on mount
  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    // Set canvas width, height, and scale
    canvas.width = SCALED_SIZE;
    canvas.height = SCALED_SIZE;
    ctx.scale(scale, scale);  // Scale for better visibility

    // Fill canvas with black (to make it a white background with black drawing)
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, PIXEL_SIZE, PIXEL_SIZE);
  }, [scale]);  // Re-run effect when scale changes

  // Start drawing on mouse down
  const startDrawing = (e) => {
    setIsDrawing(true);
    draw(e);
  };

  // Stop drawing on mouse up or mouse leave
  const stopDrawing = () => {
    setIsDrawing(false);
  };

  // Handle the drawing logic
  const draw = (e) => {
    if (!isDrawing) return;  // Don't draw if not in drawing mode

    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    // Get mouse position relative to canvas
    const rect = canvas.getBoundingClientRect();
    const x = Math.floor((e.clientX - rect.left) / scale);
    const y = Math.floor((e.clientY - rect.top) / scale);

    // Draw a white pixel to simulate the drawing
    ctx.fillStyle = "white";
    ctx.fillRect(x, y, 1, 1);

    // Dim surrounding pixels with a light gray color for softening the drawing
    ctx.fillStyle = "rgba(255, 255, 255, 0.2)";  // Light gray tint
    const offsets = [
      [-1,  1], [0,  1], [1,  1],
      [-1,  0], [0,  0], [1,  0],
      [-1, -1], [0, -1], [1, -1],
    ];

    // Apply the gray tint to surrounding pixels
    offsets.forEach(([dx, dy]) => {
      const newX = x + dx;
      const newY = y + dy;
      if (newX >= 0 && newX < PIXEL_SIZE && newY >= 0 && newY < PIXEL_SIZE) {
        ctx.fillRect(newX, newY, 1, 1);
      }
    });
  };

  // Update label input (check for valid label)
  const updateLabel = (e) => {
    let label = e.target.value;
    if (label < 10 && label > -1) {
      setLabel(label);  // Update label state if valid
    } else {
      e.target.value = "";    // Clear input if invalid label
    }
  };

  // Make prediction by sending canvas image to the backend
  const make_prediction = () => {
    const canvas = canvasRef.current;

    // Convert canvas to Base64 image
    const imageBase64 = canvas.toDataURL("image/png");

    // Send the image data to the backend for prediction
    fetch("/classifier/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ image: imageBase64 }),
    })
      .then((response) => response.json())
      .then((data) => {
        // Update the prediction and probabilities state
        setPrediction(`Prediction: ${data.prediction}`);
        setProbabilities(data.probabilities);
        setSuccessMsg("Prediction Made!");
      })
      .catch((error) => {
        setErrorMsg("Error making prediction.");
      });
  };

  // Save the image with label to the backend
  const save = () => {
    const canvas = canvasRef.current;
    const label = document.getElementById("outlined-basic").value.trim();

    // Ensure both the label and drawing are provided
    if (!canvas || label === "") {
      setErrorMsg("Please ensure both the label and the drawing are provided.");
      return;
    }

    // Convert canvas to Base64 image
    const imageBase64 = canvas.toDataURL("image/png");

    // Send label and image to the backend for saving
    fetch("/classifier/save", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ label: label, image: imageBase64 }),
    })
      .then((response) => {
        if (response.ok) {
          setSuccessMsg("Image and label successfully saved!");
          clearCanvas();                            // Clear canvas after saving
        } else {
          setErrorMsg("Failed to save data.");
        }
      })
      .catch((error) => {
        setErrorMsg("An error occurred while saving the data.");
      });
  };

  // Clear the canvas and reset relevant state
  const clearCanvas = () => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    ctx.fillStyle = "black";                        // Reset to black
    ctx.fillRect(0, 0, PIXEL_SIZE, PIXEL_SIZE);
    setLabel("");                                   // Clear label input
    setPrediction("Prediction: ");                  // Reset prediction
    setProbabilities([]);                           // Reset probabilities
  };

  return (
    <Grid2 container spacing={1} direction="column" alignItems="center">
      <Typography variant="h5" component="h2">
        Handwritten Digit Recognition
      </Typography>
      <Grid2>
        {/* Display the prediction */}
        <Typography variant="body1">{prediction}</Typography> 
      </Grid2>
      <Grid2>
        <canvas
          ref={canvasRef}
          style={{
            border: "1px solid white",
            width: `${SCALED_SIZE}px`,
            height: `${SCALED_SIZE}px`,
            imageRendering: "pixelated",    // Keep pixelated sharpness
            backgroundColor: "black",       // Set background to black
          }}
          onMouseDown={startDrawing}        // Start drawing on mouse down
          onMouseMove={draw}                // Draw on mouse move
          onMouseUp={stopDrawing}           // Stop drawing on mouse up
          onMouseLeave={stopDrawing}        // Stop drawing on mouse leave
        />
      </Grid2>
      {/* Display success or error messages */}
      <Grid2 xs={12} align="center">
        <Collapse in={errorMsg != "" || successMsg != ""}>
          {successMsg != "" ? (
            <Alert severity="success" onClose={() => {setSuccessMsg("")}}>{successMsg}</Alert>
          ) : (
            <Alert severity="error" onClose={() => {setErrorMsg("")}}>{errorMsg}</Alert>
          )}
        </Collapse>
      </Grid2>
      {/* Label input field */}
      <TextField id="outlined-basic" label="Label" variant="outlined" value={label} onChange={updateLabel} />
      {/* Buttons for prediction, clearing canvas, and saving */}
      <Grid2>
        <Button variant="contained" color="primary" onClick={make_prediction}>Predict</Button>
      </Grid2>
      <Grid2>
        <Button variant="contained" onClick={clearCanvas}>Clear Canvas</Button>
      </Grid2>
      <Grid2>
        <Button variant="contained" onClick={save}>Submit</Button>
      </Grid2>
      {/* Display the probabilities table if available */}
      <Grid2>
        {probabilities.length > 0 && (
          <TableContainer component={Paper} style={{ marginTop: "2px", maxWidth: "400px", margin: "auto" }}>
            <Typography variant="h6" style={{ padding: "2px", textAlign: "center" }}>
              Class Probabilities
            </Typography>
            <Table sx={{ minWidth: 300 }} aria-label="class probabilities table">
              <TableHead>
                <TableRow style={{ padding: "2px" }}>
                  <TableCell style={{ fontWeight: "bold" }}>Class</TableCell>
                  <TableCell align="right" style={{ fontWeight: "bold" }}>
                    Probability (%)
                  </TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {probabilities.map((prob, index) => (
                  <TableRow key={index} sx={{ "& td, & th": { padding: "1px" } }}>
                    <TableCell component="th" scope="row">
                      {index}
                    </TableCell>
                    <TableCell align="right">{(prob * 100).toFixed(2) + "%"}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Grid2>
    </Grid2>
  );
};

export default DrawingBoard;
