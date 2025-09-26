// src/Details.jsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import defaultLogo from "./assets/googleicon.png";

const API_URL = 'http://127.0.0.1:8000';

// The component now receives documentId and an onClose function as props
function Details({ documentId, onClose }) {
  // State for storing the full contract details
  const [details, setDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // This useEffect hook runs whenever the documentId prop changes
  useEffect(() => {
    if (!documentId) return; // Don't fetch if there's no ID

    const fetchDetails = async () => {
      try {
        setLoading(true);
        // API call to get the full details for the selected contract
        const response = await axios.get(`${API_URL}/contracts/${documentId}`);
        setDetails(response.data);
        setError(null);
      } catch (err) {
        setError('Failed to load contract details.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchDetails();
  }, [documentId]); // The dependency array ensures this runs when documentId changes

  // Show a loading state
  if (loading) {
    return (
        <div className="bg-white right-0 top-0 h-screen w-[58vh] flex flex-col p-7 fixed shadow-xl">
            <p>Loading details...</p>
        </div>
    );
  }

  // Show an error state
  if (error) {
    return (
        <div className="bg-white right-0 top-0 h-screen w-[58vh] flex flex-col p-7 fixed shadow-xl">
            <p style={{ color: 'red' }}>{error}</p>
            <button onClick={onClose} className="mt-4">Close</button>
        </div>
    );
  }

  // --- Main component render with data ---
  return (
    <div className="bg-white right-0 top-0 h-screen w-[58vh] flex flex-col p-7 overflow-y-auto fixed shadow-xl z-50">
      {/* Close button added */}
      <button onClick={onClose} className="absolute top-4 right-4 text-2xl font-bold text-gray-500 hover:text-gray-800">&times;</button>
      
      <div className="text-center">
        <img src={defaultLogo} alt="Logo Perusahaan" className="w-20 h-20 rounded-full mx-auto mb-4" />
        <h1 className="p-2 font-poppinsbold text-xl text-primary">
          {details?.contractMetadata?.documentTitle}
        </h1>
        <h2 className="font-poppins text-md mt-2">
          {details?.contractSummarization?.parties[0]?.name}
        </h2>
        <hr className="my-5 border-1" />
      </div>

      <div>
        <h3 className="text-lg font-poppins font-bold">Contract Overview:</h3>
        <p className="mt-2 ml-4 text-sm font-poppins text-gray-500">
          {details?.contractSummarization?.executiveSummary}
        </p>

        <h3 className="text-lg mt-6 font-poppins font-bold ">Key Terms:</h3>
        <ul className="font-poppins text-sm list-disc pl-7 leading-9 text-gray-500">
          {details?.contractSummarization?.keyTerms.map((item, index) => (
            <li key={index}>
              <strong>{item.term}:</strong> {item.definition}
            </li>
          ))}
        </ul>
        
        {/* You can add more sections here for other data like Risks, Obligations etc. */}
        <h3 className="text-lg mt-6 font-poppins font-bold">Risks & Compliance:</h3>
        <ul className="font-poppins text-sm list-disc pl-7 leading-9 text-gray-500">
          {details?.clauseLevelRiskAndCompliance?.clauses.map((clause) => (
            <li key={clause.clauseId}>
              <strong>{clause.clauseTitle} (Risk: {clause.riskAnalysis?.riskLevel}):</strong> {clause.riskAnalysis?.riskDescription}
            </li>
          ))}
        </ul>

      </div>
      <div className="mt-auto pt-6 text-center flex justify-center items-center">
        <button className="font-poppinsbold bg-gradient-to-r from-secondary to-primary text-white py-2 px-8 rounded-3xl h-13">
          Review Contract
        </button>
      </div>
    </div>
  );
}

export default Details;