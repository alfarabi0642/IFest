import React, { useRef } from 'react';
import Plus from "../assets/Plus.svg?react";

// The component now accepts an `onFileSelect` function as a prop
function Add({ onFileSelect }) {
    // useRef is used to access the hidden file input element
    const fileInputRef = useRef(null);

    const handleButtonClick = () => {
        // When the button div is clicked, it programmatically clicks the hidden input
        fileInputRef.current.click();
    };

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            // Pass the selected file up to the parent component
            onFileSelect(file);
        }
    };

    return (
        <div className="relative select-none ml-2">
            {/* The visible button the user clicks */}
            <div 
                onClick={handleButtonClick}
                className="bg-white hover:shadow-md select-none text-sm flex justify-center items-center border-solid border-black border-1 rounded-full cursor-pointer font-poppins w-22 mt-2 mr-106 h-8"
            >
                <Plus />
                Add
            </div>

            {/* A hidden file input that we control programmatically */}
            <input 
                type="file"     
                ref={fileInputRef}
                onChange={handleFileChange}
                style={{ display: 'none' }}
                accept=".pdf" // Only allow PDF files
            />
        </div>
    );
}

export default Add;