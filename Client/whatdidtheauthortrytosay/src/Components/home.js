import React, { useEffect, useState } from "react";
import "@fontsource/pixelify-sans"; 
import { predict_t5_base, predict_t5_small } from "../Services/analysis_service";

const Home = () => {
    const [inputText, setInputText] = useState("");
    const [outputText, setOutputText] = useState("");
    const [selectedModel, setSelectedModel] = useState("t5-small"); 

    useEffect(() => {
        setInputText("");
        setOutputText("");
        setSelectedModel("t5-small");
    }, []);

    const analyzeText = async () => {
        if (!inputText || !selectedModel) {
            alert("Please enter some text to analyze.");
            return;
        }
        else{
            if (selectedModel === "t5-small") {
                const response = await predict_t5_small(inputText);
                setOutputText(response["output"]);
            } else if (selectedModel === "t5-base") {
                const response = await predict_t5_base(inputText);
                setOutputText(response["output"]);
            }
        }
    };

    return (
        
        <div
            className="home"
            style={{
                height: "100vh",
                width: "100vw",
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
                backgroundColor: "#f4f4f4",
                overflow: "hidden",
            }}
        >
            <div>
                <h1
                    style={{
                        fontFamily: "Pixelify Sans",
                        fontSize: "40px",
                        color: "#000",
                        marginBottom: "20px",
                    }}
                >
                    What Did The Author Try To Say?
                </h1>
            </div>
            <div
                className="book-container"
                style={{
                    width: "100%",
                    height: "100%",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    backgroundImage: "url('/openedbook_pixelated.jpeg')",
                    backgroundSize: "cover",
                    backgroundRepeat: "no-repeat",
                    backgroundPosition: "center",
                    position: "relative",
                }}
            >
                
                <div
                    className="left-page"
                    style={{
                        position: "absolute",
                        left: "20%",
                        top: "35%", 
                        width: "28%",
                        height: "50%", 
                        display: "flex",
                        flexDirection: "column",
                        justifyContent: "space-between",
                        alignItems: "center",
                        boxShadow: "0 2px 5px rgba(0, 0, 0, 0.1)",
                    }}
                >
                    <textarea
                        value={inputText}
                        onChange={(e) => setInputText(e.target.value)}
                        placeholder="Type here..."
                        style={{
                            width: "100%",
                            height: "70%", 
                            padding: "10px",
                            fontSize: "15px",
                            fontFamily: "Pixelify Sans",
                            color: "#000",
                            backgroundColor: "rgba(255, 255, 255, 0.0)",
                            border: "0px solid #ccc",
                            outline: "none",
                            resize: "none",
                        }}
                    />
                    <div
                        style={{
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            width: "100%",
                            height: "30%", 
                        }}
                    >
                        <button
                            onClick={analyzeText}
                            style={{
                                width: "120px",
                                height: "40px",
                                fontSize: "15px",
                                fontFamily: "Pixelify Sans",
                                color: "#fff",
                                backgroundColor: "#91A195",
                                border: "none",
                                borderRadius: "5px",
                                cursor: "pointer",
                                outline: "none",
                                boxShadow: "0 2px 5px rgba(0, 0, 0, 0.1)",
                            }}
                        >
                            Analyze
                        </button>
                    </div>
                    
                    <div
                        style={{
                            width: "100%",
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            marginBottom: "10px",
                        }}
                    >
                        <label style={{ marginRight: "10px", fontFamily: "Pixelify Sans" }}>
                            <input
                                type="radio"
                                value="t5-small"
                                checked={selectedModel === "t5-small"}
                                onChange={() => setSelectedModel("t5-small")}
                                style={{ marginRight: "5px" }}
                            />
                            T5-Small
                        </label>
                        <label style={{ marginRight: "10px", fontFamily: "Pixelify Sans" }}>
                            <input
                                type="radio"
                                value="t5-base"
                                checked={selectedModel === "t5-base"}
                                onChange={() => setSelectedModel("t5-base")}
                                style={{ marginRight: "5px" }}
                            />
                            T5-Base
                        </label>
                        <label style={{ fontFamily: "Pixelify Sans" }}>
                            <input
                                type="radio"
                                value="bert"
                                checked={selectedModel === "bert"}
                                onChange={() => setSelectedModel("bert")}
                                style={{ marginRight: "5px" }}
                            />
                            Bert
                        </label>
                    </div>
                </div>

                <div
                    className="right-page"
                    style={{
                        position: "absolute",
                        right: "20%",
                        top: "35%", 
                        width: "28%",
                        height: "50%", 
                        display: "flex",
                        flexDirection: "column",
                        justifyContent: "space-between",
                        alignItems: "center",
                        boxShadow: "0 2px 5px rgba(0, 0, 0, 0.1)", 
                    }}
                >
                    <div
                        style={{
                            width: "100%",
                            height: "70%",
                            fontSize: "15px",
                            fontFamily: "Pixelify Sans",
                            color: "#000",
                            border: "none",
                            outline: "none",
                            overflowY: "auto",
                            backgroundColor: "rgba(255, 255, 255, 0.0)",
                        }}
                    >
                        {outputText || "The analysis will appear here..."}
                    </div>
                    <div
                        style={{
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            width: "100%",
                            height: "30%",
                        }}
                    >
                        <button
                            onClick={() => {
                                setOutputText("");
                                setInputText("");
                            }}
                            style={{
                                width: "120px",
                                height: "40px",
                                fontSize: "15px",
                                fontFamily: "Pixelify Sans",
                                color: "#fff",
                                backgroundColor: "#91A195",
                                border: "none",
                                borderRadius: "5px",
                                cursor: "pointer",
                                outline: "none",
                                boxShadow: "0 2px 5px rgba(0, 0, 0, 0.1)",
                            }}
                        >
                            Clear
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Home;
